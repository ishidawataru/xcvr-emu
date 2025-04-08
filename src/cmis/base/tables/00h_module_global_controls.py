info = {
    "Name": "ModuleGlobalControls",
    "Description": "CMIS v5.2 8.11 Module Global Controls",
    "Page": 0,
    "Table": {
        26: {
            7: {
                "Name": "BankBroadcastEnable",
                "Description": "Enables or disables bank broadcast for lane-banked pages.",
                "Details": [
                    "When BankBroadcastEnable is set, a WRITE to a control register in any bank of a lane-banked page is executed as a bank broadcast.",
                    "A bank broadcast is a virtually simultaneous and atomic WRITE of the same value to the same register and the same page, in all supported banks.",
                    "The module ensures a generalized broadcast register readback condition.",
                ],
                "Advertisement": "01h:156.7",
                "Type": ["RW", "Adv"],
                "Values": {
                    0: ("Bank broadcast for lane-banked pages disabled", "DISABLED"),
                    1: ("Bank broadcast for lane-banked pages enabled", "ENABLED"),
                },
            },
            6: {
                "Name": "LowPwrAllowRequestHW",
                "Description": "Enables evaluation of the LowPwrRequestHW hardware signal.",
                "Details": [
                    "Evaluation of LowPwrRequestHW is enabled by default, allowing the host to request start-up to halt in Low Power mode."
                ],
                "Type": ["RW", "Rqd"],
                "Values": {
                    0: ("Module ignores the LowPwrRequestHW signal", "IGNORE"),
                    1: (
                        "Module evaluates the LowPwrRequestHW signal (default)",
                        "EVALUATE",
                    ),
                },
            },
            5: {
                "Name": "SquelchMethodSelect",
                "Description": "Selects the method of squelching for Tx output.",
                "Advertisement": "00h:156.5-4",
                "Notes": [
                    "Method to choose depends on interface standard used.",
                    "See Table 8-45 for SquelchMethodSelect capability advertising.",
                ],
                "Type": ["RW", "Adv"],
                "Values": {
                    0: ("Squelching of Tx output reduces OMA", "REDUCES_OMA"),
                    1: ("Squelching of Tx output reduces Pav", "REDUCES_PAV"),
                },
            },
            4: {
                "Name": "LowPwrRequestSW",
                "Description": "Requests the module to stay in, or to return to, Low Power mode.",
                "Notes": ["See Table 6-12 and section 6.3.2.4 for more information."],
                "Type": ["RW", "Rqd"],
                "Values": {
                    0: ("No request", "NO_REQUEST"),
                    1: ("Request for Low Power mode", "LOW_POWER_MODE"),
                },
            },
            3: {
                "Name": "SoftwareReset",
                "Description": "Trigger bit that causes the module to be reset when 1b is written.",
                "Details": [
                    "The effect of a SoftwareReset trigger is the same as asserting the Reset hardware signal for the appropriate hold time, followed by its de-assertion."
                ],
                "Type": ["WO/SC", "Rqd"],
                "Values": {
                    0: ("No action", "NO_ACTION"),
                    1: ("Software reset", "RESET"),
                },
            },
            (2, 0): {"Name": "Custom", "Description": "Custom"},
            (7, 0): {"Name": "ModuleGlobalControls"},  # alias
        },
        (27, 28): {"Name": "Reserved", "Description": "Reserved"},
        (29, 30): {"Name": "Custom", "Description": "Custom"},
    },
}
