import asyncio
import logging

from cmis import (
    Address,
    LowPwrRequestSW,
    MemMap,
    ModuleState,
    DPStateHostLane,
)

from ..dpsm import DataPathStateMachine
from ..proto.emulator_pb2 import ReadRequest, WriteRequest

logger = logging.getLogger(__name__)


class CMISTransceiver:
    def __init__(self, index: int, config: dict, mem_map: MemMap | None = None):
        super().__init__()
        self._index = index
        self._config = config
        self._queue: asyncio.Queue = asyncio.Queue()
        self._task: asyncio.Task | None = None
        self._present = False

        self.mem_map = MemMap() if mem_map is None else mem_map

        self._dpsms: dict[int, DataPathStateMachine] = {}

        if config.get("present"):
            self.plugin()
        else:
            self._init()

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
            logger.info(
                f"Applying DPInit({i}): {value:b} AppSelCode: {scs.AppSelCode.value}"
            )
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
        def set_value(field, value):
            if type(value) is list:
                for i, val in enumerate(value):
                    set_value(field[i], val)
            elif type(value) is dict:
                for k, val in value.items():
                    set_value(getattr(field, k), val)
            else:
                field.set_value_from_str(str(value))

        for k, v in self._config.get("defaults", {}).items():
            try:
                field = getattr(self.mem_map, k)
            except AttributeError:
                logger.error(f"Invalid attribute: {k}")
                continue

            set_value(field, v)

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

        self.mem_map.ModuleState.value = ModuleState.MODULE_LOW_PWR
        self.mem_map.LowPwrRequestSW.value = LowPwrRequestSW.LOW_POWER_MODE

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

    def plugin(self) -> None:
        if self._task:
            logger.warning(f"Transceiver({self._index}) already running")
            return

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
                    elif address.includes(
                        self.mem_map.SCS0_ApplyTriggers.ApplyDPInitLane.address
                    ):
                        if self._apply_dpinit():
                            self._init_dpsms()
