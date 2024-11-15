from .eeprom import RawEEPROM, XcvrEEPROM

from .sonic_xcvr.codes.public import cmis as cmis_codes
from .sonic_xcvr.mem_maps.public.cmis import CmisMemMap as mem_map

from .sonic_xcvr.fields import consts

class CmisMemMap(mem_map):
    def __init__(self):
        codes = cmis_codes.CmisCodes
        super().__init__(codes)
