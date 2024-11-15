import asyncio
import grpc


from types import SimpleNamespace
from enum import Enum
import traceback
import sys
import os

from .eeprom import RawEEPROM, XcvrEEPROM
from .eeprom import CmisMemMap, consts
from .proto import emulator_pb2 as pb2

# see https://github.com/grpc/grpc/issues/29459#issuecomment-1641587881
proto_dir = os.path.dirname(pb2.__file__)
sys.path.append(proto_dir)

from .proto import emulator_pb2_grpc  # noqa E402


class DataPathStateMachine:
    class State(Enum):
        Unknown = 0
        Deactivated = 1
        Init = 2
        Deinit = 3
        Activated = 4
        TxTurnOn = 5
        TxTurnOff = 6
        Initialized = 7

    def __init__(self, eeprom, dpid):
        self._eeprom = eeprom
        self._dpid = dpid

        self._state = 0b0000
        self._lanemask = [0] * 8
        self._appsels = [0] * 8
        self._explicit_controls = [0] * 8

        self._appsel = 0
        self._state = self.State.Unknown

    def add_lane(self, idx, appsel, explicit_control):
        self._lanemask[idx] = 1
        self._appsels[idx] = appsel
        self._explicit_controls[idx] = explicit_control

    def update_state(self):
        deinit = self._eeprom.read(consts.DATAPATH_DEINIT_FIELD)
        txdis = self._eeprom.read(consts.TX_DISABLE_FIELD)

        print(f"{deinit=}, {txdis=}, {self._lanemask=}, {self._appsels=}")

        lanes = [i for i, v in enumerate(self._lanemask) if v]
        appsels = [self._appsels[i] for i in lanes]
        if len(appsels) == 0:
            return False

        all_same = all(x == appsels[0] for x in appsels)
        if not all_same:
            return False

        deinits = [(deinit & (1 << i) > 0) for i in lanes]
        all_same = all(x == deinits[0] for x in deinits)
        if not all_same:
            self._deinit = True
            return False

        txdiss = [(txdis & (1 << i) > 0) for i in lanes]
        all_same = all(x == txdiss[0] for x in txdiss)
        if not all_same:
            self._txdis = True
            return False

        self._appsel = appsels[0]
        deinit = deinits[0]
        txdis = txdiss[0]

        prev_state = self._state

        state = self.State.Initialized
        if deinit:
            state = self.State.Deactivated
        elif not txdis:
            state = self.State.Activated

        if state != prev_state:
            for i in lanes:
                self._eeprom.write(f"DP{i+1}State", state.value)
                if state != self.State.Deactivated:
                    self._eeprom.write(
                        f"{consts.DPINIT_PENDING}{i+1}", 0
                    )  # flag down DP Pending

            print(f"updating DPSM({self._dpid}) state: {prev_state} -> {state}")
            self._state = state

        return True

    def __str__(self):
        return f"DPSM({self._dpid}): Lanes: {self._lanemask}, AppSel: {self._appsel}, State: {self._state}"


class CMISTransceiver:

    class State(Enum):
        LowPwr = 0b001
        PwrUp = 0b010
        Ready = 0b011
        PwrDn = 0b100
        Fault = 0b101

    def __init__(self, index):
        super().__init__()
        self._index = index
        self._queue = asyncio.Queue()
        self._task = None
        self._present = False

        self.mem_map = CmisMemMap()

        self._init()
        self._dpsms = {}

    def _init(self):
        self._state = self.State.LowPwr
        self._init_eeprom()

    def _init_dpsms(self):

        field = self.mem_map.get_field(consts.ACTIVE_APSEL_CODE)
        acs = self._eeprom._read(field.offset, 8)

        dpsms = {}
        for i, v in enumerate(acs):
            appsel = (v & 0b11110000) >> 4
            # CMIS v5.2 6.2.3.2
            # The special AppSel code value 0000b in the Data Path Configuration register of a host lane indicates that the
            # lane (together with its associated resources) is unused and not part of a Data Path. The DataPathID and
            # ExplicitControl fields of unused host lanes are irrelevant and may be ignored by the module.
            if appsel == 0:
                continue

            dpid = (v & 0b00001110) >> 1
            if dpid not in dpsms:
                dpsms[dpid] = DataPathStateMachine(self._eeprom, dpid)

            appsel = (v & 0b11110000) >> 4
            explicit_control = (v & 0b00000001) == 1

            dpsm = dpsms[dpid]
            dpsm.add_lane(i, appsel, explicit_control)

        for dpsm in dpsms.values():
            if not dpsm.update_state():
                print(f"DPSM invalid config: {dpsm}")

        self._dpsms = dpsms

    def _apply_dpinit(self):
        for i in range(1, 9):
            value = self._eeprom.read(f"{consts.STAGED_CTRL_APSEL_FIELD}_0_{i}")
            print(f"Applying DPInit({i}): {value:b}")
            name = f"{consts.ACTIVE_APSEL_HOSTLANE}{i}"
            field = self.mem_map.get_field(name)
            self._eeprom._write(field.get_offset(), 1, bytearray([value]))
            appsel = (value & 0b11110000) >> 4
            if appsel == 0:
                continue

            # TODO validate the config and set appropriate status
            self._eeprom.write(f"{consts.CONFIG_LANE_STATUS}{i}", 1)  # ConfigSuccess
            self._eeprom.write(f"{consts.DPINIT_PENDING}{i}", 1)  # DP Pending
        return True

    def _init_eeprom(self):
        self._raw_eeprom = RawEEPROM()

        self._offset_to_field = {}
        for field in self.mem_map._get_all_fields().values():
            if field.offset not in self._offset_to_field:
                self._offset_to_field[field.offset] = []
            self._offset_to_field[field.offset].append(field)

        self._eeprom = XcvrEEPROM(self._index, self._raw_eeprom, self.mem_map)

        self._eeprom.write(consts.ID_FIELD, 24)  # QSFP-DD
        self._eeprom.write(consts.ID_ABBRV_FIELD, 24)  # QSFP-DD
        self._eeprom.write(consts.VENDOR_NAME_FIELD, "dummy")
        self._eeprom.write(consts.CMIS_MAJOR_REVISION, 5)
        self._eeprom.write(consts.CMIS_MINOR_REVISION, 3)
        self._eeprom.write(consts.MEDIA_TYPE_FIELD, 2)  # sm_media_interface
        self._eeprom.write(consts.POWER_CLASS_FIELD, 0b111)  # Power class 8

        # see sff8024.py for the following codes
        self._eeprom.write(
            f"{consts.HOST_ELECTRICAL_INTERFACE}_1", 79
        )  # 79: '400GAUI-4-S C2M (Annex 120G)'
        self._eeprom.write(
            f"{consts.MODULE_MEDIA_INTERFACE_SM}_1", 28
        )  # 28: '400GBASE-DR4 (Cl 124)',
        self._eeprom.write(f"{consts.HOST_LANE_COUNT}_1", 4)
        self._eeprom.write(f"{consts.MEDIA_LANE_COUNT}_1", 4)
        self._eeprom.write(f"{consts.HOST_LANE_ASSIGNMENT_OPTION}_1", 0b00000001)
        self._eeprom.write(f"{consts.MEDIA_LANE_ASSIGNMENT_OPTION}_1", 0b00000001)

        self._eeprom.write(
            f"{consts.HOST_ELECTRICAL_INTERFACE}_2", 71
        )  # 71: '200GBASE-CR2 (Clause 162)
        self._eeprom.write(
            f"{consts.MODULE_MEDIA_INTERFACE_SM}_2", 23
        )  # 23: '200GBASE-DR4 (Cl 121)',
        self._eeprom.write(f"{consts.HOST_LANE_COUNT}_2", 2)
        self._eeprom.write(f"{consts.MEDIA_LANE_COUNT}_2", 2)
        self._eeprom.write(f"{consts.HOST_LANE_ASSIGNMENT_OPTION}_2", 0b00000101)
        self._eeprom.write(f"{consts.MEDIA_LANE_ASSIGNMENT_OPTION}_2", 0b00000101)

        # default staged control set 0, data path configuration
        # and default active control set
        for i in range(1, 9):
            value = 0b00010010  # appsel: 1, dpid: 1
            if i > 4:
                value = 0
            self._eeprom.write(f"{consts.STAGED_CTRL_APSEL_FIELD}_0_{i}", value)

            name = f"{consts.ACTIVE_APSEL_HOSTLANE}{i}"
            field = self.mem_map.get_field(name)
            self._eeprom._write(field.get_offset(), 1, bytearray([value]))

        self._eeprom.write(consts.DP_PATH_INIT_DURATION, 0b0111)  # 1s < t < 5s

        field = self.mem_map.get_field(consts.TX_DISABLE_SUPPORT_FIELD)
        v = self._eeprom._read(field.get_offset(), 1)
        v = v[0] | (1 << field.bitpos)
        self._eeprom._write(field.get_offset(), 1, bytearray([v]))

        self._eeprom.write(consts.MODULE_STATE, 0b01)  # low power

    @property
    def present(self):
        return self._present

    async def read(self, req):
        if not req.force and not self.present:
            return bytearray(b"\x00" * req.length)
        return self._raw_eeprom.Read(req).data

    async def write(self, req):
        self._raw_eeprom.Write(req)
        offset = req.page * 128 + req.offset
        fields = self._offset_to_field.get(offset, [])
        await self._queue.put(SimpleNamespace(req=req, fields=fields))

    async def plugout(self):
        self._present = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                self._task = None

    async def plugin(self):
        self._init()
        self._present = True
        self._task = asyncio.create_task(self._run())

    async def _run(self):

        while True:
            ev = await self._queue.get()
            field_names = [f.name for f in ev.fields]
            if consts.MODULE_LEVEL_CONTROL in field_names:
                control = ev.req.data[0]
                prev_state = self._state
                if control & 0b100:
                    self._init()

                if control & 0b1000:
                    state = self.State.LowPwr
                else:
                    state = self.State.Ready
                    self._init_dpsms()

                if state != prev_state:
                    print(f"Updating module state: {prev_state} -> {state}")
                    self._eeprom.write(consts.MODULE_STATE, state.value)
                    self._state = state
                continue

            match self._state:
                case self.State.LowPwr:
                    pass
                case self.State.Ready:
                    print(f"ready: {field_names}, {ev.req.data[0]:x}")
                    dp_state_fields = [
                        consts.DATAPATH_DEINIT_FIELD,
                        consts.TX_DISABLE_FIELD,
                    ]
                    if any(f in field_names for f in dp_state_fields):
                        for dpsm in self._dpsms.values():
                            if not dpsm.update_state():
                                print(f"DPSM invalid config: {dpsm}")
                    elif f"{consts.STAGED_CTRL_APPLY_DPINIT_FIELD}_0" in field_names:
                        if self._apply_dpinit():
                            self._init_dpsms()


class EmulatorServer(emulator_pb2_grpc.SfpEmulatorService):
    def __init__(self):
        super().__init__()
        self.xcvrs = {}
        self.monitors = []

    async def Read(self, req, context):
        if req.index not in self.xcvrs:
            self.xcvrs[req.index] = CMISTransceiver(req.index)
        xcvr = self.xcvrs[req.index]

        data = bytes(await xcvr.read(req))

        await self.notify_monitors(
            {
                "index": req.index,
                "bank": req.bank,
                "page": req.page,
                "offset": req.offset,
                "data": data,
                "length": req.length,
                "present": xcvr.present,
                "write": False,
            }
        )

        return pb2.ReadResponse(data=data)

    async def Write(self, req, context):
        if req.index not in self.xcvrs:
            self.xcvrs[req.index] = CMISTransceiver(req.index)
        xcvr = self.xcvrs[req.index]
        # data = req.data
        #        print(
        #            f"write: bank: {req.bank}, page: {req.page:02X}h, offset: {req.offset}, length: {req.length}, data: {data if len(data) > 1 else bin(data[0])}"
        #        )

        try:
            await xcvr.write(req)
        except Exception as e:
            print(f"Error writing to EEPROM: {e}")
            traceback.print_exc()
            raise e from None

        await self.notify_monitors(
            {
                "index": req.index,
                "bank": req.bank,
                "page": req.page,
                "offset": req.offset,
                "data": req.data,
                "length": req.length,
                "present": xcvr.present,
                "write": True,
            }
        )

        return pb2.WriteResponse()

    async def GetInfo(self, req, context):
        if req.index not in self.xcvrs:
            self.xcvrs[req.index] = CMISTransceiver(req.index)
        xcvr = self.xcvrs[req.index]
        dpsms = [
            pb2.DataPathStateMachine(
                dpid=v._dpid, appsel=v._appsel, state=str(v._state)
            )
            for v in xcvr._dpsms.values()
        ]
        return pb2.GetInfoResponse(present=xcvr.present, dpsms=dpsms)

    async def UpdateInfo(self, req, context):
        if req.index not in self.xcvrs:
            self.xcvrs[req.index] = CMISTransceiver(req.index)
        xcvr = self.xcvrs[req.index]
        if req.present:
            await xcvr.plugin()
        else:
            await xcvr.plugout()

        return pb2.UpdateInfoResponse()

    async def notify_monitors(self, message):
        for queue in self.monitors:
            await queue.put(message)

    async def Monitor(self, request, context):
        queue = asyncio.Queue()
        self.monitors.append(queue)

        index = request.index

        try:
            while True:
                message = await queue.get()
                if index and message["index"] != index:
                    continue
                yield pb2.MonitorResponse(**message)
        except asyncio.CancelledError:
            pass
        finally:
            self.monitors.remove(queue)

    async def List(self, req, context):
        infos = []
        for k, v in self.xcvrs.items():
            info = pb2.GetInfoResponse()
            info.index = k
            info.present = v.present
            infos.append(info)

        return pb2.ListResponse(infos=infos)


async def _main():
    server = grpc.aio.server()
    emulator_pb2_grpc.add_SfpEmulatorServiceServicer_to_server(EmulatorServer(), server)
    port = 50051
    server.add_insecure_port(f"[::]:{port}")
    await server.start()

    try:
        print(f"Server started on port {port}")
        await server.wait_for_termination()
    except asyncio.CancelledError:
        print("Server is shutting down due to KeyboardInterrupt...")
        await server.stop(grace=10)


def main():
    try:
        asyncio.run(_main())
    except KeyboardInterrupt:
        print("Server interrupted by user, shutting down...")
