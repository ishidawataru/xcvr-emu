import re

from ..field import EEPROM as BaseEEPROM
from ..cmis import MemMap

OPTOE_PAGE_SIZE = 128
OPTOE_NON_BANKED_PAGES = 16  # page 00h-0Fh are not banked
OPTOE_BANKED_PAGE_SIZE = 240  # page 10h-FFh are banked


def to_linear(bank: int, page: int, offset: int) -> int:
    if page < OPTOE_NON_BANKED_PAGES:
        bank = 0
    if offset < OPTOE_PAGE_SIZE:
        page = 0

    if bank == 0:
        return page * OPTOE_PAGE_SIZE + offset

    linear = (OPTOE_BANKED_PAGE_SIZE * bank + 1) * OPTOE_PAGE_SIZE
    linear += (page - OPTOE_NON_BANKED_PAGES) * OPTOE_PAGE_SIZE
    linear += offset
    return linear


def from_linear(offset: int) -> tuple[int, int, int]:
    if offset < OPTOE_PAGE_SIZE:
        return 0, 0, offset

    page = (offset // OPTOE_PAGE_SIZE) - 1
    if page < OPTOE_NON_BANKED_PAGES:
        return 0, page, offset

    # page > 0x0F
    page = page - OPTOE_NON_BANKED_PAGES
    bank = page // OPTOE_BANKED_PAGE_SIZE

    return bank, page + OPTOE_NON_BANKED_PAGES, offset % OPTOE_PAGE_SIZE


class EEPROM(BaseEEPROM):
    def load(self, hexdump: str):
        lines = hexdump.strip().split("\n")

        pattern = re.compile(
            r"^(?P<address>[0-9a-fA-F]+)\s+(?P<data>(([0-9a-fA-F]+)\s+)+)"
        )

        for line in lines:
            line = line.strip()
            match = pattern.match(line)
            if match is None:
                continue
            address = match.group("address")
            data = match.group("data")
            data = bytes(int(v, 16) for v in data.split(" ") if v != "")
            bank, page, offset = from_linear(int(address, 16))
            self.write(bank, page, offset, len(data), data)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Parse a hexdump string.")
    parser.add_argument("filename", type=str, help="The hexdump string to parse.")

    args = parser.parse_args()

    eeprom = EEPROM()

    with open(args.filename, "r") as file:
        hexdump = file.read()
        eeprom.load(hexdump)

    m = MemMap(eeprom)
    data = eeprom.read(0, 0, 0, 256)
    for f, v in m.decode(0, 0, data):
        print(f.to_str(value=v))
