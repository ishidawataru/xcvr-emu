info = {
    "Name": "SupportedFiberLinkLength",
    "Description": "CMIS v5.2 8.3.7 Supported Fiber Link Length",
    "Page": 1,
    "Table": {
        132: {
            (7, 6): {
                "Name": "LengthMultiplierSMF",
                "Description": "Link length multiplier for SMF fiber",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0b00: ("0.1 (0.1 to 6.3 km)", "MULTIPLIER_0_1"),
                    0b01: ("1 (1 to 63 km)", "MULTIPLIER_1"),
                    0b10: ("10 (10 to 630 km)", "MULTIPLIER_10"),
                    0b11: ("reserved", "RESERVED"),
                },
            },
            (5, 0): {
                "Name": "BaseLengthSMF",
                "Description": "Base link length for SMF fiber in km. Must be multiplied by multiplier defined in bits 7-6 to calculate actual link length.",
                "Type": ["RO", "Rqd"],
            },
        },
        133: {
            (7, 0): {
                "Name": "LengthOM5",
                "Description": "Link length supported for OM5 fiber, units of 2 m (2 to 510 m)",
                "Type": ["RO", "Rqd"],
            }
        },
        134: {
            (7, 0): {
                "Name": "LengthOM4",
                "Description": "Link length supported for OM4 fiber, units of 2 m (2 to 510 m)",
                "Type": ["RO", "Rqd"],
            }
        },
        135: {
            (7, 0): {
                "Name": "LengthOM3",
                "Description": "Link length supported for EBW 50/125 µm fiber (OM3), units of 2m (2 to 510 m)",
                "Type": ["RO", "Rqd"],
            }
        },
        136: {
            (7, 0): {
                "Name": "LengthOM2",
                "Description": "Link length supported for 50/125 µm fiber (OM2), units of 1 m (1 to 255 m)",
                "Type": ["RO", "Rqd"],
            }
        },
        137: {(7, 0): {"Name": "Reserved", "Description": "Reserved", "Type": ["RO"]}},
    },
}
