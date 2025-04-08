info = {
    "Name": "MediaLaneAssignmentAdvertising",
    "Description": "CMIS v5.2 Table 8-52 Media Lane Assignment Advertising (Page 01h)",
    "Page": 1,
    "Table": {
        "MediaLaneAssignmentOptions": {
            "Description": (
                "Media Lane Assignment Options for the Application advertised in the "
                "Application descriptor identified by AppSel <i>. Bits 0-7 form a bit map "
                "corresponding to Media Lanes 1-8. A set bit indicates that a Data Path for "
                "the Application is allowed to begin on the corresponding Media Lane."
            ),
            "Type": ["RO", "Rqd"],
        },
        range(176, 191): {
            "Template": "MediaLaneAssignmentOptions",
        },
    },
}
