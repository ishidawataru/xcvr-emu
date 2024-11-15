from .sonic_xcvr.xcvr_eeprom import XcvrEeprom
from .sonic_xcvr.fields.xcvr_field import (
    CodeRegField,
    NumberRegField,
    RegBitsField,
    StringRegField,
)

import struct
from types import SimpleNamespace
from ..proto.emulator_pb2 import ReadRequest, WriteRequest
from typing import Dict, Tuple, Union, Protocol


def regFieldEncode(self, val: int | float, raw_state: bytes = b"") -> bytearray:
    bitmask = self.get_bitmask()
    if not bitmask:
        return bytearray(struct.pack(self.format, val))
    assert raw_state is not None
    raw_state = struct.unpack(self.format, raw_state)[0]
    val = ((val << self.start_bitpos) & bitmask) | (raw_state & ~bitmask)
    return bytearray(struct.pack(self.format, val))


def codeRegFieldEncode(self, val: int, raw_state: bytes = b"") -> bytearray:
    if val not in self.code_dict:
        raise ValueError(
            f"Invalid code {val}for field {self.name}. Valid codes are {self.code_dict.keys()}"
        )
    return regFieldEncode(self, val, raw_state)


CodeRegField.encode = codeRegFieldEncode  # type: ignore
CodeRegField.read_before_write = lambda _: True  # type: ignore

StringRegField.encode = lambda self, val, raw_state=None: bytearray(val.encode())  # type: ignore


def numberRegFieldEncode(self, val: int | float, raw_state: bytes = b"") -> bytearray:
    if self.scale is not None:
        return bytearray(struct.pack(self.format, int(val * self.scale)))
    return regFieldEncode(self, val, raw_state)


NumberRegField.encode = numberRegFieldEncode  # type: ignore
NumberRegField.read_before_write = lambda _: True  # type: ignore


def regBitsFieldEncode(self, val: int, raw_value: bytes = b"") -> bytearray:
    assert raw_value is not None
    val = val & ((1 << self.size) - 1)
    byte = raw_value[0]
    byte &= ~self.bitmask
    byte |= val << self.bitpos
    return bytearray([byte])


RegBitsField.encode = regBitsFieldEncode  # type: ignore


class RawEEPROM:
    def __init__(self) -> None:
        self.lower_page: bytearray = bytearray(128)
        self.higher_pages: Dict[Tuple[int, int], bytearray] = (
            {}
        )  # key: (bank, page), value: b"" * 128

    def Read(self, req: ReadRequest) -> SimpleNamespace:
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

        full_page = self.lower_page + higher_page

        value = full_page[offset : offset + length]
        return SimpleNamespace(data=value)

    def Write(self, req: WriteRequest) -> bool:
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

        full_page = self.lower_page + self.higher_pages[key]

        full_page = full_page[:offset] + data + full_page[offset + length :]

        self.lower_page, self.higher_pages[key] = full_page[:128], full_page[128:]

        return True


class HasDataField(Protocol):
    data: bytes


class ConnInterface(Protocol):
    def Read(self, req: ReadRequest) -> HasDataField: ...

    def Write(self, req: WriteRequest) -> bool: ...


class XcvrEEPROM:
    def __init__(
        self, index: int, conn: ConnInterface, mem_map: Dict[str, Tuple[int, int, int]]
    ):
        def read_eeprom(offset: int, length: int) -> bytes:
            # convert optoe offset to SFF page and offset
            # optoe maps the SFF 2D address to a linear address
            page = offset // 128
            if page > 0:
                page = page - 1

            if offset > 128:
                offset = (offset % 128) + 128

            req = ReadRequest(
                index=index, bank=0, offset=offset, page=page, length=length, force=True
            )

            data = conn.Read(req).data
            print(
                f"read: index; {index}, bank: {req.bank}, page: {req.page:02X}h, offset: {req.offset}, length: {req.length}, data: {data if len(data) != 1 else bin(data[0])}"
            )
            return data

        def write_eeprom(offset: int, length: int, write_buffer: bytearray) -> bool:
            # convert optoe offset to SFF page and offset
            # optoe maps the SFF 2D address to a linear address
            page = offset // 128
            if page > 0:
                page = page - 1

            if offset > 128:
                offset = (offset % 128) + 128

            data = bytes(write_buffer)
            req = WriteRequest(
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

        self.index: int = index

        self._read = read_eeprom
        self._write = write_eeprom

        self._eeprom = XcvrEeprom(read_eeprom, write_eeprom, mem_map)

    def read(self, name: str) -> dict:
        return self._eeprom.read(name)

    def write(self, name: str, data: Union[int, float, str, bytearray]) -> bool:
        return self._eeprom.write(name, data)
