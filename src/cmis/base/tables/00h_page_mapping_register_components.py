info = {
    "Name": "PageMappingRegisterComponents",
    "Description": "CMIS v5.2 8.22 Page Mapping Register Components",
    "Page": 0,
    "Table": {
        126: {
            (7, 0): {
                "Name": "BankSelect",
                "Description": "Bank Index of Page mapped to Upper Memory (if applicable). Determines which Bank of a Page is accessed when a host ACCESS addresses a Byte in Upper Memory (address 128 through 255). Ignored when the Page indexed by PageSelect is unbanked.",
                "Type": ["RW", "Cnd"],
            }
        },
        127: {
            (7, 0): {
                "Name": "PageSelect",
                "Description": "Page Index of Page mapped to Upper Memory. Determines which Page (or Page in a Bank) is accessed when a host ACCESS addresses a Byte in Upper Memory (address 128 through 255).",
                "Note": "The module may clear the PageSelect to prevent mapping an unsupported page.",
                "Type": ["RWW", "Cnd"],
            }
        },
    },
}
