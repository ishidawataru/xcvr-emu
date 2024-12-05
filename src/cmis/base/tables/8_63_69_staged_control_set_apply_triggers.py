info = {
    "Name": "StagedControlSetApplyTriggers",
    "Description": "CMIS v5.2 Table 8-63/69 Staged Control Set 0/1, Apply Triggers (Page 10h)",
    "Page": 0x10,
    "Table": {
        "ApplyTriggers": {
            0: {
                range(0, 8): {
                    "Name": "ApplyDPInitLane",
                    "Description": "ApplyDPInitLane<i>: Trigger the Provision procedure using the Staged Control Set settings for host lane <i>, with feedback provided in the associated ConfigStatusLane<i> field",
                    "Type": ["WO", "Rqd"],
                    "Values": {
                        0: ("No action for host lane <i>", "NO_ACTION"),
                        1: (
                            "Trigger the Provision procedure for host lane <i>",
                            "PROVISION",
                        ),
                    },
                }
            },
            1: {
                range(0, 8): {
                    "Name": "ApplyImmediateLane",
                    "Description": "ApplyImmediateLane<i>: Trigger the Provision or the Provision-and-Commission procedure using the Staged Control Set 0 settings for host lane <i>, with feedback provided in the associated ConfigStatusLane<i> field",
                    "Type": ["WO", "Cnd"],
                    "Values": {
                        0: ("No action for host lane <i>", "NO_ACTION"),
                        1: (
                            "Trigger the Provision or Provision-and-Commission procedure for host lane <i>",
                            "PROVISION_AND_COMMISSION",
                        ),
                    },
                }
            },
        },
        (143, 144): {"Template": "ApplyTriggers", "Prefix": "SCS0::"},
        (178, 179): {"Template": "ApplyTriggers", "Prefix": "SCS1::"},
    },
}
