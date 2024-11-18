import asyncio
import logging
from enum import Enum
from types import SimpleNamespace

from ..dpsm import DataPathStateMachine
from ..eeprom import CmisMemMap, RawEEPROM, XcvrEEPROM, consts
from ..proto.emulator_pb2 import ReadRequest, WriteRequest

logger = logging.getLogger(__name__)


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
                logger.warn(f"DPSM invalid config: {dpsm}")

        self._dpsms = dpsms

    def _apply_dpinit(self):
        for i in range(1, 9):
            value = self._eeprom.read(f"{consts.STAGED_CTRL_APSEL_FIELD}_0_{i}")
            logger.info(f"Applying DPInit({i}): {value:b}")
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
    def present(self) -> bool:
        return self._present

    async def read(self, req: ReadRequest) -> bytearray:
        if not req.force and not self.present:
            return bytearray(b"\x00" * req.length)
        return self._raw_eeprom.Read(req).data

    async def write(self, req: WriteRequest) -> None:
        self._raw_eeprom.Write(req)
        offset = req.page * 128 + req.offset
        fields = self._offset_to_field.get(offset, [])
        await self._queue.put(SimpleNamespace(req=req, fields=fields))

    async def plugout(self) -> None:
        self._present = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                self._task = None
            logger.debug(f"Transceiver({self._index}) task cancelled")

    async def plugin(self) -> None:
        self._init()
        self._present = True
        self._task = asyncio.create_task(self._run())

    async def _run(self):

        logger.info(f"Transceiver({self._index}) started")

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
                    logger.info(f"Updating module state: {prev_state} -> {state}")
                    self._eeprom.write(consts.MODULE_STATE, state.value)
                    self._state = state
                continue

            match self._state:
                case self.State.LowPwr:
                    pass
                case self.State.Ready:
                    logger.info(f"ready: {field_names}, {ev.req.data[0]:x}")
                    dp_state_fields = [
                        consts.DATAPATH_DEINIT_FIELD,
                        consts.TX_DISABLE_FIELD,
                    ]
                    if any(f in field_names for f in dp_state_fields):
                        for dpsm in self._dpsms.values():
                            if not dpsm.update_state():
                                logger.warn(f"DPSM invalid config: {dpsm}")
                    elif f"{consts.STAGED_CTRL_APPLY_DPINIT_FIELD}_0" in field_names:
                        if self._apply_dpinit():
                            self._init_dpsms()
