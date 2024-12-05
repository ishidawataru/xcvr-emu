info = {
    "Name": "LaneSpecificStateChangedFlags",
    "Description": "CMIS v5.2 Table 8-79 Lane-Specific State Changed Flags (Page 11h)",
    "Page": 0x11,
    "Table": {
        134: {
            range(0, 8): {
                "Name": "DPStateChangedFlag",
                "Description": "Latched Data Path State Changed Flag for host lane <i>",
                "Type": ["RO/COR", "Rqd"],
            }
        },
    },
}
