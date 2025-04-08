info = {
    "Name": "RxFlags",
    "Description": "CMIS v5.2 Table 8-81 Rx Flags (Page 11h)",
    "Page": 0x11,
    "Table": {
        147: {
            range(0, 8): {
                "Name": "LOSFlagRx",
                "Description": "Latched Rx LOS Flag, media lane <i>",
                "Type": ["RO/COR", "Adv"],
                "Advertisement": "01h:158.1",
            }
        },
        148: {
            range(0, 8): {
                "Name": "CDRLOLFlagRx",
                "Description": "Latched Rx CDR LOL Flag, media lane <i>",
                "Type": ["RO/COR", "Adv"],
                "Advertisement": "01h:158.2",
            }
        },
        149: {
            range(0, 8): {
                "Name": "OpticalPowerHighAlarmFlagRx",
                "Description": "Latched Rx input power High Alarm, media lane <i>",
                "Type": ["RO/COR", "Adv"],
                "Advertisement": "01h:160.2",
            }
        },
        150: {
            range(0, 8): {
                "Name": "OpticalPowerLowAlarmFlagRx",
                "Description": "Latched Rx input power Low Alarm, media lane <i>",
                "Type": ["RO/COR", "Adv"],
                "Advertisement": "01h:160.2",
            }
        },
        151: {
            range(0, 8): {
                "Name": "OpticalPowerHighWarningFlagRx",
                "Description": "Latched Rx input power High Warning, media lane <i>",
                "Type": ["RO/COR", "Adv"],
                "Advertisement": "01h:160.2",
            }
        },
        152: {
            range(0, 8): {
                "Name": "OpticalPowerLowWarningFlagRx",
                "Description": "Latched Rx input power Low Warning, media lane <i>",
                "Type": ["RO/COR", "Adv"],
                "Advertisement": "01h:160.2",
            },
        },
        153: {
            range(0, 8): {
                "Name": "OutputStatusChangedFlagRx",
                "Description": "Latched Output Status Changed Flag for Rx host lane <i>",
                "Type": ["RO/COR", "Rqd"],
            },
        },
    },
}
