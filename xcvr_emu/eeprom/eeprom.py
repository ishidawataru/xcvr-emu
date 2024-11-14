from sonic_platform_base.sonic_xcvr.xcvr_eeprom import XcvrEeprom
from sonic_platform_base.sonic_xcvr.fields.xcvr_field import (
    CodeRegField,
    NumberRegField,
    RegBitsField,
    StringRegField,
)

import struct
from types import SimpleNamespace

import emulator_pb2 as pb2


def regFieldEncode(self, val, raw_state=None):
    bitmask = self.get_bitmask()
    if not bitmask:
        return bytearray(struct.pack(self.format, val))

    raw_state = struct.unpack(self.format, raw_state)[0]
    val = ((val << self.start_bitpos) & bitmask) | (raw_state & ~bitmask)
    return bytearray(struct.pack(self.format, val))


def codeRegFieldEncode(self, val, raw_state=None):
    if val not in self.code_dict:
        raise ValueError(f"Invalid code {val}for field {self.name}. Valid codes are {self.code_dict.keys()}")
    return regFieldEncode(self, val, raw_state)


CodeRegField.encode = codeRegFieldEncode
CodeRegField.read_before_write = lambda _: True

StringRegField.encode = lambda self, val, raw_state=None: bytearray(val.encode())


def numberRegFieldEncode(self, val, raw_state=None):
    if self.scale is not None:
        return bytearray(struct.pack(self.format, int(val * self.scale)))
    return regFieldEncode(self, val, raw_state)


NumberRegField.encode = numberRegFieldEncode
NumberRegField.read_before_write = lambda _: True


def regBitsFieldEncode(self, val, raw_value=None):
    assert raw_value is not None
    val = val & ((1 << self.size) - 1)
    byte = raw_value[0]
    byte &= ~self.bitmask
    byte |= val << self.bitpos
    return bytearray([byte])


RegBitsField.encode = regBitsFieldEncode


class RawEEPROM:
    def __init__(self):
        self.lower_page = bytearray(128)
        self.higher_pages = {}  # key: (bank, page), value: b"" * 128

    def Read(self, req):
        bank = req.bank
        page = req.page
        offset = req.offset
        length = req.length

        if page < 0x10:  # pages under 0x10 are not banked
            bank = 0

        key = (bank, page)

        if key not in self.higher_pages:
            self.higher_pages[key] = bytearray(128)

        higher_page = self.higher_pages[key]

        page = self.lower_page + higher_page

        value = page[offset : offset + length]
        return SimpleNamespace(data=value)

    def Write(self, req):
        bank = req.bank
        page = req.page
        offset = req.offset
        data = req.data
        length = req.length

        # pad data with 0s if it is shorter than length
        data = bytearray(data + b"\x00" * (length - len(data)))

        if page < 0x10:  # pages under 0x10 are not banked
            bank = 0

        key = (bank, page)

        if key not in self.higher_pages:
            self.higher_pages[key] = bytearray(128)

        page = self.lower_page + self.higher_pages[key]

        page = page[:offset] + data + page[offset + length :]

        self.lower_page = page[:128]
        self.higher_pages[key] = page[128:]


class XcvrEEPROM:
    def __init__(self, index, conn, mem_map):
        def read_eeprom(offset, length):
            # convert optoe offset to SFF page and offset
            # optoe maps the SFF 2D address to a linear address
            page = offset // 128
            if page > 0:
                page = page - 1

            if offset > 128:
                offset = (offset % 128) + 128

            req = pb2.ReadRequest(
                index=index, bank=0, offset=offset, page=page, length=length, force=True
            )

            data = conn.Read(req).data
            print(
                f"read: index; {index}, bank: {req.bank}, page: {req.page:02X}h, offset: {req.offset}, length: {req.length}, data: {data if len(data) != 1 else bin(data[0])}"
            )
            return data

        def write_eeprom(offset, length, write_buffer: bytearray):
            # convert optoe offset to SFF page and offset
            # optoe maps the SFF 2D address to a linear address
            page = offset // 128
            if page > 0:
                page = page - 1

            if offset > 128:
                offset = (offset % 128) + 128

            data = bytes(write_buffer)
            req = pb2.WriteRequest(
                index=index,
                bank=0,
                page=page,
                offset=offset,
                length=length,
                data=data,
            )

            print(
                f"write: index: {index}, bank: {req.bank}, page: {req.page:02X}h, offset: {req.offset}, length: {req.length}, data: {data if len(data) > 1 else bin(data[0])}"
            )

            return conn.Write(req)

        self.index = index

        self._read = read_eeprom
        self._write = write_eeprom

        self._eeprom = XcvrEeprom(read_eeprom, write_eeprom, mem_map)

    def read(self, name):
        return self._eeprom.read(name)

    def write(self, name, data):
        return self._eeprom.write(name, data)
