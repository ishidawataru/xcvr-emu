info = {
    "Name": "SupportedMonitorsAdvertisement",
    "Description": "CMIS v5.2 8.4.7 Supported Monitors Advertisement",
    "Page": 1,
    "Table": {
        159: {
            (7, 6): {
                "Name": "Reserved",
                "Description": "Reserved",
                "Type": ["RO"]
            },
            5: {
                "Name": "CustomMonSupported",
                "Description": "0b: Custom monitor not supported, 1b: Custom monitor supported",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0: ("Custom monitor not supported", "NOT_SUPPORTED"),
                    1: ("Custom monitor supported", "SUPPORTED")
                }
            },
            4: {
                "Name": "Aux3MonSupported",
                "Description": "0b: Aux 3 monitor not supported, 1b: Aux 3 monitor supported",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0: ("Aux 3 monitor not supported", "NOT_SUPPORTED"),
                    1: ("Aux 3 monitor supported", "SUPPORTED")
                }
            },
            3: {
                "Name": "Aux2MonSupported",
                "Description": "0b: Aux 2 monitor not supported, 1b: Aux 2 monitor supported",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0: ("Aux 2 monitor not supported", "NOT_SUPPORTED"),
                    1: ("Aux 2 monitor supported", "SUPPORTED")
                }
            },
            2: {
                "Name": "Aux1MonSupported",
                "Description": "0b: Aux 1 monitor not supported, 1b: Aux 1 monitor supported",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0: ("Aux 1 monitor not supported", "NOT_SUPPORTED"),
                    1: ("Aux 1 monitor supported", "SUPPORTED")
                }
            },
            1: {
                "Name": "VccMonSupported",
                "Description": "0b: Internal 3.3 V monitor not supported, 1b: Internal 3.3 V monitor supported",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0: ("Internal 3.3 V monitor not supported", "NOT_SUPPORTED"),
                    1: ("Internal 3.3 V monitor supported", "SUPPORTED")
                }
            },
            0: {
                "Name": "TempMonSupported",
                "Description": "0b: Temperature monitor not supported, 1b: Temperature monitor supported",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0: ("Temperature monitor not supported", "NOT_SUPPORTED"),
                    1: ("Temperature monitor supported", "SUPPORTED")
                }
            }
        },
        160: {
            (7, 5): {
                "Name": "Reserved",
                "Description": "Reserved",
                "Type": ["RO"]
            },
            (4, 3): {
                "Name": "TxBiasCurrentScalingFactor",
                "Description": "Multiplier for 2uA Bias current increment used in Tx Bias current monitor and threshold registers",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0b00: ("multiply x1", "MULTIPLY_X1"),
                    0b01: ("multiply x2", "MULTIPLY_X2"),
                    0b10: ("multiply x4", "MULTIPLY_X4"),
                    0b11: ("reserved", "RESERVED")
                }
            },
            2: {
                "Name": "RxOpticalPowerMonSupported",
                "Description": "0b: Rx Optical Input Power monitor not supported, 1b: Rx Optical Input Power monitor supported",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0: ("Rx Optical Input Power monitor not supported", "NOT_SUPPORTED"),
                    1: ("Rx Optical Input Power monitor supported", "SUPPORTED")
                }
            },
            1: {
                "Name": "TxOpticalPowerMonSupported",
                "Description": "0b: Tx Output Optical Power monitor not supported, 1b: Tx Output Optical Power monitor supported",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0: ("Tx Output Optical Power monitor not supported", "NOT_SUPPORTED"),
                    1: ("Tx Output Optical Power monitor supported", "SUPPORTED")
                }
            },
            0: {
                "Name": "TxBiasMonSupported",
                "Description": "0b: Tx Bias monitor not supported, 1b: Tx Bias monitor supported",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0: ("Tx Bias monitor not supported", "NOT_SUPPORTED"),
                    1: ("Tx Bias monitor supported", "SUPPORTED")
                }
            }
        }
    }
}

