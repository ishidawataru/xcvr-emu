import logging

from cmis import (
    DPDeinitLane,
    DPInitPendingLane,
    DPStateHostLane,
    MemMap,
    OutputDisableTx,
)

logger = logging.getLogger(__name__)


class DataPathStateMachine:
    def __init__(self, mem_map: MemMap, dpid: int) -> None:
        self._mem_map = mem_map
        self._dpid = dpid

        self._lanemask = [0] * 8
        self._appsels = [0] * 8
        self._explicit_controls = [0] * 8

        self._appsel = 0
        self._state = DPStateHostLane.DPDEACTIVATED

    def add_lane(self, idx: int, appsel: int, explicit_control: bool) -> None:
        self._lanemask[idx] = 1
        self._appsels[idx] = appsel
        self._explicit_controls[idx] = explicit_control

    def update_state(self) -> bool:
        deinit = self._mem_map.DPDeinitLane
        txdis = self._mem_map.OutputDisableTx

        logger.debug(f"{deinit=}, {txdis=}, {self._lanemask=}, {self._appsels=}")

        lanes = [i for i, v in enumerate(self._lanemask) if v]
        appsels = [self._appsels[i] for i in lanes]
        if len(appsels) == 0:
            return False

        all_same = all(x == appsels[0] for x in appsels)
        if not all_same:
            return False

        deinits = [deinit[i].value for i in lanes]
        all_same = all(x == deinits[0] for x in deinits)
        if not all_same:
            self._deinit = True
            return False

        txdiss = [txdis[i].value for i in lanes]
        all_same = all(x == txdiss[0] for x in txdiss)
        if not all_same:
            self._txdis = True
            return False

        self._appsel = appsels[0]
        deinit = deinits[0]
        txdis = txdiss[0]

        logger.info(f"{deinit=}, {txdis=}, {lanes=}, {appsels=}")

        prev_state = self._state

        state = DPStateHostLane.DPINITIALIZED
        if deinit == DPDeinitLane.DEINITIALIZE:
            state = DPStateHostLane.DPDEINIT
        elif txdis == OutputDisableTx.DISABLED:
            state = DPStateHostLane.DPACTIVATED

        if state != prev_state:
            for i in lanes:
                self._mem_map.DPStateHostLane[i].value = state
                if state != DPStateHostLane.DPACTIVATED:
                    self._mem_map.DPInitPendingLane[i].value = (
                        DPInitPendingLane.NOT_PENDING
                    )
                    # flag down DP Pending

            logger.info(f"updating DPSM({self._dpid}) state: {prev_state} -> {state}")
            self._state = state

        return True

    def __str__(self) -> str:
        return f"DPSM({self._dpid}): Lanes: {self._lanemask}, AppSel: {self._appsel}, State: {self._state}"
