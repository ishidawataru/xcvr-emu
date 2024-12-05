info = {
    "Name": "ModuleLevelMasks",
    "Description": "CMIS v5.2 8.12 Module Level Masks",
    "Page": 0,
    "Table": {
        31: {
            7: {
                "Name": "CdbCmdCompleteMask2",
                "Description": "Mask bit for CdbCmdCompleteFlag2",
                "Type": ["RW", "Adv"],
            },
            6: {
                "Name": "CdbCmdCompleteMask1",
                "Description": "Mask bit for CdbCmdCompleteFlag1",
                "Type": ["RW", "Adv"],
            },
            (5, 3): {"Name": "Reserved", "Description": "Reserved"},
            2: {
                "Name": "DataPathFirmwareErrorMask",
                "Description": "Mask bit for DataPathFirmwareErrorFlag",
                "Type": ["RW", "Adv"],
            },
            1: {
                "Name": "ModuleFirmwareErrorMask",
                "Description": "Mask bit for ModuleFirmwareErrorFlag",
                "Type": ["RW", "Adv"],
            },
            0: {
                "Name": "ModuleStateChangedMask",
                "Description": "Mask bit for ModuleStateChangedFlag",
                "Type": ["RW", "Rqd"],
            },
        },
        32: {
            7: {
                "Name": "VccMonLowWarningMask",
                "Description": "Mask bit for VccMonLowWarningFlag",
                "Type": ["RW", "Adv"],
            },
            6: {
                "Name": "VccMonHighWarningMask",
                "Description": "Mask bit for VccMonHighWarningFlag",
                "Type": ["RW", "Adv"],
            },
            5: {
                "Name": "VccMonLowAlarmMask",
                "Description": "Mask bit for VccMonLowAlarmFlag",
                "Type": ["RW", "Adv"],
            },
            4: {
                "Name": "VccMonHighAlarmMask",
                "Description": "Mask bit for VccMonHighAlarmFlag",
                "Type": ["RW", "Adv"],
            },
            3: {
                "Name": "TempMonLowWarningMask",
                "Description": "Mask bit for TempMonLowWarningFlag",
                "Type": ["RW", "Adv"],
            },
            2: {
                "Name": "TempMonHighWarningMask",
                "Description": "Mask bit for TempMonHighWarningFlag",
                "Type": ["RW", "Adv"],
            },
            1: {
                "Name": "TempMonLowAlarmMask",
                "Description": "Mask bit for TempMonLowAlarmFlag",
                "Type": ["RW", "Adv"],
            },
            0: {
                "Name": "TempMonHighAlarmMask",
                "Description": "Mask bit for TempMonHighAlarmFlag",
                "Type": ["RW", "Adv"],
            },
        },
        33: {
            7: {
                "Name": "Aux2MonLowWarningMask",
                "Description": "Mask bit for Aux2MonLowWarningFlag",
                "Type": ["RW", "Adv"],
            },
            6: {
                "Name": "Aux2MonHighWarningMask",
                "Description": "Mask bit for Aux2MonHighWarningFlag",
                "Type": ["RW", "Adv"],
            },
            5: {
                "Name": "Aux2MonLowAlarmMask",
                "Description": "Mask bit for Aux2MonLowAlarmFlag",
                "Type": ["RW", "Adv"],
            },
            4: {
                "Name": "Aux2MonHighAlarmMask",
                "Description": "Mask bit for Aux2MonHighAlarmFlag",
                "Type": ["RW", "Adv"],
            },
            3: {
                "Name": "Aux1MonLowWarningMask",
                "Description": "Mask bit for Aux1MonLowWarningFlag",
                "Type": ["RW", "Adv"],
            },
            2: {
                "Name": "Aux1MonHighWarningMask",
                "Description": "Mask bit for Aux1MonHighWarningFlag",
                "Type": ["RW", "Adv"],
            },
            1: {
                "Name": "Aux1MonLowAlarmMask",
                "Description": "Mask bit for Aux1MonLowAlarmFlag",
                "Type": ["RW", "Adv"],
            },
            0: {
                "Name": "Aux1MonHighAlarmMask",
                "Description": "Mask bit for Aux1MonHighAlarmFlag",
                "Type": ["RW", "Adv"],
            },
        },
        34: {
            7: {
                "Name": "CustomMonLowWarningMask",
                "Description": "Mask bit for CustomMonLowWarningFlag",
                "Type": ["RW", "Adv"],
            },
            6: {
                "Name": "CustomMonHighWarningMask",
                "Description": "Mask bit for CustomMonHighWarningFlag",
                "Type": ["RW", "Adv"],
            },
            5: {
                "Name": "CustomMonLowAlarmMask",
                "Description": "Mask bit for CustomMonLowAlarmFlag",
                "Type": ["RW", "Adv"],
            },
            4: {
                "Name": "CustomMonHighAlarmMask",
                "Description": "Mask bit for CustomMonHighAlarmFlag",
                "Type": ["RW", "Adv"],
            },
            3: {
                "Name": "Aux3MonLowWarningMask",
                "Description": "Mask bit for Aux3MonLowWarningFlag",
                "Type": ["RW", "Adv"],
            },
            2: {
                "Name": "Aux3MonHighWarningMask",
                "Description": "Mask bit for Aux3MonHighWarningFlag",
                "Type": ["RW", "Adv"],
            },
            1: {
                "Name": "Aux3MonLowAlarmMask",
                "Description": "Mask bit for Aux3MonLowAlarmFlag",
                "Type": ["RW", "Adv"],
            },
            0: {
                "Name": "Aux3MonHighAlarmMask",
                "Description": "Mask bit for Aux3MonHighAlarmFlag",
                "Type": ["RW", "Adv"],
            },
        },
        35: {(7, 0): {"Name": "Reserved[1]", "Description": "Reserved for Masks"}},
        36: {(7, 0): {"Name": "Custom[1]", "Description": "Module level Masks"}},
    },
}
