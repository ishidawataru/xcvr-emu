info = {
    "Name": "ModuleFlags",
    "Description": "CMIS v5.2 8.9 Module Flags page 130",
    "Page": 0,
    "Table": {
        8: {
            7: {
                "Name": "CdbCmdCompleteFlag2",
                "Description": "Latched Flag to indicate completion of a CDB command for CDB instance 2.",
                "Note": "Support is advertised in field 01h:163.7-6",
                "Type": ["RO/COR", "Adv"],
            },
            6: {
                "Name": "CdbCmdCompleteFlag1",
                "Description": "Latched Flag to indicate completion of a CDB command for CDB instance 1.",
                "Note": "Support is advertised in field 01h:163.7-6",
                "Type": ["RO/COR", "Adv"],
            },
            (5, 3): {
                "Name": "Reserved",
                "Description": "Reserved",
                "Type": ["Rqd"],
            },
            2: {
                "Name": "DataPathFirmwareErrorFlag",
                "Description": "Latched Flag to indicate that subordinated firmware in an auxiliary device for processing transmitted or received signals (e.g., a DSP) has failed.",
                "Type": ["RO/COR", "Adv"],
            },
            1: {
                "Name": "ModuleFirmwareErrorFlag",
                "Description": "Latched Flag to indicate that self-supervision of the main module firmware has detected a failure in the main module firmware itself.",
                "Note": "Possible causes include program memory being corrupted and incomplete firmware loading.",
                "Type": ["RO/COR", "Adv"],
            },
            0: {
                "Name": "ModuleStateChangedFlag",
                "Description": "Latched Flag to indicate a Module State Change.",
                "Type": ["RO/COR", "Rqd"],
            },
        },
        9: {
            7: {
                "Name": "VccMonLowWarningFlag",
                "Description": "Latched Flag for low supply voltage warning.",
                "Type": ["RO/COR"],
            },
            6: {
                "Name": "VccMonHighWarningFlag",
                "Description": "Latched Flag for high supply voltage warning.",
                "Type": ["Adv"],
            },
            5: {
                "Name": "VccMonLowAlarmFlag",
                "Description": "Latched Flag for low supply voltage alarm.",
                "Type": ["RO/COR"],
            },
            4: {
                "Name": "VccMonHighAlarmFlag",
                "Description": "Latched Flag for high supply voltage alarm.",
                "Type": ["Adv"],
            },
            3: {
                "Name": "TempMonLowWarningFlag",
                "Description": "Latched Flag for low temperature warning.",
                "Type": ["RO/COR"],
            },
            2: {
                "Name": "TempMonHighWarningFlag",
                "Description": "Latched Flag for high temperature warning.",
                "Type": ["Adv"],
            },
            1: {
                "Name": "TempMonLowAlarmFlag",
                "Description": "Latched Flag for low temperature alarm.",
                "Type": ["RO/COR"],
            },
            0: {
                "Name": "TempMonHighAlarmFlag",
                "Description": "Latched Flag for high temperature alarm.",
                "Type": ["Adv"],
            },
        },
        10: {
            7: {
                "Name": "Aux2MonLowWarningFlag",
                "Description": "Latched Flag for low Aux 2 monitor warning.",
                "Type": ["RO/COR", "Adv"],
            },
            6: {
                "Name": "Aux2MonHighWarningFlag",
                "Description": "Latched Flag for high Aux 2 monitor warning.",
                "Type": ["Adv"],
            },
            5: {
                "Name": "Aux2MonLowAlarmFlag",
                "Description": "Latched Flag for low Aux 2 monitor alarm.",
                "Type": ["RO/COR"],
            },
            4: {
                "Name": "Aux2MonHighAlarmFlag",
                "Description": "Latched Flag for high Aux 2 monitor alarm.",
                "Type": ["Adv"],
            },
            3: {
                "Name": "Aux1MonLowWarningFlag",
                "Description": "Latched Flag for low Aux 1 monitor warning.",
                "Type": ["RO/COR"],
            },
            2: {
                "Name": "Aux1MonHighWarningFlag",
                "Description": "Latched Flag for high Aux 1 monitor warning.",
                "Type": ["Adv"],
            },
            1: {
                "Name": "Aux1MonLowAlarmFlag",
                "Description": "Latched Flag for low Aux 1 monitor alarm.",
                "Type": ["RO/COR"],
            },
            0: {
                "Name": "Aux1MonHighAlarmFlag",
                "Description": "Latched Flag for high Aux 1 monitor alarm.",
                "Type": ["Adv"],
            },
        },
        11: {
            7: {
                "Name": "CustomMonLowWarningFlag",
                "Description": "Latched Flag for low Vendor Defined Monitor warning.",
                "Type": ["RO/COR", "Adv"],
            },
            6: {
                "Name": "CustomMonHighWarningFlag",
                "Description": "Latched Flag for high Vendor Defined Monitor warning.",
                "Type": ["Adv"],
            },
            5: {
                "Name": "CustomMonLowAlarmFlag",
                "Description": "Latched Flag for low Vendor Defined Monitor alarm.",
                "Type": ["RO/COR"],
            },
            4: {
                "Name": "CustomMonHighAlarmFlag",
                "Description": "Latched Flag for high Vendor Defined Monitor alarm.",
                "Type": ["Adv"],
            },
            3: {
                "Name": "Aux3MonLowWarningFlag",
                "Description": "Latched Flag for low Aux 3 monitor warning.",
                "Type": ["RO/COR"],
            },
            2: {
                "Name": "Aux3MonHighWarningFlag",
                "Description": "Latched Flag for high Aux 3 monitor warning.",
                "Type": ["Adv"],
            },
            1: {
                "Name": "Aux3MonLowAlarmFlag",
                "Description": "Latched Flag for low Aux 3 monitor alarm.",
                "Type": ["RO/COR"],
            },
            0: {
                "Name": "Aux3MonHighAlarmFlag",
                "Description": "Latched Flag for high Aux 3 monitor alarm.",
                "Type": ["Adv"],
            },
        },
        12: {(7, 0): {"Name": "Reserved[1]", "Description": "Reserved for Flags"}},
        13: {(7, 0): {"Name": "Custom[1]", "Description": "Custom Flags"}},
    },
}
