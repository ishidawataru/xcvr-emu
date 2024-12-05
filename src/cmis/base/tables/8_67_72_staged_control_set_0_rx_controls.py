info = {
    "Name": "StagedControlSetRxControls",
    "Description": "CMIS v5.2 Table 8-67 Staged Control Set 0/1, Rx Controls (Page 10h)",
    "Page": 0x10,
    "Table": {
        "RxControls": {
            0: {
                range(0, 8): {
                    "Name": "CDREnableRx",
                    "Description": "CDREnableRx<i>: CDR enable for host lane <i>",
                    "Type": ["RW", "Adv"],
                    "Values": {
                        0: ("CDR bypassed", "BYPASSED"),
                        1: ("CDR enabled", "ENABLED"),
                    },
                    "Advertisement": "01h:162.1",
                },
            },
            (1, 4): {
                range(0, 32, 4): {
                    "Name": "OutputEqPreCursorTargetRx",
                    "Description": "SCS::OutputPreCursorTargetRx<i>: Rx output equalization pre-cursor target for host lane <i>",
                    "Type": ["RW", "Adv"],
                    "Advertisement": "01h:162.4-3",
                }
            },
            (5, 8): {
                range(0, 32, 4): {
                    "Name": "OutputEqPostCursorTargetRx",
                    "Description": "SCS::OutputPostCursorTargetRx<i>: Rx output equalization post-cursor target for host lane <i>",
                    "Type": ["RW", "Adv"],
                    "Advertisement": "01h:162.4-3",
                }
            },
            (9, 12): {
                range(0, 32, 4): {
                    "Name": "OutputAmplitudeTargetRx",
                    "Description": "SCS::OutputAmplitudeTargetRx<i>: Rx output amplitude target for host lane <i>",
                    "Type": ["RW", "Adv"],
                    "Advertisement": "01h:162.2",
                }
            },
            # match with RxControls defined in 8_88_active_control_set_rx_controls.py
            #            (13, 14): {
            #                "Name": "Reserved[2]",
            #            },
        },
        (161, 175): {"Template": "RxControls", "Prefix": "SCS0::"},
        (196, 210): {"Template": "RxControls", "Prefix": "SCS1::"},
    },
}
