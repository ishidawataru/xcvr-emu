import logging

from cmis import MemMap

def test_mem_map(caplog):
    caplog.set_level(logging.DEBUG)
    m = MemMap()

    assert len(m.ApplicationDescriptor) == 15
    app = m.ApplicationDescriptor[2]
    assert app.HostInterfaceID.field.name == "HostInterfaceID3"
    assert str(app.HostInterfaceID.field.address) == "00h:94"
    app = m.ApplicationDescriptor[12]
    assert app.HostInterfaceID.field.name == "HostInterfaceID13"

    v = m.ACS_RxControls
    assert len(v.CDREnableRx) == 8
    for vv in v.CDREnableRx:
        vv
    assert v.CDREnableRx[0].field.name == "ACS_CDREnableRx1"

    v = m.MediaLaneUnsupportedLane
    assert len(v) == 8
    assert v.name == "MediaLaneUnsupportedLane"
    assert str(v.address) == "00h:210"
    assert v.size == 8  # 8bits
    assert v[0].name == "MediaLaneUnsupportedLane1"
    assert v[0].size == 1  # 1bit

    v = m.OutputStatusRx
    assert len(v) == 8
    assert str(v.address) == "11h:132"
    assert str(v[0].address) == "11h:132.0"

    for lane in m.ConfigStatusLane:
        print(lane.address)

    m.ForcedSquelchTxSupported.SUPPORTED

    assert m.CmisRevision.Major.value == 0
    m.CmisRevision.Major.value = 5
    assert m.CmisRevision.Major.value == 5

    assert m.CmisRevision.Minor.value == 0
    m.CmisRevision.Minor.value = 3
    assert m.CmisRevision.Minor.value == 3

    m.CmisRevision.Major.lvalue = 6
    assert m.CmisRevision.Major.lvalue == 6

    m.CmisRevision.fetch()

    assert m.CmisRevision.Major.value == 5
    assert m.CmisRevision.Minor.value == 3


def test_with_bank(caplog):
    caplog.set_level(logging.DEBUG)
    m = MemMap()

    # accessing banked registers

    with m.with_bank(1):
        assert m.ACS_DPConfigLane[0].value == 0
        m.ACS_DPConfigLane[0].value = 1

    assert m.ACS_DPConfigLane[0].value == 0

    with m.with_bank(1):
        assert m.ACS_DPConfigLane[0].value == 1

    with m.with_bank(2):
        assert m.ACS_DPConfigLane[0].value == 0

    # accessing non-banked registers

    assert m.LowPwrRequestSW.value == m.LowPwrRequestSW.NO_REQUEST
    m.LowPwrRequestSW.value = m.LowPwrRequestSW.LOW_POWER_MODE

    with m.with_bank(1):
        assert m.LowPwrRequestSW.value == m.LowPwrRequestSW.LOW_POWER_MODE

    with m.with_bank(2):
        assert m.LowPwrRequestSW.value == m.LowPwrRequestSW.LOW_POWER_MODE

    with m.with_bank(3):
        m.LowPwrRequestSW.value = m.LowPwrRequestSW.NO_REQUEST

    assert m.LowPwrRequestSW.value == m.LowPwrRequestSW.NO_REQUEST

    with m.with_bank(1):
        assert m.LowPwrRequestSW.value == m.LowPwrRequestSW.NO_REQUEST

    with m.with_bank(2):
        assert m.LowPwrRequestSW.value == m.LowPwrRequestSW.NO_REQUEST

def test_conditional_register(caplog):
    caplog.set_level(logging.DEBUG)
    m = MemMap()

    status = m.CdbStatus[0]
    assert status.CdbCommandResult.when() == "cdb-success"
    # COMPLETED, CAPTURED and UNKNOWN_CMDID are the same value
    assert status.CdbCommandResult.COMPLETED.value ==  status.CdbCommandResult.CAPTURED.value

    status.CdbCommandResult.value = status.CdbCommandResult.COMPLETED # cdb-success

    assert status.CdbCommandResult.value == status.CdbCommandResult.COMPLETED
    assert status.CdbCommandResult.value != status.CdbCommandResult.CAPTURED
    assert status.CdbCommandResult.value != status.CdbCommandResult.UNKNOWN_CMDID

    status.CdbIsBusy.value = status.CdbIsBusy.BUSY
    assert status.CdbCommandResult.when() == "cdb-in-progress"

    assert status.CdbCommandResult.value != status.CdbCommandResult.COMPLETED
    assert status.CdbCommandResult.value == status.CdbCommandResult.CAPTURED
    assert status.CdbCommandResult.value != status.CdbCommandResult.UNKNOWN_CMDID

    status.CdbIsBusy.value = status.CdbIsBusy.IDLE
    status.CdbHasFailed.value = status.CdbHasFailed.FAILED
    assert status.CdbCommandResult.when() == "cdb-failed"

    assert status.CdbCommandResult.value != status.CdbCommandResult.COMPLETED
    assert status.CdbCommandResult.value != status.CdbCommandResult.CAPTURED
    assert status.CdbCommandResult.value == status.CdbCommandResult.UNKNOWN_CMDID

    status.CdbCommandResult.value = status.CdbCommandResult.INCOMPATIBLE_STATUS
    assert status.CdbCommandResult.value == status.CdbCommandResult.INCOMPATIBLE_STATUS

    status.CdbHasFailed.value = status.CdbHasFailed.SUCCESS

    assert status.CdbCommandResult.value != status.CdbCommandResult.INCOMPATIBLE_STATUS

    # if no matching enum value in the current state, the value is int
    assert status.CdbCommandResult.value == 0x07
