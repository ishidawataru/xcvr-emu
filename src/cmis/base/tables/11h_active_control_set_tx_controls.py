info = {
    "Name": "ActiveControlSetProvisionedTxControls",
    "Description": "CMIS v5.2 Table 8-87 Active Control Set, Provisioned Tx Controls (Page 11h)",
    "Page": 0x11,
    "Table": {
        "AdaptiveInputEqEnableTx": {
            "Description": "Enable or disable adaptive Tx input equalizer for lane <i>",
            "Type": ["RO", "Adv"],
            "Values": {
                0: ("Use fixed Tx input equalizer for lane <i>", "FIXED"),
                1: ("Enable adaptive Tx input equalizer for lane <i>", "ADAPTIVE"),
            },
            "Advertisement": "01h:161.3",
        },
        "AdaptiveInputEqRecallTx": {
            "Description": "Recall Tx EQ settings status for lane <i>",
            "Type": ["RO", "Adv"],
            "Values": {
                0b00: ("Settings are not recalled", "DO_NOT_RECALL"),
                0b01: (
                    "Settings have been recalled from recall buffer 1",
                    "RECALL_BUFFER_1",
                ),
                0b10: (
                    "Settings have been recalled from recall buffer 2",
                    "RECALL_BUFFER_2",
                ),
                0b11: ("Reserved", "RESERVED"),
            },
            "Advertisement": "01h:161.6-5",
        },
        "FixedInputEqTargetTx": {
            "Description": "Fixed Tx input equalization for lane <i> as defined in Table 6-6",
            "Type": ["RO", "Adv"],
            "Advertisement": "01h:161.2",
        },
        "CDREnableTx": {
            "Description": "Enable or bypass CDR for lane <i>",
            "Type": ["RO", "Adv"],
            "Values": {
                0: ("CDR bypassed", "BYPASSED"),
                1: ("CDR enabled", "ENABLED"),
            },
            "Advertisement": "01h:161.1",
        },
        "TxControls": {
            0: {
                range(0, 8): {
                    "Template": "AdaptiveInputEqEnableTx",
                },
            },
            (1, 2): {
                range(0, 16, 2): {
                    "Template": "AdaptiveInputEqRecallTx",
                },
            },
            (3, 6): {
                range(0, 32, 4): {
                    "Template": "FixedInputEqTargetTx",
                }
            },
            7: {
                range(0, 8): {"Template": "CDREnableTx"},
            },
        },
        (214, 221): {
            "Template": "TxControls",
            "Prefix": "ACS::",
        },
    },
}
