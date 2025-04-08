info = {
    "Name": "LaneAssociatedDataPathStates",
    "Description": "CMIS v5.2 Table 8-76 Lane-associated Data Path States (Page 11h)",
    "Page": 0x11,
    "Table": {
        (128, 131): {
            range(0, 32, 4): {
                "Template": "DPStateHostLane",
            }
        },
        "DPStateHostLane": {
            "Description": "Data Path State of host lane <i> (see Table 8-77)",
            "Type": ["RO", "Rqd"],
            "Values": {
                0x0: ("Reserved", "RESERVED"),
                0x1: ("DPDeactivated (or unused lane)", "DPDEACTIVATED"),
                0x2: ("DPInit", "DPINIT"),
                0x3: ("DPDeinit", "DPDEINIT"),
                0x4: ("DPActivated", "DPACTIVATED"),
                0x5: ("DPTxTurnOn", "DPTXTURNON"),
                0x6: ("DPTxTurnOff", "DPTXTRUNOFF"),
                0x7: ("DPInitialized", "DPINITIALIZED"),
                0x8: ("Reserved", "RESERVED"),
                0xF: ("Reserved", "RESERVED"),
            },
        },
    },
}
