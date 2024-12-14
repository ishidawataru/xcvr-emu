import asyncio
import logging

from cmis import Address, LowPwrRequestSW, MemMap, ModuleState, DPStateHostLane, SteppedConfigOnly

from ..dpsm import DataPathStateMachine
from ..proto.emulator_pb2 import ReadRequest, WriteRequest

logger = logging.getLogger(__name__)


class CMISTransceiver:

    def __init__(self, index):
        super().__init__()
        self._index = index
        self._queue = asyncio.Queue()
        self._task = None
        self._present = False

        self.mem_map = MemMap()

        self._init()
        self._dpsms = {}

    def _init(self):
        self._state = ModuleState.MODULE_LOW_PWR
        self._init_eeprom()

    def _init_dpsms(self):

        dpsms = {}
        for i, acs in enumerate(self.mem_map.ACS_DPConfigLane):
            appsel = acs.AppSelCode.value
            # CMIS v5.2 6.2.3.2
            # The special AppSel code value 0000b in the Data Path Configuration register of a host lane indicates that the
            # lane (together with its associated resources) is unused and not part of a Data Path. The DataPathID and
            # ExplicitControl fields of unused host lanes are irrelevant and may be ignored by the module.
            if appsel == 0:
                continue

            dpid = acs.DataPathID.value
            if dpid not in dpsms:
                dpsms[dpid] = DataPathStateMachine(self.mem_map, dpid)

            explicit_control = acs.ExplicitControl.value
            dpsm = dpsms[dpid]
            dpsm.add_lane(i, appsel, explicit_control)

        for dpsm in dpsms.values():
            if not dpsm.update_state():
                logger.warning(f"DPSM invalid config: {dpsm}")

        self._dpsms = dpsms

    def _apply_dpinit(self):
        for i, scs in enumerate(self.mem_map.SCS0_DPConfigLane):
            value = scs.value
            logger.info(f"Applying DPInit({i}): {value:b} AppSelCode: {scs.AppSelCode.value}")
            self.mem_map.ACS_DPConfigLane[i].value = value
            if scs.AppSelCode.value == 0:
                continue

            # TODO validate the config and set appropriate status
            self.mem_map.DPInitPendingLane[i].value = (
                self.mem_map.DPInitPendingLane.PENDING
            )
            self.mem_map.ConfigStatusLane[i].value = (
                self.mem_map.ConfigStatusLane.SUCCESS
            )

        return True

    def _init_eeprom(self):
        self.mem_map.SFF8024Identifier.value = 24
        self.mem_map.SFF8024IdentifierCopy.value = 24
        self.mem_map.VendorName.value = "dummy"
        self.mem_map.CmisRevision.Major.value = 5
        self.mem_map.CmisRevision.Minor.value = 3
        self.mem_map.MediaType.value = 2  # sm_media_interface
        self.mem_map.ModulePowerClass.value = self.mem_map.ModulePowerClass.CLASS_8

        self.mem_map.ApplicationDescriptor[0].HostInterfaceID.value = (
            79  # 400GAUI-4-S C2M (Annex 120G)
        )
        self.mem_map.ApplicationDescriptor[0].MediaInterfaceID.value = (
            28  # 400GBASE-DR4 (Cl 124)
        )
        self.mem_map.ApplicationDescriptor[0].HostLaneCount.value = 4
        self.mem_map.ApplicationDescriptor[0].MediaLaneCount.value = 4
        self.mem_map.ApplicationDescriptor[0].HostLaneAssignmentOptions.value = (
            0b00000001
        )
        self.mem_map.MediaLaneAssignmentOptions[0].value = 0b00000001

        self.mem_map.ApplicationDescriptor[1].HostInterfaceID.value = (
            71  # 200GBASE-CR2 (Clause 162)
        )
        self.mem_map.ApplicationDescriptor[1].MediaInterfaceID.value = (
            23  # 200GBASE-DR4 (Cl 121)
        )
        self.mem_map.ApplicationDescriptor[1].HostLaneCount.value = 2
        self.mem_map.ApplicationDescriptor[1].MediaLaneCount.value = 2
        self.mem_map.ApplicationDescriptor[1].HostLaneAssignmentOptions.value = (
            0b00000101
        )
        self.mem_map.MediaLaneAssignmentOptions[1].value = 0b00000101

        # default staged control set 0, data path configuration
        # and default active control set
        for i, acs in enumerate(self.mem_map.ACS_DPConfigLane):
            if i > 3:
                acs.AppSelCode.value = 0
                acs.DataPathID.value = 0
            else:
                acs.AppSelCode.value = 1
                acs.DataPathID.value = 1

        for i, scs in enumerate(self.mem_map.SCS0_DPConfigLane):
            if i > 3:
                scs.AppSelCode.value = 0
                scs.DataPathID.value = 0
            else:
                scs.AppSelCode.value = 1
                scs.DataPathID.value = 1

        self.mem_map.MaxDurationDPInit.value = (
            self.mem_map.MaxDurationDPInit.BETWEEN_1_AND_5_S
        )

        self.mem_map.OutputDisableTxSupported.value = (
            self.mem_map.OutputDisableTxSupported.SUPPORTED
        )

        self.mem_map.ModuleState.value = ModuleState.MODULE_LOW_PWR
        self.mem_map.LowPwrRequestSW.value = LowPwrRequestSW.LOW_POWER_MODE

        self.mem_map.SteppedConfigOnly.value = SteppedConfigOnly.STEP_BY_STEP # no support for intervention-free reconfiguration

        for v in self.mem_map.DPStateHostLane:
            v.value = DPStateHostLane.DPDEACTIVATED

    @property
    def present(self) -> bool:
        return self._present

    def read(self, req: ReadRequest) -> bytes:
        if not req.force and not self.present:
            return b"\x00" * req.length
        return self.mem_map.read(req.index, req.page, req.offset, req.length)

    def write(self, req: WriteRequest) -> None:
        self.mem_map.write(req.index, req.page, req.offset, req.length, req.data)
        if req.length == 1:
            address = Address(req.page, req.offset)
        else:
            address = Address(req.page, (req.offset, req.offset + req.length - 1))
        self._queue.put_nowait((req, address))

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
        control = self.mem_map.ModuleGlobalControls
        self.write(
            WriteRequest(
                page=control.address.page,
                offset=control.address.offset,
                length=control.address.byte_size,
                data=bytes([control.value]),
            )
        )

    async def _run(self) -> None:

        logger.info(f"Transceiver({self._index}) started")

        while True:
            ev: tuple[WriteRequest, Address] = await self._queue.get()
            address: Address = ev[1]

            logger.debug(f"Handling address: {address}")

            if address.includes(self.mem_map.ModuleGlobalControls.address):
                prev_state = self._state
                software_reset = self.mem_map.SoftwareReset
                if software_reset.value == software_reset.RESET:
                    logger.info("Software reset")
                    self._init()

                low_pwr = self.mem_map.LowPwrRequestSW
                if low_pwr.value == low_pwr.LOW_POWER_MODE:
                    state = ModuleState.MODULE_LOW_PWR
                else:
                    state = ModuleState.MODULE_READY
                    self._init_dpsms()

                if state != prev_state:
                    logger.info(f"Updating module state: {prev_state} -> {state}")
                    self.mem_map.ModuleState.value = state
                    self._state = state

            match self._state:
                case ModuleState.MODULE_LOW_PWR:
                    pass
                case ModuleState.MODULE_READY:
                    logger.info(f"ready: {address}")
                    dp_state_fields = [
                        self.mem_map.DPDeinitLane,
                        self.mem_map.OutputDisableTx,
                    ]
                    if any(address == f.address for f in dp_state_fields):
                        for dpsm in self._dpsms.values():
                            if not dpsm.update_state():
                                logger.warning(f"DPSM invalid config: {dpsm}")
                    elif address.includes(self.mem_map.SCS0_ApplyTriggers.ApplyDPInitLane.address):
                        if self._apply_dpinit():
                            self._init_dpsms()
