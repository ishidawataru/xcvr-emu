import pytest
from xcvr_emu.eeprom import EEPROM

from xcvr_emu.proto.emulator_pb2 import ReadRequest, WriteRequest


@pytest.fixture
def eeprom():
    return EEPROM()


def test_eeprom_read(eeprom: EEPROM):
    req = ReadRequest(index=0, bank=0, offset=0, page=0, length=1)
    assert eeprom.Read(req).data == bytearray([0x0])

def test_eeprom_write(eeprom):
    req = WriteRequest(index=0, bank=0, page=0, offset=0, length=1, data=bytes([0xAA]))
    eeprom.Write(req)
    req = ReadRequest(index=0, bank=0, offset=0, page=0, length=1)
    assert eeprom.Read(req).data == bytearray([0xAA])
