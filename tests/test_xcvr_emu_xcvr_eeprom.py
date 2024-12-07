import pytest
from xcvr_emu.eeprom import RawEEPROM, XcvrEEPROM, CmisMemMap, consts


@pytest.fixture
def eeprom():
    return XcvrEEPROM(0, RawEEPROM(), CmisMemMap())


def test_eeprom_read(eeprom: XcvrEEPROM):
    res = eeprom.read(consts.ADMIN_INFO_FIELD)
    assert isinstance(res, dict)
    assert consts.APPLS_ADVT_FIELD in res


def test_eeprom_write(eeprom: XcvrEEPROM):
    assert eeprom.read(consts.DATAPATH_DEINIT_FIELD) == 0x00
    assert eeprom.write(consts.DATAPATH_DEINIT_FIELD, 0xFF)
    assert eeprom.read(consts.DATAPATH_DEINIT_FIELD) == 0xFF
