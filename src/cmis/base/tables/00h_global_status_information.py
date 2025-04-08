info = {
    "Name": "GlobalStatusInformation",
    "Description": "CMIS v5.2 8.6 Global Status Information page 128",
    "Page": 0,
    "Table": {
        3: {
            (7, 4): {"Name": "Reserved", "Description": "Reserved"},
            (3, 1): {
                "Name": "ModuleState",
                "Description": "Current Module State (see Table 8-7 for encoding and section 6.3.2 for a description of the meaning of ModuleState)",
                "Notes": [
                    "Flat memory modules always report ModuleReady.",
                    "Not all states of the Module State Machine are observable.",
                ],
                "Type": ["RO", "Rqd"],
                "Values": {
                    0b000: ("Reserved", "RESERVED"),
                    0b001: ("ModuleLowPwr", "MODULE_LOW_PWR"),
                    0b010: ("ModulePwrUp", "MODULE_PWR_UP"),
                    0b011: ("ModuleReady", "MODULE_READY"),
                    0b100: ("ModulePwrDn", "MODULE_PWR_DN"),
                    0b101: ("ModuleFault", "MODULE_FAULT"),
                    0b110: ("Reserved", "RESERVED"),
                    0b111: ("Reserved", "RESERVED"),
                },
            },
            0: {
                "Name": "InterruptDeasserted",
                "Description": "Status of Interrupt output signal",
                "Type": ["RO"],
                "Values": {
                    0: ("Interrupt asserted", "ASSERTED"),
                    1: ("Interrupt not asserted (default)", "NOT_ASSERTED"),
                },
            },
        }
    },
}
