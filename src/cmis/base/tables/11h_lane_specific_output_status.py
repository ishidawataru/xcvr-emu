info = {
    "Name": "LaneSpecificOutputStatus",
    "Description": "CMIS v5.2 Table 8-78 Lane-Specific Output Status (Page 11h)",
    "Page": 0x11,
    "Table": {
        "OutputStatus": {
            "Description": "Output status for lane <i>",
            "Type": ["RO", "Rqd"],
            "Values": {
                0: ("Output signal invalid or muted", "INVALID_OR_MUTED"),
                1: ("Output signal valid", "VALID"),
            },
        },
        "OutputStatusRx": {
            "Template": "OutputStatus",
        },
        "OutputStatusTx": {
            "Template": "OutputStatus",
        },
        132: {range(0, 8): {"Template": "OutputStatusRx"}},
        133: {range(0, 8): {"Template": "OutputStatusTx"}},
    },
}
