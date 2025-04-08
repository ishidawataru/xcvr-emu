info = {
    "Name": "StagedControlSetTxControls",
    "Description": "CMIS v5.2 Table 8-66/71 Staged Control Set 0/1, Tx Controls (Page 10h)",
    "Page": 0x10,
    "Table": {
        "AdaptiveInputEqEnableTx": {
            "Description": "SCS0/1::AdaptiveInputEqEnableTx<i>: Adaptive input equalizer for host lane <i>",
            "Type": ["RW", "Adv"],
            "Values": {
                0: ("Use manual fixed equalizer", "FIXED"),
                1: ("Enable adaptive Tx input equalization", "ADAPTIVE"),
            },
        },
        "AdaptiveInputEqRecallTx": {
            "Description": "SCS0/1::AdaptiveInputEqRecallTx<i>: Recall stored Tx input equalizer adaptation settings for host lane <i>",
            "Type": ["RW", "Adv"],
            "Values": {
                0b00: ("Do not recall", "DO_NOT_RECALL"),
                0b01: ("Recall buffer 1", "RECALL_BUFFER_1"),
                0b10: ("Recall buffer 2", "RECALL_BUFFER_2"),
                0b11: ("Reserved", "RESERVED"),
            },
        },
        "FixedInputEqTargetTx": {
            "Description": "SCS0/1::FixedInputEqTargetTx<i>: Manual fixed Tx input equalizer control for host lane <i>",
            "Type": ["RW", "Adv"],
        },
        "CDREnableTx": {
            "Description": "SCS0/1::CDREnableTx<i>: CDR enable for host lane <i>",
            "Type": ["RW", "Adv"],
            "Values": {
                0: ("CDR bypassed", "BYPASSED"),
                1: ("CDR enabled", "ENABLED"),
            },
        },
        "TxControl": {
            0: {
                range(0, 8): {"Template": "AdaptiveInputEqEnableTx"},
            },
            (1, 2): {
                range(0, 16, 2): {
                    "Template": "AdaptiveInputEqRecallTx",
                },
            },
            (3, 6): {
                range(0, 32, 4): {
                    "Template": "FixedInputEqTargetTx",
                },
            },
            7: {
                range(0, 8): {"Template": "CDREnableTx"},
            },
        },
        (153, 160): {
            "Template": "TxControl",
            "Prefix": "SCS0::",
        },
        (188, 195): {
            "Template": "TxControl",
            "Prefix": "SCS1::",
        },
    },
}
