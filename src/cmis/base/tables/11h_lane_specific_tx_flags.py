info = {
    "Name": "LaneSpecificTxFlags",
    "Description": "CMIS v5.2 Table 8-80 Lane-Specific Tx Flags (Page 11h)",
    "Page": 0x11,
    "Table": {
        135: {
            range(0, 8): {
                "Name": "FailureFlagTx",
                "Description": "Latched Tx Failure Flag, affecting media lane <i>. This Flag indicates an internal failure that causes an unspecified malfunction in the Tx facility used by media lane <i>.",
                "Type": ["RO/COR", "Adv"],
                "Advertisement": "01h:157.0",
            }
        },
        136: {
            range(0, 8): {
                "Name": "LOSFlagTx",
                "Description": "Latched Tx LOS Flag, host lane <i>",
                "Type": ["RO/COR", "Adv"],
                "Advertisement": "01h:157.1",
            },
        },
        137: {
            range(0, 8): {
                "Name": "CDRLOLFlagTx",
                "Description": "Latched Tx CDR LOL Flag, host lane <i>",
                "Type": ["RO/COR", "Adv"],
                "Advertisement": "01h:157.2",
            }
        },
        138: {
            range(0, 8): {
                "Name": "AdaptiveInputEqFailFlagTx",
                "Description": "Latched Tx Adaptive Input Eq Fail, host lane <i>",
                "Type": ["RO/COR", "Adv"],
                "Advertisement": "01h:157.3",
            }
        },
        139: {
            range(0, 8): {
                "Name": "OpticalPowerHighAlarmFlagTx",
                "Description": "Latched Tx output power High Alarm, media lane <i>",
                "Type": ["RO/COR", "Adv"],
                "Advertisement": "01h:160.1",
            }
        },
        140: {
            range(0, 8): {
                "Name": "OpticalPowerLowAlarmFlagTx",
                "Description": "Latched Tx output power Low Alarm, media lane <i>",
                "Type": ["RO/COR", "Adv"],
                "Advertisement": "01h:160.1",
            }
        },
        141: {
            range(0, 8): {
                "Name": "OpticalPowerHighWarningFlagTx",
                "Description": "Latched Tx output power high warning, media lane <i>",
                "Type": ["RO/COR", "Adv"],
                "Advertisement": "01h:160.1",
            }
        },
        142: {
            range(0, 8): {
                "Name": "OpticalPowerLowWarningFlagTx",
                "Description": "Latched Tx output power low warning, media lane <i>",
                "Type": ["RO/COR", "Adv"],
                "Advertisement": "01h:160.1",
            }
        },
        143: {
            range(0, 8): {
                "Name": "LaserBiasHighAlarmFlagTx",
                "Description": "Latched Tx Bias High Alarm, media lane <i>",
                "Type": ["RO/COR", "Adv"],
                "Advertisement": "01h:160.0",
            }
        },
        144: {
            range(0, 8): {
                "Name": "LaserBiasLowAlarmFlagTx",
                "Description": "Latched Tx Bias Low Alarm, media lane <i>",
                "Type": ["RO/COR", "Adv"],
                "Advertisement": "01h:160.0",
            }
        },
        145: {
            range(0, 8): {
                "Name": "LaserBiasHighWarningFlagTx",
                "Description": "Latched Tx Bias High warning, media lane <i>",
                "Type": ["RO/COR", "Adv"],
                "Advertisement": "01h:160.0",
            }
        },
        146: {
            range(0, 8): {
                "Name": "LaserBiasLowWarningFlagTx",
                "Description": "Latched Tx Bias Low Warning, media lane <i>",
                "Type": ["RO/COR", "Adv"],
                "Advertisement": "01h:160.0",
            }
        },
    },
}
