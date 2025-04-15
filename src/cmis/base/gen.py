import logging
import hashlib
import random
import string
from collections import Counter
from typing import TypeAlias, Iterable

import jinja2

from .base import Field, MemMap, RangeGroup

logger = logging.getLogger(__name__)

FILTERED_FIELDNAMES = ["Reserved", "Custom"]
FILTERED_VALUENAMES_ONCE = ["RESERVED"]

EnumValue: TypeAlias = tuple[str, str, int]
EnumKey: TypeAlias = frozenset[tuple[str, int]]
Values: TypeAlias = list[EnumValue]
ConditionalValues: TypeAlias = list[tuple[str, list[tuple[str, int]]]]


def deterministic_random_string(value: str, length: int = 8) -> str:
    hash_bytes = hashlib.sha256(value.encode()).digest()
    seed = int.from_bytes(hash_bytes, "big")

    rng = random.Random(seed)
    chars = string.ascii_letters
    return "".join(rng.choices(chars, k=length))


def get_values(fields) -> list[tuple[str, int]]:
    onces = {}
    ret = []

    values = fields.get("Values", {})
    assert isinstance(values, dict), f"Invalid field {fields}"

    for k, v in values.items():
        if isinstance(k, int):
            if v[1] in FILTERED_VALUENAMES_ONCE and v[1] in onces:
                continue
            ret.append((v[1], k))
            onces[v[1]] = k
    return sorted(ret, key=lambda x: x[1])


def get_value_enum_name(f, values):
    if any(v[0] == "NOT_SUPPORTED" for v in values):
        return "SupportFlag"
    elif any(v[0] == "LESS_THAN_1_MS" for v in values):
        return "Duration"
    elif any(v[0] == "BYPASSED" for v in values):
        return "BypassedOrEnabled"
    elif any(v[0] == "FIXED" for v in values):
        return "FixedOrAdaptive"
    elif any(v[0] == "DO_NOT_RECALL" for v in values):
        return "RecallBuffer"
    elif any(v[0] == "PROVISION" for v in values):
        return "ApplyDPInitLaneFlag"
    elif any(v[0] == "PROVISION_AND_COMMISSION" for v in values):
        return "ApplyImmediateDPInitLaneFlag"
    elif any(v[0] == "ONE_LANE" for v in values):
        return "Lanes"
    elif any(v[0] == "IDLE" for v in values):
        return "IdleOrBusy"
    elif any(v[0] == "SUCCESS" for v in values):
        return "SuccessOrFailed"
    elif any(v[0] == "APPLICATION_DEPENDENT" for v in values):
        return "ExplicitControlFlag"
    elif any(v[0] == "GBIC" for v in values):
        return "Identifier"
    elif any(v[0] == "CAPTURED" for v in values):
        return "CdbCommandResult"

    # generate a fixed random unique name from values
    name = deterministic_random_string("".join(v[0] for v in values))
    return f"ValueEnum_{name}"


EnumTemplate = jinja2.Template(
    """class {{name}}Enum(Enum):
{% for (_, key, value) in values %}
    {{key}} = {{value}}
{%- else %}
pass
{%- endfor %}
"""
)

ConditionalEnumTemplate = jinja2.Template(
    """class {{name}}Enum(ConditionalEnum):
{% for (enum_name, values) in enums %}
    class {{enum_name}}(Enum):
{% for (key, value) in values %}
        {{key}} = {{value}}
{%- endfor %}
{%- endfor %}
    EnumClasses = [{{ enums | map(attribute=0) | join(', ') }}]
"""
)


class Group:
    GroupTemplate = jinja2.Template(
        """
class {{name}}(Group):
{%- for (f, values, is_range, enum_class, conditional) in subfields %}
    class {{f["Name"]}}Cls(Field):
{% if values %}
{% if conditional %}
        ConditionalEnumClass = {{enum_class}}
{% else %}
        EnumClass = {{enum_class}}
{% endif %}
{%- for (enumcls, key, _) in values %}
        {% if enumcls.startswith("#") %}{{enumcls}}{% else %}{{key}} = {{enumcls}}.{{key}}{% endif %}
{%- endfor %}
{%- else %}
        pass
{%- endif %}
{% if is_range %}
    class {{f["Name"]}}RangeCls(RangeGroup):
        def __getitem__(self, index: int) -> "{{name}}.{{f["Name"]}}Cls":
            return {{name}}.{{f["Name"]}}Cls(self.mem_map, self.field.subfields[index], index)

        def __iter__(self) -> Iterator["{{name}}.{{f["Name"]}}Cls"]:
            return iter({{name}}.{{f["Name"]}}Cls(self.mem_map, f, i) for i, f in enumerate(self.field.subfields))
{% endif %}
    @property
    def {{f["Name"]}}(self) -> "{{name}}.{{f["Name"]}}{% if is_range %}Range{% endif %}Cls":
        field = self.subfields["{{f["Name"]}}"]
        return {{name}}.{{f["Name"]}}{% if is_range %}Range{% endif %}Cls(self.mem_map, field, self.index)
{% endfor %}
"""
    )

    FieldTemplate = jinja2.Template(
        """
{% if values | length > 1 %}
class {{name}}Enum(Enum):
{%- for (key, value) in values %}
    {{key}}={{value}}
{%- endfor %}
{% endif %}
class {{name}}(Field):
{% if values | length > 1 %}
    EnumClass = {{name}}Enum
{% endif %}
{% for (key, value) in values %}
    {{key}}={{name}}Enum.{{key}}
{%- else %}
    pass
{% endfor %}
"""
    )

    RangeGroupTemplate = jinja2.Template(
        """
class {{name}}(RangeGroup, {{group_name}}):
    def __getitem__(self, index: int) -> {{group_name}}:
        return {{group_name}}(self.mem_map, self.field.subfields[index], index)

    def __iter__(self) -> Iterator[{{group_name}}]:
        return iter({{group_name}}(self.mem_map, f, i) for i, f in enumerate(self.field.subfields))
"""
    )

    def __init__(self, mem_map, group):
        self.mem_map = mem_map
        self.group = group

    @property
    def name(self):
        return self.group.name

    @property
    def address(self):
        return self.group.address

    @property
    def clsname(self):
        if isinstance(self.group, RangeGroup):
            return f"{self.group.original_name}Range"
        else:
            return self.group.original_name

    def _generate_conditional_enum(self, name: str, field: dict) -> Values:
        lists = []
        v = field.get("Values")
        assert isinstance(v, list), f"Invalid field {field}"

        conditional_values: ConditionalValues = []
        for i, value in enumerate(v):
            n = f"{name}Enum{i}"
            value = {k: v for (k, v) in value.items() if k != "When"}
            v = get_values({"Values": value})
            if len(v) == 0:
                continue
            conditional_values.append((n, v))
            lists += [(f"{name}Enum.{n}", e[0], 0) for e in v]

        counter = Counter(v[1] for v in lists)
        values: Values = []

        for item in lists:
            if counter[item[1]] > 1:
                values.append(
                    (
                        f"# {item[1]} = {item[0]}.{item[1]} # omitted because of the duplicate",
                        "",
                        0,
                    )
                )
            else:
                values.append(item)

        if len(values) == 0:
            return []

        print(
            ConditionalEnumTemplate.render(
                enums=conditional_values,
                name=name,
            )
        )
        return values

    def generate(
        self,
        classes: dict[str, set[str]],
        value_set: dict[frozenset[tuple[str, int]], dict],
        exports: list[str],
    ):
        group = (
            self.group.subfields[0]
            if isinstance(self.group, RangeGroup)
            else self.group
        )

        if group.template:
            template = group.template
            if all(isinstance(k, str) for k in template.keys()):
                # field template
                if "Template" in group.template:
                    template = group.parent_info["Templates"][
                        group.template["Template"]
                    ]
                print(
                    self.FieldTemplate.render(
                        name=group.original_name, values=get_values(template)
                    )
                )
                exports.append(group.original_name)
            else:
                # byte level or bit level template
                t = Template(self.name, template, group.parent_info["Templates"])
                fields = set(f[0]["Name"] for f in t.subfields)
                if group.original_name in classes:
                    # check the class that is already generated has the same fields
                    assert (
                        classes[group.original_name] == fields
                    ), f"{classes[group.original_name]} {fields}"
                else:
                    classes[group.original_name] = fields
                    subfields: list[
                        tuple[dict, list[tuple[str, str, int]], bool, str, bool]
                    ] = []
                    for f, v, is_range in t.subfields:
                        key = frozenset(v)
                        conditional = False
                        enum_class = ""
                        if v:
                            if key in value_set:
                                name = value_set[key]["name"]
                                values = [
                                    (f"{name}Enum", key, value) for (key, value) in v
                                ]
                            else:
                                name = get_value_enum_name(f, v)
                                logger.info(f"Generating {name} {v}")
                                conditional = isinstance(f.get("Values"), list)
                                if conditional:
                                    values = self._generate_conditional_enum(name, f)
                                else:
                                    values = [
                                        (f"{name}Enum", key, value)
                                        for (key, value) in v
                                    ]
                                    print(
                                        EnumTemplate.render(
                                            values=values,
                                            name=name,
                                        )
                                    )
                                exports.append(f"{name}Enum")
                                value_set[key] = {
                                    "fields": [
                                        "",
                                        "",
                                    ],  # dummy fields to suppress duplicate generation in Generator.generate()
                                    "name": name,
                                }
                            enum_class = f"{name}Enum"
                        else:
                            values = []

                        subfields.append((f, values, is_range, enum_class, conditional))

                    print(
                        self.GroupTemplate.render(
                            name=group.original_name, subfields=subfields
                        )
                    )
                    exports.append(group.original_name)
        else:
            print(
                self.FieldTemplate.render(
                    name=group.original_name, values=get_values(group.fields)
                )
            )
            exports.append(group.original_name)

        if isinstance(self.group, RangeGroup):
            if self.clsname in classes:
                # check the class that is already generated has the same fields
                assert (
                    classes[self.clsname] == set()
                ), f"{self.clsname} {classes[self.clsname]}"
            else:
                classes[self.clsname] = set()
                print(
                    self.RangeGroupTemplate.render(
                        name=self.clsname, group_name=self.group.original_name
                    )
                )
                exports.append(self.clsname)


class Template:
    def __init__(
        self,
        name: str,
        fields: dict[int | tuple | range, dict],
        templates: dict[str, dict],
    ) -> None:
        self.name = name
        self.fields = fields

        assert all(
            not isinstance(key, str) for key in fields.keys()
        ), f"{name} field {fields.keys()}"

        self.subfields: list[tuple[dict, Iterable[tuple[str, int]], bool]] = []

        for k, f in fields.items():
            is_range = isinstance(k, range)
            if all(isinstance(k, str) for k in f.keys()):
                if "Name" in f:
                    pass
                elif "Template" in f:
                    f.update(templates[f["Template"]])
                    f["Name"] = f["Template"]
                    assert f["Name"].isidentifier()
                else:
                    raise ValueError(f"Invalid field {f}")

                v = f.get("Values")
                # generate key for value_set
                if isinstance(v, list):  # conditional register generation
                    lists = []
                    for value in v:
                        value = {k: v for (k, v) in value.items() if k != "When"}
                        v = get_values({"Values": value})
                        lists += v
                    values = lists
                else:
                    values = get_values(f)

                self.subfields.append((f, values, is_range))
            else:
                for kk, ff in f.items():
                    is_range = isinstance(kk, range)
                    assert all(isinstance(k, str) for k in ff.keys())
                    if "Name" in ff:
                        pass
                    elif "Template" in ff:
                        ff.update(templates[ff["Template"]])
                        ff["Name"] = ff["Template"]
                        assert ff["Name"].isidentifier()
                    else:
                        raise ValueError(f"Invalid field {ff}")

                    values = get_values(ff)

                    self.subfields.append((ff, values, is_range))


class Generator:
    Header = """# DO NOT EDIT
# This file is automatically generated by gen.py

from __future__ import annotations
from typing import Iterator
from enum import Enum

from .field import BaseMemMap, Field, Group, RangeGroup, ConditionalEnum
"""

    ValueEnumTemplate = jinja2.Template(
        """class {{name}}:
{% for (enumcls, key, _) in values %}
    {% if enumcls.startswith("#") %}{{enumcls}}{% else %}{{key}} = {{enumcls}}.{{key}}{% endif %}
{%- endfor %}
"""
    )

    FieldTemplate = jinja2.Template(
        """class {{ f.name }}(Field):
{% if values %}
{% if conditional %}
    ConditionalEnumClass = {{f.name}}Enum
{% else %}
    EnumClass = {{f.name}}Enum
{% endif %}
{% for (enumcls, key, _) in values %}
    {% if enumcls.startswith("#") %}{{enumcls}}{% else %}{{key}} = {{enumcls}}.{{key}}{% endif %}
{%- endfor %}
{%- else %}
    pass
{%- endif %}
"""
    )

    FieldTemplateWithValueCls = jinja2.Template(
        """class {{ f.name }}(Field, {{ valuecls }}):
    EnumClass = {{ valuecls }}Enum"""
    )

    MemMapTemplate = jinja2.Template(
        """class MemMap(BaseMemMap):
{% for g in groups %}
    # {{ g.address }}
    @property
    def {{ g.name }}(self) -> {{ g.clsname }}:
        return {{ g.clsname }}(self, self._search_group("{{ g.name }}"))
{% endfor %}
{% for f, _, _ in fields %}
    # {{ f.address }}
    @property
    def {{ f.name }}(self) -> {{ f.name }}:
        return {{ f.name }}(self, self._search_field("{{ f.name }}"))
{% endfor %}
"""
    )

    Footer = jinja2.Template(
        """CMIS_EXPORTS = [{% for name in exports %}
    "{{name}}",
{% endfor %}]"""
    )

    def __init__(self, mem_map: MemMap) -> None:
        self.mem_map = mem_map

    def _generate_conditional_enum(self, name: str, field: Field) -> Values:
        lists = []
        v = field.fields.get("Values")
        assert isinstance(v, list), f"Invalid field {field.fields}"

        conditional_values: ConditionalValues = []
        for i, value in enumerate(v):
            n = f"{name}Enum{i}"
            value = {k: v for (k, v) in value.items() if k != "When"}
            v = get_values({"Values": value})
            if len(v) == 0:
                continue
            conditional_values.append((n, v))
            lists += [(f"{name}Enum.{n}", e[0], 0) for e in v]

        counter = Counter(v[1] for v in lists)
        values: Values = []

        for item in lists:
            if counter[item[1]] > 1:
                values.append(
                    (
                        f"# {item[1]} = {item[0]}.{item[1]} # omitted because of the duplicate",
                        "",
                        0,
                    )
                )
            else:
                values.append(item)

        if len(values) == 0:
            return []

        print(
            ConditionalEnumTemplate.render(
                enums=conditional_values,
                name=name,
            )
        )
        return values

    def _generate_enum(self, name: str, field: Field) -> Values:
        if isinstance(field.fields.get("Values"), list):
            return self._generate_conditional_enum(name, field)
        else:
            values: Values = [
                (f"{name}Enum", v[0], v[1]) for v in get_values(field.fields)
            ]

            if len(values) == 0:
                return []

            print(
                EnumTemplate.render(
                    values=values,
                    name=name,
                )
            )
            return values

    def generate(self) -> None:
        print(self.Header)

        groups: list = []
        exports: list[str] = ["MemMap"]
        fields: list[tuple[Field, EnumKey, bool]] = []

        # EnumClsName,EnumValueName,EnumValue
        value_set: dict[EnumKey, dict] = {}

        classes: dict[str, set[str]] = {}
        for _, page in sorted(self.mem_map.pages.items(), key=lambda x: x[0]):
            for g in sorted(page.group_map.values(), key=lambda x: x.address):
                if g.group is None:  # top level group
                    logger.info(f"Generating group for {g.name}, type: {type(g)}")
                    group = Group(self.mem_map, g)
                    group.generate(classes, value_set, exports)
                    groups.append(group)

            for f in sorted(page.field_map.values(), key=lambda x: x.address):
                if f.group is None and f.name not in FILTERED_FIELDNAMES:
                    logger.info("Generating field for %s", f.name)

                    conditional: bool = False
                    v = f.fields.get("Values")

                    # generate key for value_set
                    if isinstance(v, list):  # conditional register generation
                        lists = []
                        for value in v:
                            value = {k: v for (k, v) in value.items() if k != "When"}
                            v = get_values({"Values": value})
                            lists += v
                        key = frozenset(lists)
                        conditional = True
                    else:
                        key = frozenset(get_values(f.fields))

                    if key != frozenset([]):
                        if key in value_set:
                            if (
                                len(value_set[key]["fields"]) == 1
                            ):  # generate only once when used by multiple fields
                                name = value_set[key]["name"]
                                logger.info(f"Generating {value_set[key]['name']}")

                                values = self._generate_enum(name, f)

                                print(
                                    self.ValueEnumTemplate.render(
                                        values=values,
                                        name=name,
                                    )
                                )
                                exports.append(name)
                                exports.append(f"{name}Enum")

                            value_set[key]["fields"].append(f.name)
                        else:
                            name = get_value_enum_name(f, key)
                            logger.info(f"Generating {name} {f.name}")
                            value_set[key] = {
                                "fields": [f.name],
                                "name": name,
                            }

                    fields.append((f, key, conditional))
                    exports.append(f.name)

        for f, key, conditional in fields:
            if (
                len(key) > 0 and len(value_set[key]["fields"]) > 1
            ):  # if used by multiple fields. enums are already generated
                valuecls = value_set[key]["name"]
                field = self.FieldTemplateWithValueCls.render(f=f, valuecls=valuecls)
            else:
                values = self._generate_enum(f.name, f)
                field = self.FieldTemplate.render(
                    f=f, values=values, conditional=conditional
                )

            print(field)

        mem_map = self.MemMapTemplate.render(groups=groups, fields=fields)
        print(mem_map)

        print()

        print(self.Footer.render(exports=exports))


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--table-filter")

    args = parser.parse_args()

    level = logging.INFO if not args.verbose else logging.DEBUG
    logging.basicConfig(level=level)

    m = MemMap(table_filter=args.table_filter)
    Generator(m).generate()


if __name__ == "__main__":
    main()
