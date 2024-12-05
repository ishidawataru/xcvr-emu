info = {
    "Name": "LaneSpecificDirectEffectControlFields",
    "Description": "CMIS v5.2 Table 8-62 Lane-specific Direct Effect Control Fields (Page 10h)",
    "Page": 0x10,
    "Table": {
        129: {
            range(0, 8): {
                "Name": "InputPolarityFlipTx",
                "Description": "Control for Tx input polarity flip for lane <i>",
                "Type": ["RW", "Adv"],
                "Values": {
                    0: ("No Tx input polarity flip for lane", "NO_FLIP"),
                    1: ("Tx input polarity flip for lane", "FLIP"),
                },
                "Advertisement": "01h:155.0",
            },
        },
        130: {
            range(0, 8): {
                "Name": "OutputDisableTx",
                "Description": "Control for Tx output enable/disable for lane <i>",
                "Type": ["RW", "Adv"],
                "Values": {
                    0: ("Tx output enabled for media lane", "ENABLED"),
                    1: ("Tx output disabled for media lane", "DISABLED"),
                },
                "Advertisement": "01h:155.1",
            },
        },
        131: {
            range(0, 8): {
                "Name": "AutoSquelchDisableTx",
                "Description": "Control for automatic Tx output squelching for lane <i>",
                "Type": ["RW", "Adv"],
                "Values": {
                    0: (
                        "Automatic Tx output squelching enabled for media lane",
                        "ENABLED",
                    ),
                    1: (
                        "Automatic Tx output squelching disabled for media lane",
                        "DISABLED",
                    ),
                },
                "Advertisement": "01h:155.2",
            },
        },
        132: {
            range(0, 8): {
                "Name": "OutputSquelchForceTx",
                "Description": "Force Tx output squelching for lane <i>",
                "Type": ["RW", "Adv"],
                "Values": {
                    0: ("No impact on Tx output for media lane", "NO_IMPACT"),
                    1: ("Tx output squelched for media lane", "SQUELCHED"),
                },
                "Advertisement": "01h:155.3",
            },
        },
        133: {
            "Name": "Reserved[1]",
        },
        134: {
            range(0, 8): {
                "Name": "AdaptiveInputEqFreezeTx",
                "Description": "Control for freezing adaptive Tx Input Equalization for lane <i>",
                "Type": ["RW", "Adv"],
                "Values": {
                    0: (
                        "No impact on Tx input adaptation behavior for lane",
                        "NO_IMPACT",
                    ),
                    1: (
                        "Tx input equalization adaptation frozen at last value for lane",
                        "FROZEN",
                    ),
                },
                "Advertisement": "01h:161.4",
            },
        },
        "AdaptiveInputEqStoreTx": {
            "Description": "Tx Input Equalizer Adaptation Store location for lane <i>",
            "Type": ["WO", "Adv"],
            "Values": {
                0: ("Reserved", "RESERVED"),
                1: ("Store to recall buffer 1", "STORE_BUFFER_1"),
                2: ("Store to recall buffer 2", "STORE_BUFFER_2"),
                3: ("Reserved", "RESERVED"),
            },
            "Advertisement": "01h:161.5-6",
        },
        (135, 136): {
            range(0, 16, 2): {
                "Template": "AdaptiveInputEqStoreTx",
            },
        },
        137: {
            range(0, 8): {
                "Name": "OutputPolarityFlipRx",
                "Description": "Control for Rx output polarity flip for lane <i>",
                "Type": ["RW", "Adv"],
                "Values": {
                    0: ("No Rx output polarity flip for lane", "NO_FLIP"),
                    1: ("Rx output polarity flip for lane", "FLIP"),
                },
                "Advertisement": "01h:156.0",
            },
        },
        138: {
            range(0, 8): {
                "Name": "OutputDisableRx",
                "Description": "Control for Rx output enable/disable for lane <i>",
                "Type": ["RW", "Adv"],
                "Values": {
                    0: ("Rx output enabled for lane", "ENABLED"),
                    1: ("Rx output disabled for lane", "DISABLED"),
                },
                "Advertisement": "01h:156.1",
            },
        },
        139: {
            range(0, 8): {
                "Name": "AutoSquelchDisableRx",
                "Description": "Control for automatic Rx output squelching for host lane <i>",
                "Type": ["RW", "Adv"],
                "Values": {
                    0: (
                        "Automatic Rx output squelching enabled for host lane",
                        "ENABLED",
                    ),
                    1: (
                        "Automatic Rx output squelching disabled for host lane",
                        "DISABLED",
                    ),
                },
                "Advertisement": "01h:156.2",
            },
        },
        (140, 142): {
            "Name": "Reserved",
            "Description": "Reserved[3]",
            "Type": ["RO"],
        },
    },
}
