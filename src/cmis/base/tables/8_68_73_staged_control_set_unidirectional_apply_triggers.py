info = {
    "Name": "StagedControlSetUnidirectionalApplyTriggers",
    "Description": "CMIS v5.2 Table 8-68/73 Staged Control Set 0/1, Unidirectional Apply Triggers (Page 10h)",
    "Page": 0x10,
    "Table": {
        "UnidirectionalApplyTriggers": {
            0: {
                range(0, 8): {
                    "Name": "ApplyImmediateTx",
                    "Description": "ApplyImmediateTx<i>: Immediate Apply Trigger for Tx lane <i>",
                    "Type": ["WO", "Cnd"],
                    "Values": {
                        0: ("No action for host lane", "NO_ACTION"),
                        1: (
                            "Trigger the Provision-and-Commission procedure for Tx using the Staged Control Set 0 settings for host lane <i>, with feedback provided in the ConfigStatusLane<i> field",
                            "PROVISION_AND_COMMISSION",
                        ),
                    },
                },
            },
            1: {
                range(0, 8): {
                    "Name": "ApplyImmediateRx",
                    "Description": "ApplyImmediateRx<i>: Immediate Apply Trigger for Rx lane <i>",
                    "Type": ["WO", "Cnd"],
                    "Values": {
                        0: ("No action for host lane", "NO_ACTION"),
                        1: (
                            "Trigger the Provision-and-Commission procedure for Rx using the Staged Control Set 0 settings for host lane <i>, with feedback provided in the ConfigStatusLane<i> field",
                            "PROVISION_AND_COMMISSION",
                        ),
                    },
                }
            },
        },
        (176, 177): {
            "Template": "UnidirectionalApplyTriggers",
            "Prefix": "SCS0::",
        },
        (211, 212): {
            "Template": "UnidirectionalApplyTriggers",
            "Prefix": "SCS1::",
        },
    },
}
