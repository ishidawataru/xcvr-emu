info = {
    "Name": "ModuleCharacteristicsAdvertising",
    "Description": "CMIS v5.2 8.3.7 Module Characteristics Advertising",
    "Page": 1,
    "Table": {
        145: {
            7: {
                "Name": "CoolingImplemented",
                "Description": "0b: Uncooled transmitter device, 1b: Cooled transmitter",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0: ("Uncooled transmitter device", "UNCOOLED"),
                    1: ("Cooled transmitter", "COOLED"),
                },
            },
            (6, 5): {
                "Name": "TxInputClockingCapabilities",
                "Description": "Defines which Tx input lanes must be frequency synchronous",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0b00: ("Tx input lanes 1-8", "LANES_1_8"),
                    0b01: ("Tx input lanes 1-4 and 5-8", "LANES_1_4_AND_5_8"),
                    0b10: ("Tx input lanes 1-2, 3-4, 5-6, 7-8", "PAIRS"),
                    0b11: ("Lanes may be asynchronous in frequency", "ASYNCHRONOUS"),
                },
            },
            4: {
                "Name": "ePPSSupported",
                "Description": "Support of the Enhanced Pulse Per Second timing signal",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0: ("ePPS signal processing not supported", "NOT_SUPPORTED"),
                    1: ("ePPS signal processing supported", "SUPPORTED"),
                },
            },
            3: {
                "Name": "TimingPage15hSupported",
                "Description": "0b: Timing characteristics (Page 15h) not supported, 1b: Timing characteristics (Page 15h) supported",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0: (
                        "Timing characteristics (Page 15h) not supported",
                        "NOT_SUPPORTED",
                    ),
                    1: ("Timing characteristics (Page 15h) supported", "SUPPORTED"),
                },
            },
            2: {
                "Name": "Aux3MonObservable",
                "Description": "0b: Aux 3 monitor monitors Laser Temperature, 1b: Aux 3 monitor monitors Vcc2",
                "Type": ["RO", "Adv"],
                "Values": {
                    0: ("Aux 3 monitor monitors Laser Temperature", "LASER_TEMP"),
                    1: ("Aux 3 monitor monitors Vcc2", "VCC2"),
                },
            },
            1: {
                "Name": "Aux2MonObservable",
                "Description": "0b: Aux 2 monitor monitors Laser Temperature, 1b: Aux 2 monitor monitors TEC current",
                "Type": ["RO", "Adv"],
                "Values": {
                    0: ("Aux 2 monitor monitors Laser Temperature", "LASER_TEMP"),
                    1: ("Aux 2 monitor monitors TEC current", "TEC_CURRENT"),
                },
            },
            0: {
                "Name": "Aux1MonObservable",
                "Description": "0b: Aux 1 monitor is custom, 1b: Aux 1 monitor monitors TEC current",
                "Type": ["RO", "Adv"],
                "Values": {
                    0: ("Aux 1 monitor is custom", "CUSTOM"),
                    1: ("Aux 1 monitor monitors TEC current", "TEC_CURRENT"),
                },
            },
        },
        146: {
            (7, 0): {
                "Name": "ModuleTempMax",
                "Description": "S8 Maximum allowed module case temperature in 1 deg C increments",
                "Type": ["RO", "Cnd"],
            }
        },
        147: {
            (7, 0): {
                "Name": "ModuleTempMin",
                "Description": "S8 Minimum allowed module case temperature in 1 deg C increments",
                "Type": ["RO", "Cnd"],
            }
        },
        (148, 149): {
            (7, 0): {
                "Name": "PropagationDelay",
                "Description": "U16 Propagation delay of a non-separable AOC in multiples of 10 ns rounded to the nearest 10 ns",
                "Type": ["RO", "Cnd"],
            }
        },
        150: {
            (7, 0): {
                "Name": "OperatingVoltageMin",
                "Description": "U8 Minimum supported module operating voltage, in 20 mV increments (0.5-1 V), or zero for 'not specified'",
                "Type": ["RO", "Cnd"],
            }
        },
        151: {
            7: {
                "Name": "OpticalDetectorType",
                "Description": "0b: PIN detector, 1b: APD detector",
                "Type": ["RO", "Rqd"],
                "Values": {0: ("PIN detector", "PIN"), 1: ("APD detector", "APD")},
            },
            (6, 5): {
                "Name": "RxOutputEqType",
                "Description": "Defines Rx Output Equalization Type",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0b00: (
                        "Peak-to-peak (p-p) amplitude stays constant, or no information",
                        "PEAK_TO_PEAK",
                    ),
                    0b01: ("Steady-state amplitude stays constant", "STEADY_STATE"),
                    0b10: (
                        "Average of p-p and steady-state amplitude stays constant",
                        "AVERAGE_PP_STEADY",
                    ),
                    0b11: ("Reserved", "RESERVED"),
                },
            },
            4: {
                "Name": "RxPowerMeasurementType",
                "Description": "0b: OMA, 1b: average power",
                "Type": ["RO", "Adv"],
                "Values": {0: ("OMA", "OMA"), 1: ("Average power", "AVG_POWER")},
            },
            3: {
                "Name": "RxLOSType",
                "Description": "0b: Rx LOS responds to OMA, 1b: Rx LOS responds to Pavg",
                "Type": ["RO", "Adv"],
                "Values": {
                    0: ("Rx LOS responds to OMA", "OMA"),
                    1: ("Rx LOS responds to Pavg", "PAVG"),
                },
            },
            2: {
                "Name": "RxLOSIsFast",
                "Description": "0b: Module raises Rx LOS within regular timing limits, 1b: Module raises Rx LOS within 'fast mode' timing limits",
                "Type": ["RO", "Adv"],
                "Values": {
                    0: ("Regular timing limits", "REGULAR"),
                    1: ("Fast mode timing limits", "FAST"),
                },
            },
        },
        152: {
            (7, 0): {
                "Name": "CDRPowerSavedPerLane",
                "Description": "U8 Minimum power consumption saved per CDR per lane when placed in CDR bypass, in multiples of 0.01 W rounded up to the next whole multiple of 0.01 W",
                "Type": ["RO", "Cnd"],
            }
        },
        153: {
            7: {
                "Name": "RxOutputLevel3Supported",
                "Description": "0b/1b: Amplitude Code 3 not supported/supported",
                "Type": ["RO", "Cnd"],
                "Values": {
                    0: ("Amplitude Code 3 not supported", "NOT_SUPPORTED"),
                    1: ("Amplitude Code 3 supported", "SUPPORTED"),
                },
            },
            6: {
                "Name": "RxOutputLevel2Supported",
                "Description": "0b/1b: Amplitude Code 2 not supported/supported",
                "Type": ["RO", "Cnd"],
                "Values": {
                    0: ("Amplitude Code 2 not supported", "NOT_SUPPORTED"),
                    1: ("Amplitude Code 2 supported", "SUPPORTED"),
                },
            },
            5: {
                "Name": "RxOutputLevel1Supported",
                "Description": "0b/1b: Amplitude Code 1 not supported/supported",
                "Type": ["RO", "Cnd"],
                "Values": {
                    0: ("Amplitude Code 1 not supported", "NOT_SUPPORTED"),
                    1: ("Amplitude Code 1 supported", "SUPPORTED"),
                },
            },
            4: {
                "Name": "RxOutputLevel0Supported",
                "Description": "0b/1b: Amplitude Code 0 not supported/supported",
                "Type": ["RO", "Cnd"],
                "Values": {
                    0: ("Amplitude Code 0 not supported", "NOT_SUPPORTED"),
                    1: ("Amplitude Code 0 supported", "SUPPORTED"),
                },
            },
            (3, 0): {
                "Name": "TxInputEqMax",
                "Description": "Maximum supported value of the Tx Input Equalization control for manual/fixed programming",
                "Type": ["RO", "Cnd"],
            },
        },
        154: {
            (7, 4): {
                "Name": "RxOutputEqPostCursorMax",
                "Description": "Maximum supported value of the Rx Output Eq Post-cursor control",
                "Type": ["RO", "Cnd"],
            },
            (3, 0): {
                "Name": "RxOutputEqPreCursorMax",
                "Description": "Maximum supported value of the Rx Output Eq Pre-cursor control",
                "Type": ["RO", "Cnd"],
            },
        },
    },
}
