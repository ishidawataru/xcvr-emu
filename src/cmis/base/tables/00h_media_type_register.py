info = {
    "Name": "MediaTypeRegister",
    "Description": "CMIS v5.2 8.18 Media Type Register (Lower Memory)",
    "Page": 0,
    "Table": {
        85: {
            (7, 0): {
                "Name": "MediaType",
                "Description": "The MediaType field defines the interpretation of MediaInterfaceID values in the following Application Descriptors.",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0x00: ("Undefined - None, not applicable", "UNDEFINED"),
                    0x01: ("Optical Interfaces: MMF", "OPTICAL_MMF"),
                    0x02: ("Optical Interfaces: SMF", "OPTICAL_SMF"),
                    0x03: ("Passive Copper Cables", "PASSIVE_COPPER"),
                    0x04: ("Active Cables", "ACTIVE_CABLES"),
                    0x05: ("BASE-T", "BASE_T"),
                    (0x06, 0x3F): ("Reserved", "RESERVED"),
                    (0x40, 0x8F): ("Custom", "CUSTOM"),
                    (0x90, 0xFF): ("Reserved", "RESERVED"),
                },
            }
        }
    },
}
