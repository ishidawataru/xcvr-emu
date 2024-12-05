info = {
    "Name": "ConfigurationCommandStatusRegisters",
    "Description": "CMIS v5.2 Table 8-83 Configuration Command Status registers (Page 11h)",
    "Page": 0x11,
    "Table": {
        "ConfigStatusLane": {
            "Description": "Configuration Command Execution / Result Status for the Data Path of host lane <i>, during and after the most recent configuration command.",
            "Type": ["RO", "Rqd"],
            "Values": {
                0x0: (
                    "No status information available (initial register value)",
                    "UNDEFINED",
                ),
                0x1: (
                    "Positive Result Status: The last accepted configuration command has been completed successfully",
                    "SUCCESS",
                ),
                0x2: (
                    "Configuration rejected: unspecific validation failure",
                    "REJECTED",
                ),
                0x3: (
                    "Configuration rejected: invalid AppSel code",
                    "REJECTED_INVALID_APP_SEL",
                ),
                0x4: (
                    "Configuration rejected: invalid all lanes for AppSel",
                    "REJECTED_INVALID_DATA_PATH",
                ),
                0x5: (
                    "Configuration rejected: invalid SI control settings",
                    "REJECTED_INVALID_SI",
                ),
                0x6: (
                    "Configuration rejected: some lanes not in DPDeactivated",
                    "REJECTED_LANES_IN_USE",
                ),
                0x7: (
                    "Configuration rejected: lanes are only subset of DataPath",
                    "REJECTED_PARTIAL_DATA_PATH",
                ),
                (0x8, 0xB): ("Other validation failures", "RESERVED"),
                0xC: (
                    "Execution Status: A configuration command is still being processed by the module; a new configuration command is ignored for this lane while ConfigInProgress.",
                    "IN_PROGRESS",
                ),
                (0xD, 0xF): ("Custom", "CUSTOM"),
            },
        },
        (202, 205): {
            range(0, 32, 4): {
                "Template": "ConfigStatusLane",
            }
        },
    },
}
