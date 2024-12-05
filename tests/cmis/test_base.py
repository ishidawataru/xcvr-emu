import logging
import os

import pytest

from cmis.base.base import Address, MemMap


@pytest.fixture
def mem_map():
    return MemMap()


def test_basic_table():
    test_tables = os.path.join(os.path.dirname(__file__), "tables", "test_tables.py")
    table = {}
    exec(open(test_tables).read(), {}, table)

    t = table.get("table1")
    m = MemMap(no_default=True)
    m.register(t)

    f = m.search_by_name("SingleBitField")
    assert f
    assert f.name == "SingleBitField"
    assert f.address.size == 1

    f = m.search_by_name("SingleBitFieldWithValues")
    assert f
    assert f._value_to_str(bytes([0])) == "VALUE0(0)"
    assert f.address.size == 1

    f = m.search_by_name("TwoBitFieldWithValues")
    assert f
    assert f._value_to_str(bytes([0b1000])) == "VALUE2(2)"
    assert f.address.size == 2

    f = m.search_by_name("TwoByteField")
    assert f
    assert f.address.size == 16

    f = m.search_by_name("TenBitField")
    assert f
    print(f)
    assert f.address.size == 10

    f = m.search_by_name("OneByteField")
    assert f
    assert f.address.size == 8

    f = m.search_by_name("EightBitField")
    assert f
    assert f.address.size == 8

    assert (
        str(m)
        == """--- Page 00h ---
00h:0.0        | SingleBitField
00h:0.1        | SingleBitFieldWithValues [VALUE0|VALUE1]
00h:0.2-3      | TwoBitFieldWithValues [VALUE0|VALUE1|VALUE2|VALUE3]
00h:1-2        | TwoByteField
00h:2-3.0-9    | TenBitField [VALUE0|VALUE1]
00h:4          | OneByteField
00h:5          | EightBitField"""
    )


def test_table_with_templates(caplog):
    caplog.set_level(logging.DEBUG)
    test_tables = os.path.join(os.path.dirname(__file__), "tables", "test_tables.py")
    table = {}
    exec(open(test_tables).read(), {}, table)

    t = table.get("table2")
    m = MemMap(no_default=True)
    m.register(t)

    f = m.search_by_name("PrefixFieldTemplate")
    assert f

    f = m.search_by_name("PrefixByte0_1")
    assert f

    f = m.search_by_name("FieldTemplate_0")
    assert f

    assert (
        str(m)
        == """--- Page 00h ---
00h:79         | PrefixFieldTemplate
00h:80         | PrefixByte0_1
00h:81         | PrefixByte1_1
00h:82.0       | PrefixBit0_2
00h:82.1       | PrefixBit1_2
00h:83.0       | FieldTemplate_0
00h:84.0-3     | FieldTemplate_1
00h:85.0       | Bit0_0
00h:85.1       | Bit1_0"""
    )


def test_use_templates_in_templates(caplog):
    caplog.set_level(logging.DEBUG)
    test_tables = os.path.join(os.path.dirname(__file__), "tables", "test_tables.py")
    table = {}
    exec(open(test_tables).read(), {}, table)

    t = table.get("table3")
    m = MemMap(no_default=True)
    m.register(t)

    assert (
        str(m)
        == """--- Page 00h ---
00h:0          | FieldTemplate_1
00h:1-3        | FieldTemplate2_1
00h:4          | FieldTemplate2_3_1"""
    )


def test_range():
    test_tables = os.path.join(os.path.dirname(__file__), "tables", "test_tables.py")
    table = {}
    exec(open(test_tables).read(), {}, table)

    t = table.get("table4")
    m = MemMap(no_default=True)
    m.register(t)

    assert (
        str(m)
        == """--- Page 00h ---
00h:0          | ByteRangeFields1
00h:1          | ByteRangeFields2
00h:2          | ByteRangeFields3
00h:3          | ByteRangeFields4
00h:5.0        | BitRangeFields1
00h:5.1        | BitRangeFields2
00h:5.2        | BitRangeFields3
00h:5.3        | BitRangeFields4
00h:5.4        | BitRangeFields5
00h:5.5        | BitRangeFields6
00h:5.6        | BitRangeFields7
00h:5.7        | BitRangeFields8
00h:6-7.0      | BitRangeFieldsInMultiBytesField1
00h:6-7.1      | BitRangeFieldsInMultiBytesField2
00h:6-7.2      | BitRangeFieldsInMultiBytesField3
00h:6-7.3      | BitRangeFieldsInMultiBytesField4
00h:6-7.4      | BitRangeFieldsInMultiBytesField5
00h:6-7.5      | BitRangeFieldsInMultiBytesField6
00h:6-7.6      | BitRangeFieldsInMultiBytesField7
00h:6-7.7      | BitRangeFieldsInMultiBytesField8
00h:6-7.8      | BitRangeFieldsInMultiBytesField9
00h:6-7.9      | BitRangeFieldsInMultiBytesField10
00h:6-7.10     | BitRangeFieldsInMultiBytesField11
00h:6-7.11     | BitRangeFieldsInMultiBytesField12
00h:6-7.12     | BitRangeFieldsInMultiBytesField13
00h:6-7.13     | BitRangeFieldsInMultiBytesField14
00h:6-7.14     | BitRangeFieldsInMultiBytesField15
00h:6-7.15     | BitRangeFieldsInMultiBytesField16
00h:8          | ByteRangeFieldsInMultiBytesTemplate1
00h:9          | ByteRangeFieldsInMultiBytesTemplate2
00h:10.0-3     | MultiBitFieldInByteRange1
00h:11.0-3     | MultiBitFieldInByteRange2
00h:12.0       | BitRangeFieldsInByteRange1_1
00h:12.1       | BitRangeFieldsInByteRange1_2
00h:12.2       | BitRangeFieldsInByteRange1_3
00h:12.3       | BitRangeFieldsInByteRange1_4
00h:12.4       | BitRangeFieldsInByteRange1_5
00h:12.5       | BitRangeFieldsInByteRange1_6
00h:12.6       | BitRangeFieldsInByteRange1_7
00h:12.7       | BitRangeFieldsInByteRange1_8
00h:13.0       | BitRangeFieldsInByteRange2_1
00h:13.1       | BitRangeFieldsInByteRange2_2
00h:13.2       | BitRangeFieldsInByteRange2_3
00h:13.3       | BitRangeFieldsInByteRange2_4
00h:13.4       | BitRangeFieldsInByteRange2_5
00h:13.5       | BitRangeFieldsInByteRange2_6
00h:13.6       | BitRangeFieldsInByteRange2_7
00h:13.7       | BitRangeFieldsInByteRange2_8
00h:14.0       | Bit0_0
00h:14.1       | Bit1_0
00h:15.0       | Bit0_1
00h:15.1       | Bit1_1
00h:16.0       | Prefix1_Bit0
00h:16.1       | Prefix1_Bit1
00h:17.0       | Prefix1_Bit0_0
00h:17.1       | Prefix1_Bit1_0
00h:18.0       | Prefix1_Bit0_1
00h:18.1       | Prefix1_Bit1_1"""
    )


def test_address():
    addr = Address(0, (0, 7), (8, 15))
    assert addr.size == 8
    assert addr.byte_size == 1
    assert addr.start_byte == 1
    assert str(addr) == "00h:1"

    addr = Address(0, (0, 7), (8, 16))
    assert addr.size == 9
    assert addr.byte_size == 2
    assert addr.start_byte == 1
    assert str(addr) == "00h:1-2.0-8"

    addr = Address(0, (0, 7), (5, 10))
    assert addr.size == 6
    assert addr.byte_size == 2
    assert addr.start_byte == 0
    assert str(addr) == "00h:0-1.5-10"

    addr = Address(0, 1, (0, 3))
    assert addr.size == 4
    assert addr.byte_size == 1
    assert addr.start_byte == 1
    assert str(addr) == "00h:1.0-3"

    addr = Address(0, 1, (0, 7))
    assert addr.size == 8
    assert addr.byte_size == 1
    assert addr.start_byte == 1
    assert str(addr) == "00h:1"

    addr = Address(0, (2, 3), (0, 9))
    assert addr.size == 10
    assert str(addr) == "00h:2-3.0-9"
    assert str(addr.to_canonical()) == "00h:2-3.0-9"

    addr = Address.from_str("00h:2-3.0-9")
    assert str(addr) == "00h:2-3.0-9"


def test_search(mem_map):
    f = mem_map.search(0, 0)
    assert len(f) == 1
    assert f[0].name == "SFF8024Identifier"


def test_to_str_with_values(caplog):
    caplog.set_level(logging.DEBUG)
    test_tables = os.path.join(os.path.dirname(__file__), "tables", "test_tables.py")
    table = {}
    exec(open(test_tables).read(), {}, table)

    t = table.get("table5")
    m = MemMap(no_default=True)
    m.register(t)

    f = m.search_by_name("ByteRangeFields", include_groups=True)
    assert (
        f.to_str(
            value=bytes([0x01, 0x02, 0x03, 0x04]),
            recursive=True,
        )
        == """00h:0-3        | ByteRangeFields (Group of 4)
00h:0          | ByteRangeFields1 | 1
00h:1          | ByteRangeFields2 | 2
00h:2          | ByteRangeFields3 | 3
00h:3          | ByteRangeFields4 | 4"""
    )

    f = m.search_by_name("BitRangeFields", include_groups=True)
    assert (
        f.to_str(
            value=bytes([0b11110000, 0b11110000]),
            recursive=True,
        )
        == """00h:4-5        | BitRangeFields (Group of 8)
00h:4.0-1      | BitRangeFields1 | 0
00h:4.2-3      | BitRangeFields2 | 0
00h:4.4-5      | BitRangeFields3 | 3
00h:4.6-7      | BitRangeFields4 | 3
00h:5.0-1      | BitRangeFields5 | 0
00h:5.2-3      | BitRangeFields6 | 0
00h:5.4-5      | BitRangeFields7 | 3
00h:5.6-7      | BitRangeFields8 | 3"""
    )

    f = m.search_by_name("Template", include_groups=True)
    assert (
        f.to_str(
            value=bytes([0b00101011]),
            recursive=True,
        )
        == """00h:6          | Template (Group of 3)
00h:6.0        | Bit0 | 1
00h:6.1        | Bit1 | 1
00h:6.2-7      | Bit2_7 | 10"""
    )
