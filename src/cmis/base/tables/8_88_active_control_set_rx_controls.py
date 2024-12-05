info = {
    "Name": "ActiveControlSetProvisionedRxControls",
    "Description": "CMIS v5.2 Table 8-88 Active Control Set, Provisioned Rx Controls (Page 11h)",
    "Page": 0x11,
    "Table": {
        "CDREnableRx": {
            "Description": "Enable or bypass CDR for lane <i>",
            "Type": ["RO", "Adv"],
            "Values": {
                0: ("CDR bypassed", "BYPASSED"),
                1: ("CDR enabled", "ENABLED"),
            },
            "Advertisement": "01h:162.1",
        },
        "RxControls": {
            0: {
                range(0, 8): {"Template": "CDREnableRx"},
            },
            (1, 4): {
                range(0, 32, 4): {
                    "Name": "OutputEqPreCursorTargetRx",
                    "Description": "Rx output pre-cursor equalization for lane <i> as defined in Table 6-7",
                    "Type": ["RO", "Adv"],
                    "Advertisement": "01h:162.4-3",
                }
            },
            (5, 8): {
                range(0, 32, 4): {
                    "Name": "OutputEqPostCursorTargetRx",
                    "Description": "Rx output post-cursor equalization for lane <i> as defined in Table 6-7",
                    "Type": ["RO", "Adv"],
                    "Advertisement": "01h:162.4-3",
                },
            },
            (9, 12): {
                range(0, 32, 4): {
                    "Name": "OutputAmplitudeTargetRx",
                    "Description": "Rx output amplitude level for lane <i> as defined in Table 6-8",
                    "Type": ["RO", "Adv"],
                    "Advertisement": "01h:162.2",
                },
            },
        },
        (222, 234): {
            "Template": "RxControls",
            "Prefix": "ACS::",
        },
    },
}
