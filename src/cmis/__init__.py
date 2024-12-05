from .field import Field, Group, RangeGroup, EEPROM, Address
from .cmis import CMIS_EXPORTS
from .cmis import *  # noqa


class Page(Address):
    def __init__(self, page: int):
        super().__init__(page)


__all__ = [
    "Field",
    "Group",
    "RangeGroup",
    "EEPROM",
    "Address",
    "Page",
] + CMIS_EXPORTS
