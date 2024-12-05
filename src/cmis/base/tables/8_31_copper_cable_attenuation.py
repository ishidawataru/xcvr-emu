info = {
    "Name": "CopperCableAttenuationAndMediaLaneInformation",
    "Description": "CMIS v5.2 8.3.7 Copper Cable Attenuation and Media Lane Information",
    "Page": 0,
    "Table": {
        204: {
            "Name": "AttenuationAt5GHz",
            "Description": "U8 Passive copper cable attenuation at 5 GHz in 1 dB increments",
            "Type": ["RO", "Cnd"],
        },
        205: {
            "Name": "AttenuationAt7GHz",
            "Description": "U8 Passive copper cable attenuation at 7 GHz in 1 dB increments",
            "Type": ["RO", "Cnd"],
        },
        206: {
            "Name": "AttenuationAt12p9GHz",
            "Description": "U8 Passive copper cable attenuation at 12.9 GHz in 1 dB increments",
            "Type": ["RO", "Cnd"],
        },
        207: {
            "Name": "AttenuationAt25p8GHz",
            "Description": "U8 Passive copper cable attenuation at 25.8 GHz in 1 dB increments",
            "Type": ["RO", "Cnd"],
        },
        (208, 209): {"Name": "Reserved", "Description": "Reserved", "Type": ["RO"]},
        210: {
            range(0, 8): {
                "Name": "MediaLaneUnsupportedLane",
                "Description": "Indicates if Media Lane is unsupported.",
                "Type": ["RO", "Cnd"],
                "Values": {
                    0: ("Media Lane supported", "SUPPORTED"),
                    1: ("Media Lane not supported", "NOT_SUPPORTED"),
                },
            },
        },
    },
}
