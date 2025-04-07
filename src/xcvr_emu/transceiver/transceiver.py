import asyncio
import logging

from cmis import (
    Address,
    LowPwrRequestSW,
    MemMap,
    ModuleState,
    DPStateHostLane,
    BanksSupportedEnum,
    LanesEnum
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

        self._dpsms: dict[tuple[int, int], DataPathStateMachine] = {}

        if config.get("present"):
            self.plugin()
        else:
            self._init()

    def _iterate_banks(self, f, *args):
        num_banks = 1
        original_bank = self.mem_map.bank
        match self.mem_map.BanksSupported.value:
            case BanksSupportedEnum.BANKS_0_1_SUPPORTED:
                num_banks = 2
            case BanksSupportedEnum.BANKS_0_3_SUPPORTED:
                num_banks = 4

        try:
            for bank in range(num_banks):
                self.mem_map.bank = bank
                f(*args)
        finally:
            self.mem_map.bank = original_bank

    def _init(self):
        self._state = ModuleState.MODULE_LOW_PWR
        self._init_eeprom()

    def _init_dpsms(self):
        dpsms = {}
        def __init_dpsms(dpsms):
            bank = self.mem_map.bank
            for i, acs in enumerate(self.mem_map.ACS_DPConfigLane):
                appsel = acs.AppSelCode.value
                # CMIS v5.2 6.2.3.2
                # The special AppSel code value 0000b in the Data Path Configuration register of a host lane indicates that the
                # lane (together with its associated resources) is unused and not part of a Data Path. The DataPathID and
                # ExplicitControl fields of unused host lanes are irrelevant and may be ignored by the module.
                if appsel == 0:
                    continue

                dpid = acs.DataPathID.value
                if (bank, dpid) not in dpsms:
                    dpsms[(bank, dpid)] = DataPathStateMachine(self.mem_map, bank, dpid)

                explicit_control = acs.ExplicitControl.value
                dpsm = dpsms[(bank, dpid)]
                dpsm.add_lane(i, appsel, explicit_control)

            for ((b, _), dpsm) in dpsms.items():
                if b != bank:
                    continue

                if not dpsm.update_state():
                    logger.warning(f"DPSM invalid config: {dpsm}")

        self._iterate_banks(__init_dpsms, dpsms)
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

        # use ApplicationDescriptor1 for the default application
        default_app = self.mem_map.ApplicationDescriptor[0]

        count = 0
        match default_app.HostLaneCount.value:
            case LanesEnum.ONE_LANE:
                count = 1
            case LanesEnum.TWO_LANES:
                count = 2
            case LanesEnum.FOUR_LANES:
                count = 4
            case LanesEnum.EIGHT_LANES:
                count = 8

        assign = default_app.HostLaneAssignmentOptions.value

        # default staged control set 0, data path configuration
        # and default active control set
        def provision_acs_scs():
            dpid = 0
            current_count = 0
            for i, acs in enumerate(self.mem_map.ACS_DPConfigLane):
                if (assign >> i) & 0x1 == 1:
                    dpid += 1
                    current_count = 0
                if current_count < count:
                    acs.AppSelCode.value = 1
                    acs.DataPathID.value = dpid
                    current_count += 1
                else:
                    acs.AppSelCode.value = 0
                    acs.DataPathID.value = 0

            for i, scs in enumerate(self.mem_map.SCS0_DPConfigLane):
                scs.value = self.mem_map.ACS_DPConfigLane[i].value

            for v in self.mem_map.DPStateHostLane:
                v.value = DPStateHostLane.DPDEACTIVATED

        self._iterate_banks(provision_acs_scs)

        self.mem_map.ModuleState.value = ModuleState.MODULE_LOW_PWR
        self.mem_map.LowPwrRequestSW.value = LowPwrRequestSW.LOW_POWER_MODE


    @property
    def present(self) -> bool:
        return self._present

    def _page_bank_emulation(self, req: ReadRequest | WriteRequest) -> None:
        if req.offset >= 128: # upper page
            self.mem_map.PageSelect.value = req.page
            if req.page >= 0x10: # banked page
                max_bank = 1
                match self.mem_map.BanksSupported.value:
                    case BanksSupportedEnum.BANKS_0_1_SUPPORTED:
                        max_bank = 2
                    case BanksSupportedEnum.BANKS_0_3_SUPPORTED:
                        max_bank = 4

                if req.bank < max_bank:
                    self.mem_map.BankSelect.value = req.bank

    def read(self, req: ReadRequest) -> bytes:
        if not req.force and not self.present:
            return b"\x00" * req.length
        self._page_bank_emulation(req)
        return self.mem_map.read(req.bank, req.page, req.offset, req.length)

    def write(self, req: WriteRequest) -> None:
        self._page_bank_emulation(req)
        self.mem_map.write(req.bank, req.page, req.offset, req.length, req.data)
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
            bank: int = ev[0].bank

            self.mem_map.bank = bank

            logger.debug(f"Handling address: {address}, bank: {bank}")

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
                    logger.info(f"ready: {address}, bank: {bank}")
                    dp_state_fields = [
                        self.mem_map.DPDeinitLane,
                        self.mem_map.OutputDisableTx,
                    ]
                    if any(address == f.address for f in dp_state_fields):
                        for ((b, _), dpsm) in self._dpsms.items():
                            if b != bank:
                                continue

                            if not dpsm.update_state():
                                logger.warning(f"DPSM invalid config: {dpsm}")
                    elif address.includes(
                        self.mem_map.SCS0_ApplyTriggers.ApplyDPInitLane.address
                    ):
                        if self._apply_dpinit():
                            self._init_dpsms()
