from enum import Enum
import logging

from .eeprom import consts, XcvrEEPROM


logger = logging.getLogger(__name__)


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

    def __init__(self, eeprom: XcvrEEPROM, dpid: int) -> None:
        self._eeprom = eeprom
        self._dpid = dpid

        self._lanemask = [0] * 8
        self._appsels = [0] * 8
        self._explicit_controls = [0] * 8

        self._appsel = 0
        self._state = self.State.Unknown

    def add_lane(self, idx: int, appsel: int, explicit_control: bool) -> None:
        self._lanemask[idx] = 1
        self._appsels[idx] = appsel
        self._explicit_controls[idx] = explicit_control

    def update_state(self) -> bool:
        deinit = self._eeprom.read(consts.DATAPATH_DEINIT_FIELD)
        assert isinstance(deinit, int)
        txdis = self._eeprom.read(consts.TX_DISABLE_FIELD)
        assert isinstance(txdis, int)

        logger.debug(f"{deinit=}, {txdis=}, {self._lanemask=}, {self._appsels=}")

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

            logger.info(f"updating DPSM({self._dpid}) state: {prev_state} -> {state}")
            self._state = state

        return True

    def __str__(self) -> str:
        return f"DPSM({self._dpid}): Lanes: {self._lanemask}, AppSel: {self._appsel}, State: {self._state}"
