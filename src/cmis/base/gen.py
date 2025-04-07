import logging
from typing import Collection

import jinja2

from .base import Field, MemMap, RangeGroup

logger = logging.getLogger(__name__)

FILTERED_FIELDNAMES = ["Reserved", "Custom"]
FILTERED_VALUENAMES_ONCE = ["RESERVED"]


def get_values(fields):
    onces = {}
    values = []
    for k, v in fields.get("Values", {}).items():
        if isinstance(k, int):
            if v[1] in FILTERED_VALUENAMES_ONCE and v[1] in onces:
                continue
            values.append((v[1], k))
            onces[v[1]] = k
    return values


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

    return f"ValueEnum_{id(f)}"


class Group:
    ValueEnumTemplate = jinja2.Template(
        """class {{name}}Enum(Enum):
{% for (key, value) in values %}
    {{key}} = {{value}}
{%- endfor %}
"""
    )

    GroupTemplate = jinja2.Template(
        """
class {{name}}(Group):
{%- for (f, values, is_range, enum_class) in subfields %}
    class {{f["Name"]}}Cls(Field):
{% if enum_class %}
        EnumClass = {{enum_class}}
{% endif %}
{%- for (key, value) in values %}
        {{key}}={{value}}
{%- else %}
        pass
{% endfor %}
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
                v = Template(self.name, template, group.parent_info["Templates"])
                fields = set(f[0]["Name"] for f in v.subfields)
                if group.original_name in classes:
                    # check the class that is already generated has the same fields
                    assert (
                        classes[group.original_name] == fields
                    ), f"{classes[group.original_name]} {fields}"
                else:
                    classes[group.original_name] = fields
                    subfields: list[
                        tuple[dict, list[tuple[str, str]], bool, str | None]
                    ] = []
                    for f, values, is_range in v.subfields:
                        key = frozenset(values)
                        if values:
                            if key in value_set:
                                name = value_set[key]["name"]
                            else:
                                name = get_value_enum_name(f, values)
                                logger.info(f"Generating {name} {values}")
                                print(
                                    self.ValueEnumTemplate.render(
                                        values=sorted(values, key=lambda x: x[1]),
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
                            subfields.append(
                                (
                                    f,
                                    [(key, f"{name}Enum.{key}") for (key, _) in values],
                                    is_range,
                                    f"{name}Enum",
                                )
                            )
                        else:
                            subfields.append((f, [], is_range, None))

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

        self.subfields: list[tuple[dict, list[tuple[str, int]], bool]] = []

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

                self.subfields.append((f, get_values(f), is_range))
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

                    self.subfields.append((ff, get_values(ff), is_range))


class Generator:
    Header = """# DO NOT EDIT
# This file is automatically generated by gen.py

from __future__ import annotations
from typing import Iterator
from enum import Enum

from .field import BaseMemMap, Field, Group, RangeGroup
"""

    ValueEnumTemplate = jinja2.Template(
        """class {{name}}Enum(Enum):
{% for (key, value) in values %}
    {{key}} = {{value}}
{%- endfor %}

class {{name}}:
{% for (key, _) in values %}
    {{key}} = {{name}}Enum.{{key}}
{%- endfor %}
"""
    )

    MemMapTemplate = jinja2.Template(
        """{% for (f, values, valuecls) in fields %}
{% if values | length > 1 %}
class {{ f.name }}Enum(Enum):
{% for (key, value) in values %}
    {{key}} = {{value}}
{%- endfor %}
{% endif %}
{% if valuecls %}
class {{ f.name }}(Field, {{ valuecls }}):
    EnumClass = {{ valuecls }}Enum
{% else %}
class {{ f.name }}(Field):
{% endif %}
{% if values | length > 1 %}
    EnumClass = {{f.name}}Enum
{% endif %}
{% for (key, _) in values %}
    {{key}} = {{f.name}}Enum.{{key}}
{%- else %}
{% if not valuecls %}
    pass
{% endif %}
{% endfor %}
{%- endfor %}
class MemMap(BaseMemMap):
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

    def generate(self) -> None:
        print(self.Header)

        groups = []
        exports: list[str] = ["MemMap"]
        fields: list[tuple[Field, Collection, str | None]] = []

        value_set: dict[frozenset[tuple[str, int]], dict] = {}

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
                    values = get_values(f.fields)
                    key = frozenset(values)
                    if values:
                        if key in value_set:
                            if len(value_set[key]["fields"]) == 1:
                                name = value_set[key]["name"]
                                logger.info(
                                    f"Generating {value_set[key]['name']} {values}"
                                )
                                print(
                                    self.ValueEnumTemplate.render(
                                        values=sorted(values, key=lambda x: x[1]),
                                        name=name,
                                    )
                                )
                                exports.append(name)
                                exports.append(f"{name}Enum")

                            value_set[key]["fields"].append(f.name)
                        else:
                            name = get_value_enum_name(f, values)
                            value_set[key] = {
                                "fields": [f.name],
                                "name": name,
                            }
                    fields.append((f, values, None))
                    exports.append(f.name)

        fields = [
            (
                (f, [], value_set[frozenset(values)]["name"])
                if values and len(value_set[frozenset(values)]["fields"]) > 1
                else (f, sorted(values, key=lambda x: x[1]), None)
            )
            for f, values, _ in fields
        ]

        print()

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
