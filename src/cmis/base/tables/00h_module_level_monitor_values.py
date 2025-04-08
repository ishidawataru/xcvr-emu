info = {
    "Name": "ModuleLevelMonitorValues",
    "Description": "CMIS v5.2 8.10 Module-Level Monitor Values",
    "Page": 0,
    "Table": {
        (14, 15): {
            (7, 0): {
                "Name": "TempMonValue",
                "Description": "S16 Module Temperature Monitor (Current Value) internally measured temperature in 1/256 degree Celsius increments.",
                "Type": ["RO", "Adv"],
            }
        },
        (16, 17): {
            (7, 0): {
                "Name": "VccMonVoltage",
                "Description": "U16 Supply Voltage Monitor (Current Value) internally measured input supply voltage in 100 µV increments.",
                "Type": ["RO", "Adv"],
            }
        },
        (18, 19): {
            (7, 0): {
                "Name": "Aux1MonValue",
                "Description": "S16 Aux1 Monitor (Current Value).",
                "Details": [
                    "The monitored observable is advertised in 01h:145.0:",
                    "0b: Custom",
                    "1b: TEC Current in 100%/32767 increments of maximum TEC current magnitude.",
                    "+32767 (100%) of the max current magnitude when heating.",
                    "-32767 is -100% of the max current magnitude when cooling.",
                ],
                "Type": ["RO", "Adv"],
            }
        },
        (20, 21): {
            (7, 0): {
                "Name": "Aux2MonValue",
                "Description": "S16 Aux2 Monitor (Current Value).",
                "Details": [
                    "The monitored observable is advertised in 01h:145.1:",
                    "0b: Laser Temperature in 1/256 degree Celsius increments.",
                    "1b: TEC Current in 100%/32767 increments of maximum TEC current magnitude.",
                    "+32767 (100%) of the max current magnitude when heating.",
                    "-32767 is -100% of the max current magnitude when cooling.",
                ],
                "Type": ["RO", "Adv"],
            }
        },
        (22, 23): {
            (7, 0): {
                "Name": "Aux3MonValue",
                "Description": "S16 Aux3 Monitor (Current Value).",
                "Details": [
                    "The monitored observable is advertised in 01h:145.2:",
                    "0b: Laser Temperature in 1/256 degree Celsius increments.",
                    "1b: Additional Supply Voltage in 100 µV increments.",
                ],
                "Type": ["RO", "Adv"],
            }
        },
        (24, 25): {
            (7, 0): {
                "Name": "CustomMonValue",
                "Description": "S16 or U16: Custom monitor (Current Value).",
                "Type": ["RO", "Adv"],
            }
        },
    },
}
