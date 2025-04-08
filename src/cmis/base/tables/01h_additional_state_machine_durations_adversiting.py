info = {
    "Name": "AdditionalStateMachineDurationsAdvertising",
    "Description": "CMIS v5.2 8.4.7 Additional State Machine Durations Advertising",
    "Page": 1,
    "Table": {
        167: {
            (7, 4): {
                "Name": "MaxDurationModulePwrDn",
                "Description": "Encoded maximum duration of the ModulePwrDn state (see Table 8-43)",
                "Type": ["RO", "Rqd"],
                "Template": "Duration",
            },
            (3, 0): {
                "Name": "MaxDurationModulePwrUp",
                "Description": "Encoded maximum duration of the ModulePwrUp state (see Table 8-43)",
                "Type": ["RO", "Rqd"],
                "Template": "Duration",
            },
        },
        168: {
            (7, 4): {
                "Name": "MaxDurationDPTxTurnOff",
                "Description": "Encoded maximum duration of the DPTxTurnOff state (see Table 8-43)",
                "Type": ["RO", "Rqd"],
                "Template": "Duration",
            },
            (3, 0): {
                "Name": "MaxDurationDPTxTurnOn",
                "Description": "Encoded maximum duration of the DPTxTurnOn state (see Table 8-43)",
                "Type": ["RO", "Rqd"],
                "Template": "Duration",
            },
        },
        169: {(7, 0): {"Name": "Reserved", "Description": "Reserved", "Type": ["RO"]}},
        "Duration": {
            "Values": {
                0b0000: ("T_state < 1 ms", "LESS_THAN_1_MS"),
                0b0001: ("1 ms <= T_state < 5 ms", "BETWEEN_1_AND_5_MS"),
                0b0010: ("5 ms <= T_state < 10 ms", "BETWEEN_5_AND_10_MS"),
                0b0011: ("10 ms <= T_state < 50 ms", "BETWEEN_10_AND_50_MS"),
                0b0100: ("50 ms <= T_state < 100 ms", "BETWEEN_50_AND_100_MS"),
                0b0101: ("100 ms <= T_state < 500 ms", "BETWEEN_100_AND_500_MS"),
                0b0110: ("500 ms <= T_state < 1 s", "BETWEEN_500_MS_AND_1_S"),
                0b0111: ("1 s <= T_state < 5 s", "BETWEEN_1_AND_5_S"),
                0b1000: ("5 s <= T_state < 10 s", "BETWEEN_5_AND_10_S"),
                0b1001: ("10 s <= T_state < 1 min", "BETWEEN_10_S_AND_1_MIN"),
                0b1010: ("1 min <= T_state < 5 min", "BETWEEN_1_AND_5_MIN"),
                0b1011: ("5 min <= T_state < 10 min", "BETWEEN_5_AND_10_MIN"),
                0b1100: ("10 min <= T_state < 50 min", "BETWEEN_10_AND_50_MIN"),
                0b1101: ("T_state >= 50 min", "GREATER_THAN_50_MIN"),
                0b1110: ("Reserved", "RESERVED"),
                0b1111: ("Reserved", "RESERVED"),
            }
        },
    },
}
