def version_lt(m, major: int, minor: int):
    return m.CmisRevision.value < (major << 4 | minor)


def version_lte(m, major: int, minor: int):
    return m.CmisRevision.value <= (major << 4 | minor)


def version_gt(m, major: int, minor: int):
    return m.CmisRevision.value > (major << 4 | minor)


def version_gte(m, major: int, minor: int):
    return m.CmisRevision.value >= (major << 4 | minor)


def intervention_free(m):
    return m.SteppedConfigOnly.value(as_int=True) == 0


def step_by_step(m):
    return m.SteppedConfigOnly.value(as_int=True) == 1


info = {
    "Name": "ManagementCharacteristics",
    "Description": "CMIS v5.2 8.2.1 Management Characteristics page 127",
    "Page": 0,
    "Table": {
        0: {
            "Name": "SFF8024Identifier",
            "Description": "SFF8024Identifier is an SFF-8024 module type Identifier from the Identifier Values table in [5] which allows to infer both physical form factor and management protocol of the module.",
            "Note": "The CMIS interpretation of all other registers or fields is valid only when the fundamental SFF8024Identifier indicates that the module uses the CMIS management protocol.",
            "Type": ["RO", "Rqd"],
            "Values": {
                0x0: ("Unknown", "UNKNOWN"),
                0x1: ("GBIC", "GBIC"),
                0x2: ("Module soldered to motherboard", "MODULE_SOLDERED"),
                0x3: ("SFP/SFP+/SFP28 with SFF-8472 management interface", "SFP"),
                0x4: ("300 pin XBI", "XBI"),
                0x5: ("XENPAK", "XENPAK"),
                0x6: ("XFP", "XFP"),
                0x7: ("XFF", "XFF"),
                0x8: ("XFP-E", "XFP_E"),
                0x9: ("XPAK", "XPAK"),
                0xA: ("X2", "X2"),
                0xB: ("DWDM-SFP", "DWDM_SFP"),
                0xC: ("QSFP", "QSFP"),
                0xD: (
                    "QSFP+ with SFF-8636 or SFF-8436 management interface",
                    "QSFP_PLUS",
                ),
                0xE: ("CXP", "CXP"),
                0xF: ("Shielded Mini Multilane HD 4X", "SHIELDED_MINI_MULTILANE_HD_4X"),
                0x10: (
                    "Shielded Mini Multilane HD 8X",
                    "SHIELDED_MINI_MULTILANE_HD_8X",
                ),
                0x11: ("QSFP28", "QSFP28"),
                0x12: ("CXP2", "CXP2"),
                0x13: ("CDFP (Style1/Style2) INF-TA-1003", "CDFP_STYLE1_STYLE2"),
                0x14: (
                    "Shielded Mini Multilane HD 4X Fanout Cable",
                    "SHIELDED_MINI_MULTILANE_HD_4X_FANOUT",
                ),
                0x15: (
                    "Shielded Mini Multilane HD 8X Fanout Cable",
                    "SHIELDED_MINI_MULTILANE_HD_8X_FANOUT",
                ),
                0x16: ("CDFP (Style3) INF-TA-1003", "CDFP_STYLE3"),
                0x17: ("MicroQSFP", "MICRO_QSFP"),
                0x18: ("QSFP-DD", "QSFP_DD"),
                0x19: ("OSFP", "OSFP"),
                0x1A: ("SFP-DD", "SFP_DD"),
                0x1B: ("DSFP Dual Small Form Factor", "DSFP"),
                0x1C: ("x4 MiniLink/OcuLink", "X4_MINILINK"),
                0x1D: ("x8 MiniLink/OcuLink", "X8_MINILINK"),
                0x1E: ("QSFP+ with CMIS", "QSFP_PLUS_CMIS"),
                0x1F: ("SFP-DD with CMIS", "SFP_DD_CMIS"),
                0x20: ("SFP+ with CMIS", "SFP_PLUS_CMIS"),
                0x21: ("OSFP-XD with CMIS", "OSFP_XD"),
                0x22: ("OIF-ELSFP with CMIS", "OIF_ELSFP"),
                0x23: ("CDFP(x4 PCIe) SFF-TA-1032 with CMIS", "CDFP_X4"),
                0x24: ("CDFP(x8 PCIe) SFF-TA-1032 with CMIS", "CDFP_X8"),
                0x25: ("CDFP(x16 PCIe) SFF-TA-1032 with CMIS", "CDFP_X16"),
                (0x26, 0x7F): ("Reserved", "RESERVED"),
                (0x80, 0xFF): ("Vendor specific", "VENDOR_SPECIFIC"),
            },
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
            (1, 0): [
                {
                    "When": ("version < v5.3", lambda m: version_lt(m, 5, 3)),
                    "Name": "Reserved",
                    "Description": "Reserved",
                },
                {
                    "When": ("version >= v5.3", lambda m: version_gte(m, 5, 3)),
                    "Name": "AutoCommissioning",
                    "Description": """
                    This field allows modules to support just one of the two intervention-free reconfiguration procedures, either the regular (automatic DPSM state changing) one or the hot one (staying in DPSM state):
                    SteppedConfigOnly = 0:
                        xx: both regular and hot supported (legacy default)
                    SteppedConfigOnly = 1:
                        00: none, neither regular nor hot supported
                        01: only regular supported (affects ApplyDPInit)
                        10: only hot supported (affects ApplyImmediate)
                        11: reserved
                    Effect on ApplyImmediate:
                        When hot intervention-free reconfiguration is unsupported,
                        the module ignores any WRITE to ApplyImmediate registers
                    Effect on ApplyDPInit:
                        When regular intervention-free reconfiguration is not
                        supported, the module accepts ApplyDPInit in all states as a
                        Provision command (see Table 6-4) , but the DPSM excludes
                        the DPReinitT term in the DPDeReinitS transition signal (see
                        Case 2 in section 6.3.3.1)
                    """,
                    "Type": ["RO", "Rqd"],
                    "Values": [
                        {
                            "When": ("intervention-free", intervention_free),
                            (0x00, 0xFF): ("Reserved", "RESERVED"),
                        },
                        {
                            "When": ("step-by-step", step_by_step),
                            0: ("None", "NONE"),
                            1: ("Only regular supported", "ONLY_REGULAR_SUPPORTED"),
                            2: ("Only hot supported", "ONLY_HOT_SUPPORTED"),
                            (3, 0xFF): ("Reserved", "RESERVED"),
                        },
                    ],
                },
            ],
        },
    },
}
