info = {
    "Name": "ManagementCharacteristics",
    "Description": "CMIS v5.2 8.2.1 Management Characteristics page 127",
    "Page": 0,
    "Table": {
        0: {
            (7, 0): {
                "Name": "SFF8024Identifier",
                "Description": "SFF8024Identifier is an SFF-8024 module type Identifier from the Identifier Values table in [5] which allows to infer both physical form factor and management protocol of the module.",
                "Note": "The CMIS interpretation of all other registers or fields is valid only when the fundamental SFF8024Identifier indicates that the module uses the CMIS management protocol.",
                "Type": ["RO", "Rqd"],
                # TODO "get Values from SFF-8024 module type Identifier table"
            }
        },
        "CmisRevision": {
            (7, 4): {
                "Name": "Major",
                "Description": "Major revision number",
            },
            (3, 0): {
                "Name": "Minor",
                "Description": "Minor revision number",
            },
        },
        1: {
            "Template": "CmisRevision",
            "Description": "CMIS revision number (decimal). The upper nibble (bits 7-4) is the integer part (major number). The lower nibble (bits 3-0) is the decimal part (minor number).",
            "Example": "01h indicates version 0.1, 21h indicates version 2.1.",
            "Note": "See Appendix G.3 for interoperability implications of the major revision number (integer part).",
            "Type": ["RO", "Rqd"],
        },
        2: {
            7: {
                "Name": "MemoryModel",
                "Description": "Indicator of the memory model of the module. 0b: Paged memory (Pages 00h-02h, 10h-11h supported), 1b: Flat memory (Page 00h supported only).",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0: ("Paged memory", "PAGED"),
                    1: ("Flat memory", "FLAT"),
                },
            },
            6: {
                "Name": "SteppedConfigOnly",
                "Description": "Module supports intervention-free reconfiguration or step-by-step reconfiguration.",
                "Details": "0b: Module supports intervention-free reconfiguration. 1b: Module supports only step-by-step reconfiguration.",
                "Note": "Support for intervention-free reconfiguration is required for any Application that supports or requires time critical speed negotiation with active modules that is not achievable with stepwise configuration, such as InfiniBand or Fibre Channel.",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0: ("Intervention-free reconfiguration", "INTERVENTION_FREE"),
                    1: ("Step-by-step reconfiguration", "STEP_BY_STEP"),
                },
            },
            (5, 4): {"Name": "Reserved", "Description": "Reserved"},
            (3, 2): {
                "Name": "MciMaxSpeed",
                "Description": "Indicates maximum supported clock speed of Management Communication Interface (MCI).",
                "Type": ["RO", "Rqd"],
                "Values": {
                    0b00: ("Module supports up to 400 kHz", "UP_TO_400_KHZ"),
                    0b01: ("Module supports up to 1 MHz", "UP_TO_1_MHZ"),
                    0b10: ("Reserved", "RESERVED"),
                    0b11: ("Reserved", "RESERVED"),
                },
            },
            (1, 0): {"Name": "Reserved", "Description": "Reserved"},
        },
    },
}
