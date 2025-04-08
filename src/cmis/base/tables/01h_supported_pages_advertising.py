info = {
    "Name": "SupportedPagesAdvertising",
    "Description": "CMIS v5.2 8.3.7 Supported Pages Advertising",
    "Page": 1,
    "Table": {
        142: {
            7: {
                "Name": "NetworkPathPagesSupported",
                "Description": "Page 16h and NP-related parts of Page 17h supported",
                "Type": ["RO", "Rqd"],
            },
            6: {
                "Name": "VDMPagesSupported",
                "Description": "VDM Pages 20h-2Fh (partially) supported (advertisement details in Page 2Fh)",
                "Type": ["RO", "Rqd"],
            },
            5: {
                "Name": "DiagnosticPagesSupported",
                "Description": "Banked Page 13h-14h supported",
                "Type": ["RO", "Rqd"],
            },
            4: {"Name": "Reserved", "Description": "Reserved", "Type": ["RO"]},
            3: {
                "Name": "Page05hSupported",
                "Description": "Form Factor specific Page 05h is supported",
                "Type": ["RO", "Rqd"],
            },
            2: {
                "Name": "Page03hSupported",
                "Description": "User Page 03h supported",
                "Type": ["RO", "Rqd"],
            },
            (1, 0): {
                "Name": "BanksSupported",
                "Description": "Banks supported for Pages 10h-2Fh",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0b00: ("Bank 0 supported (8 lanes)", "BANK_0_SUPPORTED"),
                    0b01: ("Banks 0 and 1 supported (16 lanes)", "BANKS_0_1_SUPPORTED"),
                    0b10: ("Banks 0-3 supported (32 lanes)", "BANKS_0_3_SUPPORTED"),
                    0b11: ("Reserved", "RESERVED"),
                },
            },
        }
    },
}
