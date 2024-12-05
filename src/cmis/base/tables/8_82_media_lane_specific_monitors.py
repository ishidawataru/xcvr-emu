info = {
    "Name": "MediaLaneSpecificMonitors",
    "Description": "CMIS v5.2 Table 8-82 Media Lane-Specific Monitors (Page 11h)",
    "Page": 0x11,
    "Table": {
        "OpticalPowerTx": {
            "Description": "Internally measured Tx output optical power: in 0.1 µW increments, yielding a total measurement range of 0 to 6.5535 mW (~-40 to +8.2 dBm for non-zero values).",
            "Type": ["RO", "Adv"],
            "Advertisement": "01h:160.1",
        },
        "LaserBiasTx": {
            "Description": "Internally measured Tx bias current monitor: in 2 µA increments, times the multiplier from Table 8-47.",
            "Type": ["RO", "Adv"],
            "Advertisement": "01h:160.0",
        },
        "OpticalPowerRx": {
            "Description": "Internally measured Rx input optical power: in 0.1 µW increments, yielding a total measurement range of 0 to 6.5535 mW (~-40 to +8.2 dBm for non-zero values).",
            "Type": ["RO", "Adv"],
            "Advertisement": "01h:160.2",
        },
        range(154, 170, 2): {
            "Template": "OpticalPowerTx",
        },
        range(170, 186, 2): {
            "Template": "LaserBiasTx",
        },
        range(186, 202, 2): {
            "Template": "OpticalPowerRx",
        },
    },
}
