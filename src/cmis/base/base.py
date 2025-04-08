import logging
import os
import re
from copy import deepcopy
from typing import Generator, ContextManager

logger = logging.getLogger(__name__)


def swap_if_needed(v):
    if isinstance(v, tuple):
        assert v[0] != v[1]
        return (v[1], v[0]) if v[0] > v[1] else v
    return v


class Address:
    def __init__(
        self,
        page: int,
        offset: int | tuple[int, int] | None = None,
        bit: int | tuple[int, int] | None = None,
    ) -> None:
        self.page = page

        if offset is None:
            assert bit is None
            offset = (0, 255)

        self.offset = swap_if_needed(offset)
        self.bit = swap_if_needed(bit)

        if isinstance(self.offset, int) and isinstance(self.bit, tuple):
            assert (self.bit[1] - self.bit[0]) < 8, f"bit range too large: {self.bit}"
        elif isinstance(self.offset, tuple) and isinstance(self.bit, tuple):
            assert (self.bit[1] - self.bit[0]) < (
                self.offset[1] - self.offset[0] + 1
            ) * 8, f"bit range too large: {self.bit}"

    @classmethod
    def from_str(cls, s: str):
        pattern = (
            r"(?P<page>[0-9a-f]{1,2})h"
            r"(?::"
            r"(?P<start_offset>[0-9]{1,3})"
            r"(?:-(?P<end_offset>[0-9]{1,3}))?"
            r"(?:\."
            r"(?P<start_bit>[0-9]{1,3})"
            r"(?:-(?P<end_bit>[0-9]{1,3}))?"
            r")?"
            r")?"
        )
        match = re.match(pattern, s, re.IGNORECASE)
        if not match:
            raise ValueError(f"Invalid address format: {s}")

        page = int(match.group("page"), 16)
        start_offset = match.group("start_offset")
        if start_offset:
            end_offset = match.group("end_offset")
            offset: tuple[int, int] | int | None = (
                (int(start_offset), int(end_offset))
                if end_offset
                else int(start_offset)
            )

            start_bit = match.group("start_bit")
            if start_bit:
                end_bit = match.group("end_bit")
                bit: tuple[int, int] | int | None = (
                    (int(start_bit), int(end_bit)) if end_bit else int(start_bit)
                )
            else:
                bit = None
        else:
            offset = None
            bit = None

        return cls(page, offset, bit)

    def to_canonical(self) -> "Address":
        return Address.from_str(str(self))

    @property
    def size(self) -> int:
        """Return the size of the field in bits"""
        if self.bit is not None:
            if isinstance(self.bit, tuple):
                return self.bit[1] - self.bit[0] + 1
            return 1
        if self.offset is not None:
            if isinstance(self.offset, tuple):
                return (self.offset[1] - self.offset[0] + 1) * 8
            return 8
        return 128

    @property
    def byte_size(self) -> int:
        """How many bytes are needed to store the field"""
        if isinstance(self.bit, tuple):
            return (self.bit[1] // 8) - (self.bit[0] // 8) + 1
        return (self.size + 7) // 8

    @property
    def start_bit(self) -> int:
        return self.bit[0] if isinstance(self.bit, tuple) else self.bit

    @property
    def start_byte(self):
        if self.bit is None:
            return self.offset if isinstance(self.offset, int) else self.offset[0]

        return (
            self.offset
            if isinstance(self.offset, int)
            else self.offset[0] + self.bit[0] // 8
        )

    def __str__(self):
        assert self.page is not None
        page = f"{self.page:02X}"

        if isinstance(self.offset, tuple):
            offset = f"{self.offset[0]}-{self.offset[1]}"
        else:
            offset = f"{self.offset}"

        if self.bit is None:
            return f"{page}h:{offset}"

        if isinstance(self.bit, tuple):
            if isinstance(self.offset, tuple):
                # generate canonical address form when both offset and bit are ranges
                # e.g) 0x00h:0-7.8-14 = 0x00h:1.0-6

                byte_begin = self.bit[0] // 8
                byte_end = self.bit[1] // 8
                if byte_begin == byte_end:
                    offset = f"{self.offset[0] + byte_begin}"
                else:
                    offset = (
                        f"{self.offset[0] + byte_begin}-{self.offset[0] + byte_end}"
                    )
                    if (byte_end - byte_begin + 1) * 8 == self.size:
                        return f"{page}h:{offset}"
                start = self.bit[0] - byte_begin * 8
                end = self.bit[1] - byte_begin * 8
            else:
                start = self.bit[0]
                end = self.bit[1]

            if start == 0 and end == 7:
                return f"{page}h:{offset}"

            bit = f"{start}-{end}"
        else:
            bit = f"{self.bit}"

        return f"{page}h:{offset}.{bit}"

    def __lt__(self, other):
        assert self.page is not None
        assert other.page is not None
        page = self.page
        other_page = other.page

        if page != other_page:
            return page < other_page

        def get_start(value, offset_for_range=0):
            if isinstance(value, tuple):
                value = value[0]
            elif isinstance(value, range):
                value = value.start - offset_for_range
            elif value is None:
                value = 0
            else:
                value = value

            return value

        offset = get_start(self.offset)
        other_offset = get_start(other.offset)

        if offset != other_offset:
            return offset < other_offset

        bit = 0 if self.bit is None else self.bit
        other_bit = 0 if other.bit is None else other.bit

        bit = get_start(bit, 1)
        other_bit = get_start(other_bit, 1)

        if bit == other_bit:
            return self.size > other.size
        else:
            return bit < other_bit

    def __eq__(self, other):
        # use the canonical form for comparison
        return str(self) == str(other)

    def overraps(self, other):
        if other.page != self.page:
            return False

        offset = (
            self.offset
            if isinstance(self.offset, tuple)
            else (self.offset, self.offset)
        )
        other_offset = (
            other.offset
            if isinstance(other.offset, tuple)
            else (other.offset, other.offset)
        )

        if offset[0] > other_offset[1] or offset[1] < other_offset[0]:
            return False

        if self.bit is None or other.bit is None:
            return True

        bit = self.bit if isinstance(self.bit, tuple) else (self.bit, self.bit)
        other_bit = (
            other.bit if isinstance(other.bit, tuple) else (other.bit, other.bit)
        )

        if bit[0] > other_bit[1] or bit[1] < other_bit[0]:
            return False

        return True

    def includes(self, other):
        if other.page != self.page:
            return False

        offset = (
            self.offset
            if isinstance(self.offset, tuple)
            else (self.offset, self.offset)
        )
        other_offset = (
            other.offset
            if isinstance(other.offset, tuple)
            else (other.offset, other.offset)
        )

        if not (offset[0] <= other_offset[0] and offset[1] >= other_offset[1]):
            return False

        if self.bit is None:
            return True

        bit = self.bit if isinstance(self.bit, tuple) else (self.bit, self.bit)
        other_bit = (
            other.bit if isinstance(other.bit, tuple) else (other.bit, other.bit)
        )

        if not (bit[0] <= other_bit[0] and bit[1] >= other_bit[1]):
            return False

        return True


class Field:
    def __init__(self, parent_info: dict, fields: dict, is_group=False) -> None:
        self.parent_info = parent_info
        if "Name" in fields:
            self.name = fields["Name"]
        elif "Template" in fields:
            self.name = fields["Template"]

        self.original_name = self.name

        if "Prefix" in parent_info:
            self.name = parent_info["Prefix"] + self.name

        if "Prefix" in fields:
            self.name = fields["Prefix"] + self.name

        if not self.name.isidentifier() and "::" in self.name:
            self.name = self.name.replace("::", "_")

        assert self.name.isidentifier(), f"{self.name} is not a valid python identifier"

        self.subfields: list = []
        self.fields = fields
        self.value: None | int | bytes = None

        if "RangeInfo" in parent_info:
            range_info = parent_info["RangeInfo"]
            try:
                if isinstance(range_info, int):
                    if "SuffixFunc" in fields:
                        self.name += fields["SuffixFunc"](range_info)
                    elif "SuffixFunc" in parent_info:
                        self.name += parent_info["SuffixFunc"](range_info)
                    else:
                        self.name += str(range_info + 1)
                elif isinstance(range_info, tuple):
                    byte, bit = range_info
                    if "SuffixFunc" in fields:
                        self.name += fields["SuffixFunc"](byte, bit)
                    elif "SuffixFunc" in parent_info:
                        self.name += parent_info["SuffixFunc"](byte, bit)
                    else:
                        self.name += f"{byte+1}_{bit+1}"
            except TypeError as e:
                if not is_group:
                    raise
                # this happens when we fail to create a group name for a nested range field
                # give up and use the top level name
                logger.debug(f"{self.name} type error: {e}")

        else:
            if "Suffix" in fields:
                self.name += fields["Suffix"]

            if "Suffix" in parent_info:
                self.name += parent_info["Suffix"]

        # TODO "SubFields" handling
        if "Group" in parent_info:
            parent_info["Group"].add_subfield(self)

        if is_group:
            return

        if len(parent_info["Offsets"]) == 1:
            offset = parent_info["Offsets"][0]
            bit = None
        else:
            offset, bit = self.parent_info["Offsets"]

        self.address = Address(
            self.parent_info["Page"].page_num,
            offset,
            bit,
        ).to_canonical()

    @property
    def group(self):
        return self.parent_info.get("Group", None)

    @property
    def template(self):
        templete = self.fields.get("Template")
        if templete:
            return self.parent_info["Templates"].get(templete)
        return None

    def to_str(
        self,
        with_table: bool = False,
        with_group: bool = False,
        recursive: bool = False,
        value: None | bytes = None,
    ) -> str:
        s = f"{str(self.address):15s}| {self.name}"
        if len(self.subfields) > 0:
            s += f" (Group of {len(self.subfields)})"
            if recursive:
                assert value is not None
                offset = self.address.start_byte
                ss = []
                for f in self.subfields:
                    if isinstance(f.address.offset, int):
                        i = f.address.offset - offset
                        v = value[i].to_bytes(1, "big")
                    elif isinstance(f.address.offset, tuple):
                        v = value[
                            f.address.offset[0]
                            - offset : f.address.offset[1]
                            - offset
                            + 1
                        ]

                    # bit level adjustment will be done in _value_to_str()

                    ss.append(
                        f.to_str(
                            with_table,
                            with_group,
                            recursive,
                            value=v,
                        )
                    )

                s += "\n" + "\n".join(ss)
                return s

        if with_table:
            table = self.parent_info["TableName"]
            s = f" | {table} | {str(self.address):15s}| {self.name}"
        if with_group:
            if "Group" in self.parent_info:
                s += f" | {self.parent_info['Group'].name}"

        if value is not None:
            s += f" | {self._value_to_str(value)}"
        else:
            values = self.fields.get("Values")
            if values:
                if not all(isinstance(v[1], str) for v in values.values()):
                    logger.warning("conditional values? %s", values)
                    s += f" {values}"
                else:
                    values = "|".join(v[1] for v in values.values())
                    values = f"[{values}]"
                s += f" {values}"
        return s

    def __str__(self):
        return self.to_str()

    def _value_to_str(self, value: bytes) -> str:
        value_type = self.fields.get("ValueType")
        if value_type is str:
            return value.decode("ascii")

        vint = int.from_bytes(value, "big")

        if self.address.bit is not None:
            shift = (
                self.address.bit
                if isinstance(self.address.bit, int)
                else self.address.bit[0]
            )

            mask = (
                0b1
                if isinstance(self.address.bit, int)
                else (0b1 << (self.address.bit[1] - self.address.bit[0] + 1)) - 1
            )

            vint = vint >> shift & mask

        values = self.fields.get("Values", {})
        if values:
            for k, v in values.items():
                if vint == k:
                    return f"{v[1]}({vint!r})"
                if isinstance(k, tuple) and k[0] <= vint <= k[1]:
                    return f"{v[1]}({vint!r})"
        return str(vint)

    def describe(self):
        lines = []
        lines.append(f"Name: {self.name}, Address: {str(self.address)}")
        lines.append(f"Type: {self.fields.get('Type')}")
        lines.append(f"Table: {self.parent_info['TableName']}")
        if self.parent_info.get("FileName"):
            lines.append(f"File: {self.parent_info['FileName']}")
        if self.fields.get("Description"):
            lines.append(f"Description: {self.fields.get('Description')}")

        values = self.fields.get("Values")
        if values:
            lines.append("Valid Values:")
            for k, v in values.items():
                lines.append(f"  {k}: {v[1]}")

        if self.subfields:
            lines.append("Subfields:")
            for f in self.subfields:
                lines.append(f"  {f}")

        return "\n".join(lines)


class Group(Field):
    def __init__(self, parent_info: dict, fields: dict) -> None:
        super().__init__(parent_info, fields, is_group=True)

    def add_subfield(self, field: Field):
        self.subfields.append(field)

    @property
    def address(self) -> Address:
        if len(self.subfields) == 0:
            return Address(0, 0, 0)
        #            raise ValueError(f"Group({self.name}) has no subfields")

        self.subfields.sort(key=lambda x: x.address)
        first = self.subfields[0].address
        last = self.subfields[-1].address

        if first.page != last.page:
            raise ValueError(
                f"Group spans multiple pages. {self.name}, {first}, {last}"
            )

        if first.offset != last.offset:
            assert first.bit is None or first.bit == 0 or isinstance(first.bit, tuple)
            assert last.bit is None or last.bit == 7 or isinstance(last.bit, tuple)

            start = first.offset if isinstance(first.offset, int) else first.offset[0]
            end = last.offset if isinstance(last.offset, int) else last.offset[1]

            return Address(first.page, (start, end), None)

        if first.bit is None and last.bit is None:
            return Address(first.page, first.offset, None)

        start = first.bit if isinstance(first.bit, int) else first.bit[0]
        end = last.bit if isinstance(last.bit, int) else last.bit[1]

        if start == 0 and end == 7:
            return Address(first.page, first.offset, None)

        return Address(first.page, first.offset, (start, end))

    @address.setter
    def address(self, value: Address):
        pass


class RangeGroup(Group):
    def __init__(self, parent_info: dict, fields: dict, range: range) -> None:
        super().__init__(parent_info, fields)
        self.range = range


class Template(Group):
    pass


class Page:
    def __init__(self, page_num: int) -> None:
        self.page_num = page_num
        self.fields: list[Field] = []
        self.field_map: dict[str, Field] = {}
        self.group_map: dict[str, Group] = {}
        self.template_map: dict[str, Template] = {}

    def handle_field(self, p: dict, field: dict) -> list[Field]:
        offsets = p["Offsets"]
        assert not isinstance(offsets[-1], range)
        try:
            return [Field(p, field)]
        except AssertionError as e:
            logger.warning(f"Failed to create field:  {e}")
            return []

    def handle_template(self, p: dict, field: dict) -> list[Field]:
        templates = p["Templates"]
        assert field["Template"] in templates, f"Template {field['Template']} not found"

        template = templates[field["Template"]]
        fieldTemplate = all(isinstance(k, str) for k in template)

        if fieldTemplate:
            if "Template" in template:
                assert (
                    len(template) == 1
                ), "Nested field template is only allowed for template renaming"
                assert (
                    template["Template"] in templates
                ), f"Nested field template {template['Template']} not found"
                template = templates[template["Template"]]

            field.update(template)
            return self.handle_field(p, field)

        group = Group(p, field)
        if group.name in self.group_map:
            group = self.group_map[group.name]
        else:
            self.group_map[group.name] = group

        p = p.copy()
        p["Group"] = group

        if "Prefix" in field:
            p["Prefix"] = p.get("Prefix", "") + field["Prefix"]

        if "Suffix" in field:
            p["Suffix"] = field["Suffix"] + p.get("Suffix", "")

        if "SuffixFunc" in field:
            p["SuffixFunc"] = field["SuffixFunc"]

        offsets = p["Offsets"]
        range_templating = isinstance(offsets[-1], tuple)
        if range_templating:
            offset = offsets[-1]
            start, end = swap_if_needed(offset)

            available_space = end - start + 1
            max_ = 0
            for k in template.keys():
                if isinstance(k, tuple):
                    max_ = max(max_, max(k[0], k[1]))
                elif isinstance(k, range):
                    max_ = max(max_, list(k)[-1])
                else:
                    max_ = max(max_, k)
            required_space = max_ + 1
            assert (
                available_space >= required_space
            ), f"Insufficient space for template {field['Template']}. {required_space} required, {available_space} available"

            p["Offsets"] = p["Offsets"][:-1]

            field = {}
            for k, v in template.items():
                if isinstance(k, tuple):
                    k = (k[0] + start, k[1] + start)
                elif isinstance(k, range):
                    k = range(k.start + start, k.stop + start, k.step)
                else:
                    k = k + start
                field[k] = v

        elif len(offsets) == 1:
            field = template.copy()  # bit level template
            assert type(offsets[0]) in [
                int,
                tuple,
            ]  # range is not supported here
        else:
            assert False, "template for a single bit must be a field template"

        self.update(p, field)
        return []

    def update(self, parent_info, field_dict):
        #        table_name = parent_info["TableName"]
        #        if table_name not in self.group_map:
        #            group = Group(parent_info, {"Name": table_name})
        #            self.group_map[table_name] = group
        #        else:
        #            group = self.group_map[table_name]

        pp = parent_info.copy()
        templates = deepcopy(pp.get("Templates", {}))
        for name in (k for k in field_dict.keys() if isinstance(k, str)):
            if name in self.template_map:
                logger.warning("Duplicate template: %s", name)
            field = field_dict[name].copy()
            field["Name"] = name
            self.template_map[name] = Template(pp, field)

            templates[name] = field_dict[name]
        pp["Templates"] = templates

        for offset, field in field_dict.items():
            if isinstance(offset, str):
                continue
            # copy parent_info
            p = pp.copy()
            assert p.get("Page", self) == self
            p["Page"] = self

            if isinstance(offset, range):  # range handling
                if "Template" in field or "Name" in field:
                    group = RangeGroup(p, field, offset)
                    if group.name in self.group_map:
                        group = self.group_map[group.name]
                    else:
                        self.group_map[group.name] = group

                for i, o in enumerate(offset):
                    ppp = p.copy()
                    if group:
                        ppp["Group"] = group
                    if "RangeInfo" in p:
                        logging.warning(f"nested range not recommended: {group.name}")
                    ppp["RangeInfo"] = (
                        i if "RangeInfo" not in p else (p["RangeInfo"], i)
                    )
                    o = o if offset.step == 1 else (o, o + offset.step - 1)
                    self.update(ppp, {o: field})

            else:
                offsets = p.get("Offsets", []).copy()
                offsets.append(offset)
                p["Offsets"] = offsets

                if "Template" in field or "Name" in field:
                    handler = (
                        self.handle_template
                        if "Template" in field
                        else self.handle_field
                    )
                    for f in handler(p, field):
                        self.fields.append(f)
                        if f.name in self.field_map:
                            logger.debug("Duplicate field: %s", f.name)
                        self.field_map[f.name] = f
                else:
                    assert len(offsets) == 1
                    assert type(offsets[0]) in [
                        int,
                        tuple,
                    ]  # range is not supported here
                    self.update(p, field)

        # keep fields sorted by address
        self.fields.sort(key=lambda x: x.address)

    def to_str(self, indent=0, include_groups=False, verbose=False):
        if include_groups:
            fields = self.fields + list(self.group_map.values())
            fields.sort(key=lambda x: x.address)
        else:
            fields = self.fields

        lines = [
            " " * indent + f.to_str(with_group=verbose, with_table=verbose)
            for f in fields
        ]
        return "\n".join(lines)

    def __str__(self):
        return self.to_str()

class BankContext:
    def __init__(self, mem_map: "MemMap", bank: int) -> None:
        self.mem_map = mem_map
        self.bank = bank

    def __enter__(self):
        self.original_bank = self.mem_map.bank
        self.mem_map.bank = self.bank

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mem_map.bank = self.original_bank


class MemMap:
    def register(self, info, filename=""):
        page_num, name, field_dict, description = (
            info["Page"],
            info["Name"],
            info["Table"],
            info["Description"],
        )
        page = self.pages.get(page_num, Page(page_num))
        page.update({"FileName": filename, "TableName": name, "TableDescription": description}, field_dict)
        self.pages[page_num] = page
        self.field_map.update(page.field_map)
        self.group_map.update(page.group_map)

    def __init__(self, no_default=False, table_filter=None) -> None:
        self.pages: dict[int, Page] = {}
        self.field_map: dict[str, Field] = {}
        self.group_map: dict[str, Group] = {}

        if no_default:
            return

        tables_dir = os.path.join(os.path.dirname(__file__), "tables")

        def list_tables_directory():
            return [f for f in os.listdir(tables_dir) if f.endswith(".py")]

        def filter_table(table):
            if table_filter is None:
                return False

            for f in table_filter.split(","):
                if f in table:
                    return False
            return True

        for f in list_tables_directory():
            if filter_table(f):
                continue
            table: dict = {}
            exec(open(f"{tables_dir}/{f}").read(), {}, table)
            info = table.get("info")
            if info:
                logger.info(f"registering {f}, table={info['Name']}")
                self.register(info, f)

    def with_bank(self, bank: int) -> ContextManager:
        return BankContext(self, bank)

    def search(
        self,
        page: int,
        offset: int | tuple[int, int] | None = None,
        bit: int | None = None,
    ) -> list[Field]:
        results = []
        if page:
            pages = [self.pages[page]] if page in self.pages else []
        else:
            pages = list(self.pages.values())

        address = Address(page, offset, bit).to_canonical()

        for p in pages:
            for f in p.fields:
                if address.includes(f.address):
                    results.append(f)
        return results

    def search_by_name(
        self, name, pertial_match=False, include_groups=False, include_fields=True
    ):
        if not pertial_match:
            return (self.field_map.get(name) if include_fields else None) or (
                self.group_map.get(name) if include_groups else None
            )
        else:
            results = []
            if include_fields:
                for k, v in self.field_map.items():
                    if name.lower() in k.lower():
                        results.append(v)

            if include_groups:
                for k, v in self.group_map.items():
                    if name.lower() in k.lower():
                        results.append(v)

            return sorted(results, key=lambda x: x.address)

    def decode(
        self, page: int, offset: int, data: bytes
    ) -> Generator[tuple[Field, bytes], None, None]:
        fields = self.search(
            page, offset if len(data) == 1 else (offset, offset + len(data) - 1), None
        )
        for f in fields:
            logger.info("Decoding %s", f)
            if isinstance(f.address.offset, int):
                i = f.address.offset - offset
                v = data[i].to_bytes(1, "big")
            elif isinstance(f.address.offset, tuple):
                v = data[
                    f.address.offset[0] - offset : f.address.offset[1] - offset + 1
                ]

            yield f, v

    def to_str(self, include_groups=False, verbose=False):
        lines = []
        for page in sorted(self.pages.values(), key=lambda x: x.page_num):
            lines.append(f"--- Page {page.page_num:02X}h ---")
            lines.append(page.to_str(include_groups=include_groups, verbose=verbose))

        return "\n".join(lines)

    def __str__(self):
        return self.to_str()


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--key")
    parser.add_argument("--value")
    parser.add_argument("--exact-match", action="store_true")
    parser.add_argument("--no-group", action="store_true")
    parser.add_argument("--no-field", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--table-filter")

    args = parser.parse_args()

    level = logging.WARNING if not args.verbose else logging.DEBUG
    logging.basicConfig(level=level)

    m = MemMap(table_filter=args.table_filter)
    if args.key:
        if args.value:
            field = m.search_by_name(
                args.key,
                include_fields=not args.no_field,
                include_groups=not args.no_group,
            )
            print(field.describe())

            for f, v in m.decode(
                field.address.page, field.address.offset, bytes([int(args.value, 0)])
            ):
                print(f.to_str(value=v))
        else:
            for field in m.search_by_name(
                args.key,
                pertial_match=not args.exact_match,
                include_groups=not args.no_group,
                include_fields=not args.no_field,
            ):
                print(field)
    else:
        print(m.to_str(include_groups=not args.no_group, verbose=args.verbose))


if __name__ == "__main__":
    main()
