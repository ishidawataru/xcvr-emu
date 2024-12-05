info = {
    "Name": "ApplicationDescriptorRegisters",
    "Description": "CMIS v5.2 8.20 Application Descriptor Registers Bytes 1-4 (Lower Memory)",
    "Page": 0,
    "Table": {
        range(86, 118, 4): {
            "Template": "ApplicationDescriptor",
        },
        range(223, 251, 4): {
            "Template": "ApplicationDescriptor",
            "SuffixFunc": lambda x: str(x + 9),
        },
        "ApplicationDescriptor": {
            0: {
                "Name": "HostInterfaceID",
                "Description": "ID from [5] or FFh to mark as unused (empty Application Descriptor)",
                "Type": ["RO", "Rqd"],
            },
            1: {
                "Name": "MediaInterfaceID",
                "Description": "ID from a suitable table of IDs in [5] that is identified by the MediaType Byte 00h:85",
                "Type": ["RO", "Rqd"],
            },
            2: {
                (7, 4): {
                    "Name": "HostLaneCount",
                    "Description": "Lane count defined by interface ID",
                    "Values": {
                        0b0000: ("0 lanes (reserved)", "RESERVED"),
                        0b0001: ("1 lane", "ONE_LANE"),
                        0b0010: ("2 lanes", "TWO_LANES"),
                        0b0100: ("4 lanes", "FOUR_LANES"),
                        0b1000: ("8 lanes", "EIGHT_LANES"),
                        (0b1010, 0b1111): ("Reserved", "RESERVED"),
                    },
                },
                (3, 0): {
                    "Name": "MediaLaneCount",
                    "Description": "Number of lanes corresponding to Media Type",
                    "Values": {
                        0b0000: ("0 lanes (reserved)", "RESERVED"),
                        0b0001: ("1 lane", "ONE_LANE"),
                        0b0010: ("2 lanes", "TWO_LANES"),
                        0b0100: ("4 lanes", "FOUR_LANES"),
                        0b1000: ("8 lanes", "EIGHT_LANES"),
                        (0b1001, 0b1111): ("Reserved", "RESERVED"),
                    },
                },
            },
            3: {
                "Name": "HostLaneAssignmentOptions",
                "Description": "Bits 0-7 form a bit map corresponding to Host Lanes 1-8. A set bit indicates that the Application may begin on the corresponding host lane.",
                "Type": ["RO"],
            },
        },
    },
}
