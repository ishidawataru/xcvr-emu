info = {
    "Name": "CDBAdvertisement",
    "Description": "CMIS v5.2 8.4.7 CDB Advertisement",
    "Page": 1,
    "Table": {
        163: {
            (7, 6): {
                "Name": "CdbInstancesSupported",
                "Description": "00b: CDB functionality not supported, 01b: One CDB instance supported, 10b: Two CDB instances supported, 11b: Reserved",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0b00: ("CDB functionality not supported", "NOT_SUPPORTED"),
                    0b01: ("One CDB instance supported", "ONE_INSTANCE"),
                    0b10: ("Two CDB instances supported", "TWO_INSTANCES"),
                    0b11: ("Reserved", "RESERVED"),
                },
            },
            5: {
                "Name": "CdbBackgroundModeSupported",
                "Description": "0b: Background CDB operation not supported, 1b: Background CDB operation supported",
                "Type": ["RO", "Cnd"],
                "Values": {
                    0: ("Background CDB operation not supported", "NOT_SUPPORTED"),
                    1: ("Background CDB operation supported", "SUPPORTED"),
                },
            },
            4: {
                "Name": "CdbAutoPagingSupported",
                "Description": "0b: Auto Paging not supported, 1b: Auto Paging and Auto Page wrap supported",
                "Type": ["RO", "Cnd"],
                "Values": {
                    0: ("Auto Paging not supported", "NOT_SUPPORTED"),
                    1: ("Auto Paging and Auto Page wrap supported", "SUPPORTED"),
                },
            },
            (3, 0): {
                "Name": "CdbMaxPagesEPL",
                "Description": "Encodes the EPL Page range or the maximum length of extended payload.",
                "Type": ["RO", "Cnd"],
                "Values": {
                    0: ("(none)", "NONE"),
                    1: ("A0h", "A0H"),
                    2: ("A0h–A1h", "A0H_A1H"),
                    3: ("A0h–A2h", "A0H_A2H"),
                    4: ("A0h–A3h", "A0H_A3H"),
                    5: ("A0h–A7h", "A0H_A7H"),
                    6: ("A0h–A8h", "A0H_A8H"),
                    7: ("A0h–Afh", "A0H_AFH"),
                },
            },
        },
        164: {
            (7, 0): {
                "Name": "CdbReadWriteLengthExtension",
                "Description": "Specifies i * 8 allowable additional number of bytes in a WRITE or READ access to an EPL CDB Page (A0h–AFh).",
                "Type": ["RO", "Cnd"],
            }
        },
        165: {
            7: {
                "Name": "CdbCommandTriggerMethod",
                "Description": "Determines how the host triggers CDB command processing in the module.",
                "Type": ["RO", "Cnd"],
                "Values": {
                    0: (
                        "Single byte WRITE to 9Fh:129 or two-byte WRITE to CMDID register properly terminated by host (STOP)",
                        "SINGLE_BYTE_WRITE",
                    ),
                    1: (
                        "MCI transaction of a WRITE access including the CMDID register properly terminated by host (STOP)",
                        "MCI_TRANSACTION",
                    ),
                },
            },
            (6, 5): {"Name": "Reserved", "Description": "Reserved", "Type": ["RO"]},
            (4, 0): {
                "Name": "CdbExtMaxBusyTime",
                "Description": "Encodes the maximum CDB busy time T_CDBB as max(1,X)*160 ms in range of 160 ms to 4960 ms.",
                "Type": ["RO", "Cnd"],
            },
        },
        166: {
            7: {
                "Name": "CdbMaxBusySpecMethod",
                "Description": "Indicates whether maximum CDB busy time is specified via CdbMaxBusyTime or CdbExtMaxBusyTime.",
                "Type": ["RO", "Cnd"],
                "Values": {
                    0: (
                        "Maximum CDB busy time specified via CdbMaxBusyTime",
                        "CDB_MAX_BUSY_TIME",
                    ),
                    1: (
                        "Maximum CDB busy time specified via CdbExtMaxBusyTime",
                        "CDB_EXT_MAX_BUSY_TIME",
                    ),
                },
            },
            (6, 0): {
                "Name": "CdbMaxBusyTime",
                "Description": "Encodes the maximum CDB busy time T_CDBB as min(80,X)ms in range of 0 ms to 80 ms.",
                "Type": ["RO", "Cnd"],
            },
        },
    },
}
