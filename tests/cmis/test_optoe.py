import logging
import os

from cmis import MemMap
from cmis.optoe import EEPROM

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def test_eeprom_load():
    filename = os.path.join(os.path.dirname(__file__), "eeprom_hexdump.txt")
    eeprom = EEPROM()

    with open(filename, "r") as f:
        hexdump = f.read()
        eeprom.load(hexdump)

    m = MemMap(eeprom)
    data = eeprom.read(0, 0, 0, 256)
    for f, v in m.decode(0, 0, data):
        logger.debug(f.to_str(value=v))

    assert m.VendorName.value.strip() == "CISCO"
    assert m.SFF8024Identifier.value == m.SFF8024Identifier.QSFP_DD
