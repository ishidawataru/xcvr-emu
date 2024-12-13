info = {
    "Name": "Page00hOverview",
    "Description": "CMIS v5.2 8.3 Page 00h (Administrative Information)",
    "Page": 0,
    "Table": {
        128: {
            "Name": "SFF8024IdentifierCopy",
            "Description": "This Byte shall contain the same value as the SFF8024 Identifier Byte 00h:0. See Byte 00h:0 for a description of its meaning.",
            "Note": "This duplication requirement is maintained for historical reasons and for similarity with predecessor SFF MSA specifications.",
            "Type": ["RO", "Rqd"],
        },
        (129, 144): {
            "Name": "VendorName",
            "Description": "Vendor name (ASCII). A 16 character read-only field, left aligned and padded on the right with ASCII spaces (20h). Represents the full name of the company, or an abbreviation. Must correlate to VendorOUI.",
            "Type": ["RO", "Rqd"],
            "ValueType": str,
        },
        (145, 147): {
            "Name": "VendorOUI",
            "Description": "Vendor IEEE company ID. A 3-byte field containing the IEEE Company Identifier for the vendor. Value of all zero indicates unspecified OUI.",
            "Type": ["RO", "Rqd"],
        },
        (148, 163): {
            "Name": "VendorPN",
            "Description": "Part number provided by vendor (ASCII). A 16-byte field, left aligned and padded on the right with ASCII spaces (20h). Defines the vendor part number or product name. All zeroes indicate unspecified part number.",
            "Type": ["RO", "Rqd"],
            "ValueType": str,
        },
        (164, 165): {
            "Name": "VendorRev",
            "Description": "Revision level for part number provided by vendor (ASCII). A 2-byte field, left aligned and padded with ASCII spaces (20h). All zeroes indicate unspecified revision.",
            "Type": ["RO", "Rqd"],
            "ValueType": str,
        },
        (166, 181): {
            "Name": "VendorSN",
            "Description": "Vendor Serial Number (ASCII). A 16-byte field, left aligned and padded with ASCII spaces (20h). Represents the vendor's serial number for the product. All zeroes indicate unspecified serial number.",
            "Type": ["RO", "Rqd"],
            "ValueType": str,
        },
        "DateCode": {
            (0, 1): {
                "Name": "Year",
                "Description": "ASCII two lower digits of year (00-99)",
                "Type": ["RO", "Rqd"],
            },
            2: {
                "Name": "Month",
                "Description": "ASCII digits of month (01=Jan through 12=Dec)",
                "Type": ["RO", "Rqd"],
            },
            3: {
                "Name": "DayOfMonth",
                "Description": "ASCII day of month (01-31)",
                "Type": ["RO", "Rqd"],
            },
            (4, 7): {
                "Name": "LotCode",
                "Description": "ASCII custom lot code, may be blank",
                "Type": ["RO", "Opt"],
            },
        },
        (182, 189): {
            "Template": "DateCode",
            "Description": "Manufacturing Date Code (ASCII). An 8-byte field containing the vendor's date code in ASCII. Mandatory and formatted as described in Table 8-26.",
            "Type": ["RO", "Rqd"],
        },
        (190, 199): {
            "Name": "CLEICode",
            "Description": "Common Language Equipment Identification Code (ASCII). A 10-byte field representing the Common Language Equipment Identification code.",
            "Type": ["RO", "Rqd"],
        },
        200: {
            (7, 5): {
                "Name": "ModulePowerClass",
                "Description": "Power class of the module",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0b000: ("Power class 1", "CLASS_1"),
                    0b001: ("Power class 2", "CLASS_2"),
                    0b010: ("Power class 3", "CLASS_3"),
                    0b011: ("Power class 4", "CLASS_4"),
                    0b100: ("Power class 5", "CLASS_5"),
                    0b101: ("Power class 6", "CLASS_6"),
                    0b110: ("Power class 7", "CLASS_7"),
                    0b111: ("Power class 8", "CLASS_8"),
                },
            },
            (4, 0): {"Name": "Reserved", "Description": "Reserved"},
        },
        201: {
            "Name": "MaxPower",
            "Description": "Maximum power consumption in multiples of 0.25 W, rounded up to the next whole multiple of 0.25 W",
            "Type": ["RO", "Rqd"],
        },
        202: {
            (7, 6): {
                "Name": "LengthMultiplier",
                "Description": "Multiplier for value in bits 5-0",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0b00: ("multiplier 0.1", "MULTIPLIER_0_1"),
                    0b01: ("multiplier 1", "MULTIPLIER_1"),
                    0b10: ("multiplier 10", "MULTIPLIER_10"),
                    0b11: ("multiplier 100", "MULTIPLIER_100"),
                },
            },
            (5, 0): {
                "Name": "BaseLength",
                "Description": "Link length base value in meters. A value of 0 indicates an undefined Link Length, e.g. when the physical media can be disconnected from the module.",
                "Type": ["RO", "Rqd"],
            },
        },
        203: {
            "Name": "ConnectorType",
            "Description": "Type of connector present in the module. See [5] for Connector Type codes.",
            "Type": ["RO", "Rqd"],
        },
        212: {
            "Name": "MediaInterfaceTechnology",
            "Description": "Media Interface Technology as per Table 8-36",
            "Type": ["RO", "Rqd"],
            "Values": {
                0x00: ("850 nm VCSEL", "VCSEL_850NM"),
                0x01: ("1310 nm VCSEL", "VCSEL_1310NM"),
                0x02: ("1550 nm VCSEL", "VCSEL_1550NM"),
                0x03: ("1310 nm FP", "FP_1310NM"),
                0x04: ("1310 nm DFB", "DFB_1310NM"),
                0x05: ("1550 nm DFB", "DFB_1550NM"),
                0x06: ("1310 nm EML", "EML_1310NM"),
                0x07: ("1550 nm EML", "EML_1550NM"),
                0x08: ("Others", "OTHERS"),
                0x09: ("1490 nm DFB", "DFB_1490NM"),
                0x0A: ("Copper cable unequalized", "COPPER_UNEQUALIZED"),
                0x0B: (
                    "Copper cable passive equalized",
                    "COPPER_PASSIVE_EQUALIZED",
                ),
                0x0C: (
                    "Copper cable, near and far end limiting active equalizers",
                    "COPPER_NEAR_FAR_ACTIVE_EQ",
                ),
                0x0D: (
                    "Copper cable, far end limiting active equalizers",
                    "COPPER_FAR_ACTIVE_EQ",
                ),
                0x0E: (
                    "Copper cable, near end limiting active equalizers",
                    "COPPER_NEAR_ACTIVE_EQ",
                ),
                0x0F: (
                    "Copper cable, linear active equalizers",
                    "COPPER_LINEAR_ACTIVE_EQ",
                ),
                0x10: ("C-band tunable laser", "C_BAND_TUNABLE"),
                0x11: ("L-band tunable laser", "L_BAND_TUNABLE"),
                (0x12, 0xFF): ("Reserved", "RESERVED"),
            },
        },
        (213, 220): {"Name": "Reserved", "Description": "Reserved", "Type": ["RO"]},
        221: {"Name": "Custom", "Description": "Custom", "Type": ["RO"]},
        222: {
            "Name": "PageChecksum",
            "Description": "Page Checksum over bytes 128-221",
            "Type": ["RO", "Rqd"],
        },
        (223, 255): {
            "Name": "Custom",
            "Description": "Custom Information (non-volatile)",
            "Type": ["RO"],
        },
    },
}
