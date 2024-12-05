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
