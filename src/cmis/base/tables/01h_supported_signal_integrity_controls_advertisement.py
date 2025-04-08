info = {
    "Name": "SupportedSignalIntegrityControlsAdvertisement",
    "Description": "CMIS v5.2 8.4.7 Supported Signal Integrity Controls Advertisement",
    "Page": 1,
    "Table": {
        161: {
            7: {"Name": "Reserved", "Description": "Reserved", "Type": ["RO"]},
            (6, 5): {
                "Name": "TxInputEqRecallBuffersSupported",
                "Description": "00b: Tx Input Eq Store/Recall not supported, 01b: Tx Input Eq Store/Recall buffer count=1, 10b: Tx Input Eq Store/Recall buffer count=2, 11b: reserved",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0b00: ("Tx Input Eq Store/Recall not supported", "NOT_SUPPORTED"),
                    0b01: ("Tx Input Eq Store/Recall buffer count=1", "BUFFER_COUNT_1"),
                    0b10: ("Tx Input Eq Store/Recall buffer count=2", "BUFFER_COUNT_2"),
                    0b11: ("Reserved", "RESERVED"),
                },
            },
            4: {
                "Name": "TxInputEqFreezeSupported",
                "Description": "0b: Tx Input Eq Freeze not supported, 1b: Tx Input Eq Freeze supported",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0: ("Tx Input Eq Freeze not supported", "NOT_SUPPORTED"),
                    1: ("Tx Input Eq Freeze supported", "SUPPORTED"),
                },
            },
            3: {
                "Name": "TxInputAdaptiveEqSupported",
                "Description": "0b: Adaptive Tx Input Eq not supported, 1b: Adaptive Tx Input Eq supported",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0: ("Adaptive Tx Input Eq not supported", "NOT_SUPPORTED"),
                    1: ("Adaptive Tx Input Eq supported", "SUPPORTED"),
                },
            },
            2: {
                "Name": "TxInputEqFixedManualControlSupported",
                "Description": "0b: Tx Input Eq Fixed Manual control not supported, 1b: Tx Input Eq Fixed Manual control supported",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0: (
                        "Tx Input Eq Fixed Manual control not supported",
                        "NOT_SUPPORTED",
                    ),
                    1: ("Tx Input Eq Fixed Manual control supported", "SUPPORTED"),
                },
            },
            1: {
                "Name": "TxCDRBypassControlSupported",
                "Description": "0b: If a Tx CDR is supported, it cannot be bypassed, 1b: If a Tx CDR is supported, it can be bypassed",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0: (
                        "If a Tx CDR is supported, it cannot be bypassed",
                        "NOT_BYPASSABLE",
                    ),
                    1: ("If a Tx CDR is supported, it can be bypassed", "BYPASSABLE"),
                },
            },
            0: {
                "Name": "TxCDRSupported",
                "Description": "0b: Tx CDR not supported, 1b: Tx CDR supported",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0: ("Tx CDR not supported", "NOT_SUPPORTED"),
                    1: ("Tx CDR supported", "SUPPORTED"),
                },
            },
        },
        162: {
            7: {"Name": "Reserved", "Description": "Reserved", "Type": ["RO"]},
            6: {
                "Name": "UnidirReconfigSupported",
                "Description": "0b/1b: ApplyImmediateTx/Rx on Page 10h and DPConfigTx/Rx on Page 19h are not supported/supported, for all supported Staged Control Sets",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0: ("ApplyImmediateTx/Rx not supported", "NOT_SUPPORTED"),
                    1: ("ApplyImmediateTx/Rx supported", "SUPPORTED"),
                },
            },
            5: {
                "Name": "StagedSet1Supported",
                "Description": "Staged Control Set 1 supported on Page 10h",
                "Type": ["RO"],
            },
            (4, 3): {
                "Name": "RxOutputEqControlSupported",
                "Description": "00b: Rx Output Eq control not supported, 01b: Rx Output Eq Pre-cursor control supported, 10b: Rx Output Eq Post-cursor control supported, 11b: Rx Output Eq Pre- and Post-cursor control supported",
                "Type": ["RO"],
                "Values": {
                    0b00: ("Rx Output Eq control not supported", "NOT_SUPPORTED"),
                    0b01: (
                        "Rx Output Eq Pre-cursor control supported",
                        "PRE_CURSOR_SUPPORTED",
                    ),
                    0b10: (
                        "Rx Output Eq Post-cursor control supported",
                        "POST_CURSOR_SUPPORTED",
                    ),
                    0b11: (
                        "Rx Output Eq Pre- and Post-cursor control supported",
                        "BOTH_SUPPORTED",
                    ),
                },
            },
            2: {
                "Name": "RxOutputAmplitudeControlSupported",
                "Description": "0b: Rx Output Amplitude control not supported, 1b: Rx Output Amplitude control supported",
                "Type": ["RO"],
                "Values": {
                    0: ("Rx Output Amplitude control not supported", "NOT_SUPPORTED"),
                    1: ("Rx Output Amplitude control supported", "SUPPORTED"),
                },
            },
            1: {
                "Name": "RxCDRBypassControlSupported",
                "Description": "0b: Rx CDR Bypass control not supported (if a CDR is supported, it cannot be bypassed), 1b: Rx CDR Bypass control supported",
                "Type": ["RO"],
                "Values": {
                    0: ("Rx CDR Bypass control not supported", "NOT_SUPPORTED"),
                    1: ("Rx CDR Bypass control supported", "SUPPORTED"),
                },
            },
            0: {
                "Name": "RxCDRSupported",
                "Description": "0b: Rx CDR not supported, 1b: Rx CDR supported",
                "Type": ["RO"],
                "Values": {
                    0: ("Rx CDR not supported", "NOT_SUPPORTED"),
                    1: ("Rx CDR supported", "SUPPORTED"),
                },
            },
        },
    },
}
