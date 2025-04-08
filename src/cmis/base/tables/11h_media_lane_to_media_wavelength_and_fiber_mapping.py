info = {
    "Name": "MediaLaneToMediaWavelengthAndFiberMapping",
    "Description": (
        "CMIS v5.2 Table 8-90 Media Lane to Media Wavelength and Fiber Mapping (Page 11h)"
    ),
    "Page": 0x11,
    "Table": {
        "MediaLaneMapping": {
            (7, 4): {
                "Name": "WavelengthMapping",
                "Description": "Mapping of media lane <i> to media wavelength.",
                "Type": ["RO", "Cnd"],
                "Values": {
                    0b0000: ("Mapping unknown or undefined", "UNDEFINED"),
                    0b0001: ("Maps to media wavelength 1", "WAVELENGTH_1"),
                    0b0010: ("Maps to media wavelength 2", "WAVELENGTH_2"),
                    0b0011: ("Maps to media wavelength 3", "WAVELENGTH_3"),
                    0b0100: ("Maps to media wavelength 4", "WAVELENGTH_4"),
                    0b0101: ("Maps to media wavelength 5", "WAVELENGTH_5"),
                    0b0110: ("Maps to media wavelength 6", "WAVELENGTH_6"),
                    0b0111: ("Maps to media wavelength 7", "WAVELENGTH_7"),
                    0b1000: ("Maps to media wavelength 8", "WAVELENGTH_8"),
                    (0b1001, 0b1111): ("Reserved", "RESERVED"),
                },
            },
            (3, 0): {
                "Name": "FiberMapping",
                "Description": "Mapping of media lane <i> to media fiber.",
                "Type": ["RO", "Cnd"],
                "Values": {
                    0b0000: ("Mapping unknown or undefined", "UNDEFINED"),
                    0b0001: ("Maps to media fiber 1 or TR1", "FIBER1_OR_TR1"),
                    0b0010: ("Maps to media fiber 2 or RT1", "FIBER2_OR_RT1"),
                    0b0011: ("Maps to media fiber 3 or TR2", "FIBER3_OR_TR2"),
                    0b0100: ("Maps to media fiber 4 or RT2", "FIBER4_OR_RT2"),
                    0b0101: ("Maps to media fiber 5 or TR3", "FIBER5_OR_TR3"),
                    0b0110: ("Maps to media fiber 6 or RT3", "FIBER6_OR_RT3"),
                    0b0111: ("Maps to media fiber 7 or TR4", "FIBER7_OR_TR4"),
                    0b1000: ("Maps to media fiber 8 or RT4", "FIBER8_OR_RT4"),
                },
            },
        },
        "MediaLaneMappingTx": {
            "Template": "MediaLaneMapping",
        },
        "MediaLaneMappingRx": {
            "Template": "MediaLaneMapping",
        },
        range(240, 248): {
            "Template": "MediaLaneMappingTx",
        },
        range(248, 256): {
            "Template": "MediaLaneMappingRx",
        },
    },
}
