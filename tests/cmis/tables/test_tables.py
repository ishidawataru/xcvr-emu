table1 = {
    "Name": "Table1",
    "Description": "Basic Table",
    "Page": 0,
    "Table": {
        0: {  # single byte field
            0: {  # single bit field
                "Name": "SingleBitField",
                "Description": "Single bit field",
                "Type": ["RO", "Opt"],
            },
            1: {  # single bit field with values
                "Name": "SingleBitFieldWithValues",
                "Description": "Single bit field",
                "Type": ["RO", "Opt"],
                "Values": {
                    0: ("Value0", "VALUE0"),
                    1: ("Value1", "VALUE1"),
                },
            },
            (3, 2): {  # two bit field with values
                "Name": "TwoBitFieldWithValues",
                "Description": "Two bit field",
                "Type": ["RO", "Opt"],
                "Values": {
                    0: ("Value0", "VALUE0"),
                    1: ("Value1", "VALUE1"),
                    2: ("Value2", "VALUE2"),
                    3: ("Value3", "VALUE3"),
                },
            },
            # 8: {} -- this is invalid. max bit index is 7
        },
        (1, 2): {  # two byte field
            "Name": "TwoByteField",
            "Description": "Two byte field",
            "Type": ["RW", "Rqd"],
        },
        # above is equivalent to below (syntax sugar)
        #        (1, 2): {
        #            (15, 0): {
        #                "Name": "TwoByteField",
        #                "Description": "Two byte field",
        #                "Type": ["RW", "Rqd"],
        #            }
        #        },
        (3, 2): {
            # 10bits field -- this is valid because parent byte space indicator is (3, 2)
            (9, 0): {
                "Name": "TenBitField",
                "Description": "Ten bit field",
                "Type": ["RW", "Rqd"],
                "Values": {
                    0: ("Value0", "VALUE0"),
                    1: ("Value1", "VALUE1"),
                },
            }
        },
        4: {
            "Name": "OneByteField",
            "Description": "One byte field",
            "Type": ["RW", "Rqd"],
        },
        5: {  # 4, 5 is equivalent.
            (7, 0): {
                "Name": "EightBitField",
                "Description": "Eight bit field",
                "Type": ["RW", "Rqd"],
            }
        },
    },
}

# ----------

# 3 types of templates
#
# 1. ByteLevelTemplate
# 2. BitLevelTemplate
# 3. FieldTemplate
#
# template is a dictionary. if all keys are int or tuple, it is a byte level or bit level template.
# if all keys are str, it is a field template.
# byte level template, bit level template is determined by where it is used.
#
# if it is used where byte identifier is tuple, it is byte level template or field template.
# if it is used where byte identifier is single byte, it is bit level template or field template.
# if it is used where bit identifier is tuple, it is bit level template or field template.
# if it is used where bit identifier is single bit, it is field template.

table2 = {
    "Name": "Table2",
    "Description": "A Table With Templates",
    "Page": 0,
    "Table": {
        "ByteLevelTemplate": {
            0: {  # byte level not bit level
                "Name": "Byte0",
            },
            1: {
                (7, 0): {  # bit field description is also allowed
                    "Name": "Byte1",
                },
            },
            # 2 is invalid because it doesn't fit in (90, 91) byte space
        },
        79: {
            "Template": "FieldTemplate",
            "Prefix": "Prefix",
        },
        (80, 81): {
            "Template": "ByteLevelTemplate",  # when byte identifier is tuple, template is byte level
            "Prefix": "Prefix",
            "Suffix": "_1",
        },
        "BitLevelTemplate": {
            0: {  # bit level not byte level
                "Name": "Bit0",
            },
            1: {
                "Name": "Bit1",
            },
        },
        82: {
            "Template": "BitLevelTemplate",  # when byte identifier is single byte, template is bit level
            "Prefix": "Prefix",
            "Suffix": "_2",
        },
        "FieldTemplate": {
            "Name": "FieldTemplate",  # optional. if not provided, name is template name
            "Description": "ID from a suitable table of IDs in [5] that is identified by the MediaType Byte 00h:85",
            "Type": ["RO", "Rqd"],
        },
        83: {
            0: {
                "Template": "FieldTemplate",  # when template is used for single bit field, template is field template
                "Suffix": "_0",
            }
        },
        # when template is used for multi bit field, template is bit level template or field template
        84: {
            (3, 0): {
                "Template": "FieldTemplate",  # field template case
                "Suffix": "_1",
            }
        },
        85: {
            (3, 0): {
                "Template": "BitLevelTemplate",  # bit level template case
                "Suffix": "_0",
            }
        },
    },
}

# ----------

table3 = {
    "Name": "Table3",
    "Description": "Use Templates in Templates",
    "Page": 0,
    "Table": {
        (0, 4): {
            "Template": "ByteLevelTemplate",
            "Suffix": "_1",
        },
        "ByteLevelTemplate": {
            0: {
                "Template": "BitLevelTemplate",
            },
            (1, 4): {
                # the same rule of template is applied for nested template
                # if it is used where byte identifier is tuple, it is byte level template or field template.
                "Template": "ByteLevelTemplate2",
            },
        },
        "BitLevelTemplate": {
            (7, 0): {
                "Template": "FieldTemplate",
            }
        },
        "FieldTemplate": {
            "Name": "FieldTemplate",
        },
        "FieldTemplate2": {
            "Name": "FieldTemplate2",
        },
        "ByteLevelTemplate2": {
            (0, 2): {
                "Template": "FieldTemplate2",
            },
            3: {
                "Template": "FieldTemplate2",
                "Suffix": "_3",
            },
        },
    },
}

# ----------

table4 = {
    "Name": "Table4",
    "Description": "Use range",
    "Page": 0,
    "Table": {
        range(0, 4): {
            "Name": "ByteRangeFields",
        },
        5: {
            range(0, 8): {
                "Name": "BitRangeFields",
            },
            # no overwrap check for now
            #            7: {
            #                "Name": "SingleBitField",
            #            },
        },
        (6, 7): {
            range(0, 16): {
                "Name": "BitRangeFieldsInMultiBytesField",
            },
        },
        "MultiBytesTemplate": {
            range(0, 2): {
                "Name": "ByteRangeFieldsInMultiBytesTemplate",
            },
        },
        (8, 9): {
            "Template": "MultiBytesTemplate",
        },
        range(10, 12): {
            (3, 0): {
                "Name": "MultiBitFieldInByteRange",
            }
        },
        # nested range is supported but not recommended. it is better to single range with tuple like the next one
        range(12, 14): {
            range(0, 8): {
                "Name": "BitRangeFieldsInByteRange",
            }
        },
        #        (12, 13): {
        #            range(0, 16): {
        #                "Name": "BitRangeFieldsInByteRange",
        #            }
        #        },
        range(14, 16): {
            "Template": "BitLevelTemplate",
        },
        "BitLevelTemplate": {
            0: {
                "Name": "Bit0",
                "SuffixFunc": lambda i: f"_{i}",
            },
            1: {
                "Name": "Bit1",
                "SuffixFunc": lambda i: f"_{i}",
            },
        },
        "MultiBytesTemplateWithBitLevelTemplate": {
            0: {
                "Template": "BitLevelTemplate",
            },
            range(1, 3): {
                "Template": "BitLevelTemplate",
                # "Suffix": "_suffix" # adding suffix here is not supported because BitLevelTemplate uses SuffixFunc
            },
        },
        (16, 18): {
            "Template": "MultiBytesTemplateWithBitLevelTemplate",
            "Prefix": "Prefix1::",
        },
    },
}

# ----------

table5 = {
    "Name": "Table5",
    "Description": "Use range",
    "Page": 0,
    "Table": {
        range(0, 4): {
            "Name": "ByteRangeFields",
        },
        (4, 5): {
            range(0, 16, 2): {
                "Name": "BitRangeFields",
            },
        },
        "Template": {
            0: {
                "Name": "Bit0",
            },
            1: {
                "Name": "Bit1",
            },
            (2, 7): {
                "Name": "Bit2_7",
            },
        },
        6: {
            "Template": "Template",
        },
    },
}
