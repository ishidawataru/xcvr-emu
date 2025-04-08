info = {
    "Name": "DataPathConditions",
    "Description": "CMIS v5.2 Table 8-89 Data Path Conditions (Page 11h)",
    "Page": 0x11,
    "Table": {
        235: {
            range(0, 8): {
                "Name": "DPInitPendingLane",
                "Description": (
                    "Indicates whether DPInit has not yet been executed after a successful ApplyDPInit. "
                    "If not executed, the Active Control Set content may deviate from the actual hardware configuration."
                ),
                "Type": ["RO", "Rqd"],
                "Values": {
                    0: ("DPInit not pending", "NOT_PENDING"),
                    1: (
                        "DPInit not yet executed after successful ApplyDPInit",
                        "PENDING",
                    ),
                },
            },
        },
        (236, 239): {
            "Name": "Reserved",
            "Description": "Reserved for future use",
            "Type": ["RO"],
        },
    },
}
