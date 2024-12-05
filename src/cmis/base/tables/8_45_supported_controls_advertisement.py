info = {
    "Name": "SupportedControlsAdvertisement",
    "Description": "CMIS v5.2 8.4.7 Supported Controls Advertisement",
    "Page": 1,
    "Table": {
        155: {
            7: {
                "Name": "WavelengthIsControllable",
                "Description": "0b: No wavelength control, 1b: Active wavelength control supported",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0: ("No wavelength control", "NO_CONTROL"),
                    1: ("Active wavelength control supported", "CONTROL_SUPPORTED")
                }
            },
            6: {
                "Name": "TransmitterIsTunable",
                "Description": "0b: Transmitter not tunable, 1b: Transmitter is tunable (Pages 04h & 12h supported)",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0: ("Transmitter not tunable", "NOT_TUNABLE"),
                    1: ("Transmitter is tunable", "TUNABLE")
                }
            },
            (5, 4): {
                "Name": "SquelchMethodTx",
                "Description": "Defines the Tx output squelching function",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0b00: ("Tx output squelching function is not supported", "NOT_SUPPORTED"),
                    0b01: ("Tx output squelching function reduces OMA", "REDUCES_OMA"),
                    0b10: ("Tx output squelching function reduces Pav", "REDUCES_PAV"),
                    0b11: ("Host controls the method for Tx output squelching", "HOST_CONTROL")
                }
            },
            3: {
                "Name": "ForcedSquelchTxSupported",
                "Description": "0b/1b: Host cannot/can force squelching of Tx outputs using OutputSquelchForceTx*",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0: ("Host cannot force squelching of Tx outputs", "NOT_SUPPORTED"),
                    1: ("Host can force squelching of Tx outputs", "SUPPORTED")
                }
            },
            2: {
                "Name": "AutoSquelchDisableTxSupported",
                "Description": "0b/1b: Host cannot/can disable automatic squelching of Tx outputs using AutoSquelchDisableTx*",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0: ("Host cannot disable automatic squelching of Tx outputs", "NOT_SUPPORTED"),
                    1: ("Host can disable automatic squelching of Tx outputs", "SUPPORTED")
                }
            },
            1: {
                "Name": "OutputDisableTxSupported",
                "Description": "0b/1b: Host cannot/can disable Tx outputs using the OutputDisableTx register",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0: ("Host cannot disable Tx outputs", "NOT_SUPPORTED"),
                    1: ("Host can disable Tx outputs", "SUPPORTED")
                }
            },
            0: {
                "Name": "InputPolarityFlipTxSupported",
                "Description": "0b/1b: InputPolarityFlipTx control not supported/supported",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0: ("InputPolarityFlipTx control not supported", "NOT_SUPPORTED"),
                    1: ("InputPolarityFlipTx control supported", "SUPPORTED")
                }
            }
        },
        156: {
            7: {
                "Name": "BankBroadcastSupported",
                "Description": "0b/1b: The BankBroadcastEnable control is not supported/supported",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0: ("BankBroadcastEnable control not supported", "NOT_SUPPORTED"),
                    1: ("BankBroadcastEnable control supported", "SUPPORTED")
                }
            },
            (6, 3): {
                "Name": "Reserved",
                "Description": "Reserved",
                "Type": ["RO"]
            },
            2: {
                "Name": "AutoSquelchDisableRxSupported",
                "Description": "0b/1b: Host cannot/can disable automatic squelching of Rx outputs using AutoSquelchDisableRx register",
                "Type": ["RO", "Cnd"],
                "Values": {
                    0: ("Host cannot disable automatic squelching of Rx outputs", "NOT_SUPPORTED"),
                    1: ("Host can disable automatic squelching of Rx outputs", "SUPPORTED")
                }
            },
            1: {
                "Name": "OutputDisableRxSupported",
                "Description": "0b/1b: Host cannot/can disable Rx outputs using the OutputDisableRx register",
                "Type": ["RO", "Cnd"],
                "Values": {
                    0: ("Host cannot disable Rx outputs", "NOT_SUPPORTED"),
                    1: ("Host can disable Rx outputs", "SUPPORTED")
                }
            },
            0: {
                "Name": "OutputPolarityFlipRxSupported",
                "Description": "0b/1b: PolarityFlipRx not supported/supported",
                "Type": ["RO", "Cnd"],
                "Values": {
                    0: ("PolarityFlipRx not supported", "NOT_SUPPORTED"),
                    1: ("PolarityFlipRx supported", "SUPPORTED")
                }
            }
        }
    }
}
