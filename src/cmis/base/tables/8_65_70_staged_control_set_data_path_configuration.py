info = {
    "Name": "StagedControlSetDataPathConfiguration",
    "Description": "CMIS v5.2 Table 8-65/70 Staged Control Set 0/1, Data Path Configuration (Page 10h)",
    "Page": 0x10,
    "Table": {
        "DPConfigLane": {
            (7, 4): {
                "Name": "AppSelCode",
                "Description": "SCS<i>::AppSelCodeLane<i>: Stores the AppSel code of the Descriptor of the Application. If the lane <i> is not part of a Data Path, the value is assigned as NULL (0000b).",
                "Type": ["RW", "Rqd"],
            },
            (3, 1): {
                "Name": "DataPathID",
                "Description": "SCS<i>::DataPathIDLane<i>: Stores the DataPathID of the Data Path. If the lane <i> is not part of a Data Path, the value is ignored.",
                "Type": ["RW", "Rqd"],
            },
            0: {
                "Name": "ExplicitControl",
                "Description": "SCS<i>::ExplicitControlLane<i>: Determines whether the lane uses Application-dependent settings or Staged Control Set 0 control values.",
                "Type": ["RW", "Rqd"],
                "Values": {
                    0: (
                        "Use Application-dependent settings for lane <i>",
                        "APPLICATION_DEPENDENT",
                    ),
                    1: (
                        "Use Staged Control Set 0 control values for lane <i>",
                        "STAGED_CONTROL_SET",
                    ),
                },
            },
        },
        range(145, 153): {"Template": "DPConfigLane", "Prefix": "SCS0::"},
        range(180, 188): {"Template": "DPConfigLane", "Prefix": "SCS1::"},
    },
}
