info = {
    "Name": "SupportedFlagsAdvertisement",
    "Description": "CMIS v5.2 8.4.7 Supported Flags Advertisement",
    "Page": 1,
    "Table": {
        157: {
            (7, 4): {
                "Name": "Reserved",
                "Description": "Reserved",
                "Type": ["RO"]
            },
            3: {
                "Name": "AdaptiveInputEqFailFlagTxSupported",
                "Description": "0b: Tx Adaptive Input Eq Fail Flags not supported, 1b: supported",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0: ("Tx Adaptive Input Eq Fail Flags not supported", "NOT_SUPPORTED"),
                    1: ("Tx Adaptive Input Eq Fail Flags supported", "SUPPORTED")
                }
            },
            2: {
                "Name": "CDRLOLFlagTxSupported",
                "Description": "0b: Tx CDR Loss of Lock Flags not supported, 1b: supported",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0: ("Tx CDR Loss of Lock Flags not supported", "NOT_SUPPORTED"),
                    1: ("Tx CDR Loss of Lock Flags supported", "SUPPORTED")
                }
            },
            1: {
                "Name": "LOSFlagTxSupported",
                "Description": "0b: Tx Loss of Signal Flags not supported, 1b: supported",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0: ("Tx Loss of Signal Flags not supported", "NOT_SUPPORTED"),
                    1: ("Tx Loss of Signal Flags supported", "SUPPORTED")
                }
            },
            0: {
                "Name": "FailureFlagTxSupported",
                "Description": "0b: Tx Fault Flags not supported, 1b: supported",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0: ("Tx Fault Flags not supported", "NOT_SUPPORTED"),
                    1: ("Tx Fault Flags supported", "SUPPORTED")
                }
            }
        },
        158: {
            (7, 3): {
                "Name": "Reserved",
                "Description": "Reserved",
                "Type": ["RO"]
            },
            2: {
                "Name": "CDRLOLFlagRxSupported",
                "Description": "0b: Rx CDR Loss of Lock Flags not supported, 1b: Rx CDR Loss of Lock Flags supported",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0: ("Rx CDR Loss of Lock Flags not supported", "NOT_SUPPORTED"),
                    1: ("Rx CDR Loss of Lock Flags supported", "SUPPORTED")
                }
            },
            1: {
                "Name": "LOSFlagRxSupported",
                "Description": "0b: Rx Loss of Signal Flags not supported, 1b: Rx Loss of Signal Flags supported",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0: ("Rx Loss of Signal Flags not supported", "NOT_SUPPORTED"),
                    1: ("Rx Loss of Signal Flags supported", "SUPPORTED")
                }
            },
            0: {
                "Name": "Reserved",
                "Description": "Reserved",
                "Type": ["RO"]
            }
        }
    }
}

