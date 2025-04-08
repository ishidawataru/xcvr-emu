info = {
    "Name": "FaultInformation",
    "Description": "CMIS v5.2 8.16 Fault Information",
    "Page": 0,
    "Table": {
        41: {
            (7, 0): {
                "Name": "ModuleFaultCause",
                "Description": "Reason of entering the ModuleFault state",
                "Type": ["RO", "Opt"],
                "Values": {
                    0: ("No Fault detected (or field not supported)", "NO_FAULT"),
                    1: ("TEC runaway", "TEC_RUNAWAY"),
                    2: ("Data memory corrupted", "DATA_MEMORY_CORRUPTED"),
                    3: ("Program memory corrupted", "PROGRAM_MEMORY_CORRUPTED"),
                    (4, 31): ("Reserved (fault codes)", "RESERVED_FAULT_CODES"),
                    (32, 63): ("Custom (fault codes)", "CUSTOM_FAULT_CODES"),
                    (64, 255): ("Reserved (general)", "RESERVED_GENERAL"),
                },
            }
        }
    },
}
