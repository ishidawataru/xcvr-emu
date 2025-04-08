info = {
    "Name": "CdbStatusFields",
    "Description": "CMIS v5.2 8.13 CdbStatus fields and 8.14 Bit definitions within CdbStatus fields",
    "Page": 0,
    "Table": {
        range(37, 39): {
            "Template": "CdbStatus",
            "Description": "Status of the most recent CDB command in CDB instance 1",
            "Type": ["RO", "Adv"],
        },
        "CdbStatus": {
            7: {
                "Name": "CdbIsBusy",
                "Description": "Indicates whether the module is busy or idle.",
                "Values": {
                    0: ("Module idle, host can write", "IDLE"),
                    1: ("Module busy, host needs to wait", "BUSY"),
                },
            },
            6: {
                "Name": "CdbHasFailed",
                "Description": "Indicates if there was a failure after the module has completed execution of the last CDB command.",
                "Values": {
                    0: ("Last triggered CDB command completed successfully", "SUCCESS"),
                    1: ("Last triggered CDB command failed", "FAILED"),
                },
            },
            (5, 0): {
                "Name": "CdbCommandResult",
                "Description": "Provides detailed classification for the status of the last CDB command.",
                "Values": {
                    "IN_PROGRESS": {
                        0x00: ("Reserved", "RESERVED"),
                        0x01: ("Command is captured but not processed", "CAPTURED"),
                        0x02: ("Command checking is in progress", "CHECKING"),
                        0x03: ("Command execution is in progress", "EXECUTING"),
                        (0x04, 0x2F): ("Reserved", "RESERVED"),
                        (0x30, 0x3F): ("Custom", "CUSTOM"),
                    },
                    "SUCCESS": {
                        0x00: ("Reserved", "RESERVED"),
                        0x01: ("Command completed successfully", "COMPLETED"),
                        0x02: ("Reserved", "RESERVED"),
                        0x03: ("Previous CMD was ABORTED by CMD Abort", "ABORTED"),
                        (0x04, 0x1F): ("Reserved", "RESERVED"),
                        (0x20, 0x2F): ("Reserved", "RESERVED"),
                        (0x30, 0x3F): ("Custom", "CUSTOM"),
                    },
                    "FAILED": {
                        0x00: ("Reserved", "RESERVED"),
                        0x01: ("CMDID unknown", "UNKNOWN_CMDID"),
                        0x02: (
                            "Parameter range error or parameter not supported",
                            "PARAM_ERROR",
                        ),
                        0x03: (
                            "Previous CMD was not properly ABORTED (by CMD Abort)",
                            "NOT_ABORTED",
                        ),
                        0x04: ("Command checking time out", "TIMEOUT"),
                        0x05: ("CdbChkCode Error", "CHKCODE_ERROR"),
                        0x06: (
                            "Password related error (command specific meaning)",
                            "PASSWORD_ERROR",
                        ),
                        0x07: (
                            "Command not compatible with operating status",
                            "INCOMPATIBLE_STATUS",
                        ),
                        (0x08, 0x0F): (
                            "Reserved for STS command checking error",
                            "STS_ERROR",
                        ),
                        (0x10, 0x1F): ("Reserved", "RESERVED"),
                        (0x20, 0x2F): (
                            "For individual STS command or task error",
                            "STS_TASK_ERROR",
                        ),
                        (0x30, 0x3F): ("Custom", "CUSTOM"),
                    },
                },
            },
        },
    },
}
