info = {
    "Name": "DataPathInitializationControl",
    "Description": "CMIS v5.2 Table 8-61 Data Path initialization control (Page 10h:128)",
    "Page": 0x10,
    "Table": {
        128: {
            range(0, 8): {
                "Name": "DPDeinitLane",
                "Description": "Data Path initialization control for host lane",
                "Type": ["RW", "Rqd"],
                "Values": {
                    0: (
                        "Initialize the Data Path associated with host lane",
                        "INITIALIZE",
                    ),
                    1: (
                        "Deinitialize the Data Path associated with host lane",
                        "DEINITIALIZE",
                    ),
                },
            },
        },
    },
}
