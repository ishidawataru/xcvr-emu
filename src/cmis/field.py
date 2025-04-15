import logging
from enum import Enum
from typing import Protocol, Type

from .base import Address, Field as BaseField, Group as BaseGroup, MemMap

logger = logging.getLogger(__name__)


class MemoryAccessor(Protocol):
    def read(self, bank: int, page: int, offset: int, length: int) -> bytes: ...

    def write(
        self, bank: int, page: int, offset: int, length: int, data: bytes
    ) -> None: ...


class EEPROM:
    def __init__(self, name: str | None = "") -> None:
        self.name = name
        self.prefix = f"{self.name}: " if self.name else ""
        self.lower_page: bytearray = bytearray(128)
        self.higher_pages: dict[
            tuple[int, int], bytearray
        ] = {}  # key: (bank, page), value: b"" * 128

    def read(self, bank: int, page: int, offset: int, length: int) -> bytes:
        if page < 0x10:  # pages under 0x10 are not banked
            bank = 0

        key = (bank, page)

        if key not in self.higher_pages:
            self.higher_pages[key] = bytearray(128)

        higher_page = self.higher_pages[key]

        full_page = self.lower_page + higher_page

        data = full_page[offset : offset + length]
        logger.debug(
            self.prefix
            + f"Reading from {bank=}, {page=}, {offset=}, {length=} -> data={int.from_bytes(data, 'big'):0b}"
        )
        return bytes(data)

    def write(
        self, bank: int, page: int, offset: int, length: int, data: bytes
    ) -> None:
        logger.debug(
            self.prefix
            + f"Writing to {bank=}, {page=}, {offset=}, {length=}, data={int.from_bytes(data, 'big'):0b}"
        )
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


class BaseMemMap(MemMap):
    def __init__(
        self,
        remote: MemoryAccessor = EEPROM("remote"),
        local: MemoryAccessor = EEPROM("local"),
        no_default=False,
        table_filter=None,
    ) -> None:
        super().__init__(no_default=no_default, table_filter=table_filter)
        self.remote = remote
        self.local = local
        self.bank = 0

    def read(self, bank: int, page: int, offset: int, length: int) -> bytes:
        return self.remote.read(bank, page, offset, length)

    def write(
        self, bank: int, page: int, offset: int, length: int, data: bytes
    ) -> None:
        return self.remote.write(bank, page, offset, length, data)

    def _search_group(self, name: str) -> BaseGroup:
        return self.search_by_name(name, include_groups=True, include_fields=False)

    def _search_field(self, name: str) -> BaseField:
        return self.search_by_name(name, include_groups=False, include_fields=True)

    def _update_bits(self, num: int, start: int, length: int, value: int):
        mask = ((1 << length) - 1) << start
        num_cleared = num & ~mask
        value_shifted = (value << start) & mask
        logger.debug(f"{num_cleared=:0b}, {value_shifted=:0b}, {mask=:0b}")
        return num_cleared | value_shifted

    def _sync(self, addr: Address, src: MemoryAccessor, dst: MemoryAccessor) -> None:
        src_value = src.read(
            self.bank,
            addr.page,
            addr.start_byte,
            addr.byte_size,
        )

        if addr.bit:
            dst_value = dst.read(
                self.bank,
                addr.page,
                addr.start_byte,
                addr.byte_size,
            )
            src_int = int.from_bytes(src_value, "big")
            dst_int = int.from_bytes(dst_value, "big")
            start_bit = addr.start_bit % 8
            src_int = self._update_bits(
                dst_int, start_bit, addr.size, src_int >> start_bit
            )
            src_value = src_int.to_bytes(addr.byte_size, "big")

        dst.write(
            self.bank,
            addr.page,
            addr.start_byte,
            addr.byte_size,
            src_value,
        )

    def fetch(self, addr: Address) -> None:
        self._sync(addr, self.remote, self.local)

    def store(self, addr: Address) -> None:
        self._sync(addr, self.local, self.remote)

class ConditionalEnum:
    EnumClasses: None | list[Type[Enum]] = None

    def __init__(
        self, mem_map: BaseMemMap, field: BaseField
    ):
        self.mem_map = mem_map
        self.field = field
        values = self.field.fields.get("Values")
        assert isinstance(values, list), f"{self.field.name}: Values must be a list"
        self.values: list[dict] = values
        assert self.EnumClasses and len(self.EnumClasses) == len(self.values), f"{self.field.name}: EnumClasses must be the same length as Values"

    def value(self, value: int) -> Enum | int:
        for i, v in enumerate(self.values):
            if v["When"][1](self.mem_map):
                return self.EnumClasses[i](value) # type: ignore
        else:
            return  value

class Field:
    EnumClass: None | Type[Enum] = None
    ConditionalEnumClass: None | Type[ConditionalEnum] = None

    def __init__(
        self, mem_map: BaseMemMap, field: BaseField, index: int | None = None
    ) -> None:
        self.mem_map = mem_map
        self.field = field
        self.index = index
        self.value_type = self.field.fields.get("ValueType")
        if self.value_type is str:
            assert self.size % 8 == 0, "ASCIIField size must be a multiple of 8"
        self.conditional_enum = self.ConditionalEnumClass(
            mem_map, field
        ) if self.ConditionalEnumClass else None

    @property
    def name(self) -> str:
        return self.field.name

    @property
    def address(self) -> Address:
        return self.field.address

    @property
    def size(self) -> int:
        return self.field.address.size

    def fetch(self) -> None:
        logger.debug(f"Fetching {self.name}, {self.address}")
        self.mem_map.fetch(self.address)

    def store(self) -> None:
        logger.debug(f"Storing {self.name}, {self.address}")
        self.mem_map.store(self.address)

    @property
    def value(self) -> int | str | Enum:
        self.fetch()
        return self.lvalue

    @value.setter
    def value(self, src: int | str | Enum) -> None:
        self.lvalue = src
        self.store()

    @property
    def lvalue(self) -> int | str | Enum:
        value = self.mem_map.local.read(
            self.mem_map.bank,
            self.address.page,
            self.address.start_byte,
            self.address.byte_size,
        )
        v = int.from_bytes(value, "big")
        if self.address.bit is not None:
            start_bit = self.address.start_bit % 8
            v >>= start_bit
            v &= (1 << self.size) - 1
        if self.value_type is str:
            return value.decode("ascii")

        if self.EnumClass:
            e = self.EnumClass(v)
            logger.debug(f"Get {self.name}({self.address}): {e}({e.value})")
            return e
        elif self.conditional_enum:
            d = self.conditional_enum.value(v)
            logger.debug(f"Get {self.name}({self.address}): {d}")
            return d

        logger.debug(f"Get {self.name}({self.address}): {v:0b}")
        return v

    @lvalue.setter
    def lvalue(self, src: int | str | Enum) -> None:
        logger.debug(f"Setting {self.name}({self.address}) to {src}")

        if isinstance(src, Enum):
            src = src.value

        if self.value_type is str:
            assert isinstance(src, str), f"{self.name}: Value must be a string"
            src_value = src.encode("ascii")
            assert len(src_value) <= self.address.byte_size, (
                f"{self.name}: Value too long"
            )
        else:
            assert isinstance(src, int), f"{self.name}: Value must be an integer"
            src_int = src
            if self.address.bit is not None:
                dst = self.mem_map.local.read(
                    self.mem_map.bank,
                    self.address.page,
                    self.address.start_byte,
                    self.address.byte_size,
                )
                dst_int = int.from_bytes(dst, "big")
                start_bit = self.address.start_bit % 8
                logger.debug(f"{dst_int=}, {start_bit=}, {self.size=}, {src_int=}")
                src_int = self.mem_map._update_bits(
                    dst_int, start_bit, self.size, src_int
                )
                logger.debug(f"{src_int=}")
            src_value = src_int.to_bytes(self.address.byte_size, "big")

        self.mem_map.local.write(
            self.mem_map.bank,
            self.address.page,
            self.address.start_byte,
            self.address.byte_size,
            src_value,
        )

    def set_value_from_str(self, value: str):
        if self.value_type is str:
            self.value = value
        else:
            try:
                vint = int(value, 0)
                self.value = vint
            except ValueError:
                if self.EnumClass:
                    self.value = self.EnumClass[value]
                else:
                    raise ValueError(f"Invalid value: {value}")

    def to_str(self, value: int | str) -> str:
        values = self.field.fields.get("Values")
        if values and value in values:
            return values[value][1]

        return str(value)


class Group(Field):
    def __init__(
        self, mem_map: BaseMemMap, field: BaseField, index: int | None = None
    ) -> None:
        super().__init__(mem_map, field, index)
        self.subfields = {f.original_name: f for f in field.subfields}


class RangeGroup(Field):
    def __len__(self) -> int:
        return len(self.field.subfields)
