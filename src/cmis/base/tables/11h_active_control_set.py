info = {
    "Name": "ActiveControlSetProvisionedDataPathConfiguration",
    "Description": "CMIS v5.2 Table 8-86 Active Control Set, Provisioned Data Path Configuration (Page 11h)",
    "Page": 0x11,
    "Table": {
        "DPConfigLane": {
            (7, 4): {
                "Name": "AppSelCode",
                "Description": "Defines the Application assigned to the Data Path containing lane <i> by reference to the Application Descriptor of that Application.",
                "Type": ["RO", "Rqd"],
            },
            (3, 1): {
                "Name": "DataPathID",
                "Description": "Index of first lane in the Data Path containing lane <i>.",
                "Type": ["RO", "Rqd"],
            },
            0: {
                "Name": "ExplicitControl",
                "Description": "Specifies if lane <i> SI settings are application dependent or host-defined.",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0: (
                        "Use Application-dependent settings for lane <i>",
                        "APPLICATION_DEPENDENT",
                    ),
                    1: ("Host defined", "HOST_DEFINED"),
                },
            },
        },
        range(206, 214): {
            "Template": "DPConfigLane",
            "Prefix": "ACS::",
        },
    },
}
