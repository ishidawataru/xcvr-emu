info = {
    "Name": "LaneSpecificMasks",
    "Description": "CMIS v5.2 Table 8-74 Lane-Specific Masks (Page 10h)",
    "Page": 0x10,
    "Table": {
        213: {
            range(0, 8): {
                "Name": "DPStateChangedMask",
                "Description": "Mask for DPStateChangedFlag<i> for Data Path of host lane <i>",
                "Type": ["RW", "Rqd"],
            },
        },
        214: {
            range(0, 8): {
                "Name": "FailureMaskTx",
                "Description": "Mask for FailureFlagTx<i>, affecting media lane <i>",
                "Type": ["RW", "Adv"],
            },
        },
        215: {
            range(0, 8): {
                "Name": "LOSMaskTx",
                "Description": "Mask for LOSFlagTx<i>, lane <i>",
                "Type": ["RW", "Adv"],
            },
        },
        216: {
            range(0, 8): {
                "Name": "CDRLOLMaskTx",
                "Description": "Mask for CDRLOLFlagTx<i>, lane <i>",
                "Type": ["RW", "Adv"],
            },
        },
        217: {
            range(0, 8): {
                "Name": "AdaptiveInputEqFailMaskTx",
                "Description": "Mask for AdaptiveInputEqFailFlagTx<i>, lane <i>",
                "Type": ["RW", "Adv"],
            },
        },
        218: {
            range(0, 8): {
                "Name": "OpticalPowerHighAlarmMaskTx",
                "Description": "Mask for OpticalPowerHighAlarmFlagTx<i>, media lane <i>",
                "Type": ["RW", "Adv"],
            },
        },
        219: {
            range(0, 8): {
                "Name": "OpticalPowerLowAlarmMaskTx",
                "Description": "Mask for OpticalPowerLowAlarmFlagTx<i>, media lane <i>",
                "Type": ["RW", "Adv"],
            },
        },
        220: {
            range(0, 8): {
                "Name": "OpticalPowerHighWarningMaskTx",
                "Description": "Mask for OpticalPowerHighWarningFlagTx<i>, media lane <i>",
                "Type": ["RW", "Adv"],
            },
        },
        221: {
            range(0, 8): {
                "Name": "OpticalPowerLowWarningMaskTx",
                "Description": "Mask for OpticalPowerLowWarningFlagTx<i>, media lane <i>",
                "Type": ["RW", "Adv"],
            },
        },
        222: {
            range(0, 8): {
                "Name": "LaserBiasHighAlarmMaskTx",
                "Description": "Mask for LaserBiasHighAlarmFlagTx<i>, media lane <i>",
                "Type": ["RW", "Adv"],
            },
        },
        223: {
            range(0, 8): {
                "Name": "LaserBiasLowAlarmMaskTx",
                "Description": "Mask for LaserBiasLowAlarmFlagTx<i>, media lane <i>",
                "Type": ["RW", "Adv"],
            },
        },
        224: {
            range(0, 8): {
                "Name": "LaserBiasHighWarningMaskTx",
                "Description": "Mask for LaserBiasHighWarningFlagTx<i>, media lane <i>",
                "Type": ["RW", "Adv"],
            },
        },
        225: {
            range(0, 8): {
                "Name": "LaserBiasLowWarningMaskTx",
                "Description": "Mask for LaserBiasLowWarningFlagTx<i>, media lane <i>",
                "Type": ["RW", "Adv"],
            },
        },
        226: {
            range(0, 8): {
                "Name": "LOSMaskRx",
                "Description": "Mask for LOSFlagRx<i>, media lane <i>",
                "Type": ["RW", "Adv"],
            },
        },
        227: {
            range(0, 8): {
                "Name": "CDRLOLMaskRx",
                "Description": "Mask for CDRLOLFlagRx<i>, media lane <i>",
                "Type": ["RW", "Adv"],
            },
        },
        228: {
            range(0, 8): {
                "Name": "OpticalPowerHighAlarmMaskRx",
                "Description": "Mask for OpticalPowerHighAlarmFlagRx<i>, media lane <i>",
                "Type": ["RW", "Adv"],
            },
        },
        229: {
            range(0, 8): {
                "Name": "OpticalPowerLowAlarmMaskRx",
                "Description": "Mask for OpticalPowerLowAlarmFlagRx<i>, media lane <i>",
                "Type": ["RW", "Adv"],
            },
        },
        230: {
            range(0, 8): {
                "Name": "OpticalPowerHighWarningMaskRx",
                "Description": "Mask for OpticalPowerHighWarningFlagRx<i>, media lane <i>",
                "Type": ["RW", "Adv"],
            },
        },
        231: {
            range(0, 8): {
                "Name": "OpticalPowerLowWarningMaskRx",
                "Description": "Mask for OpticalPowerLowWarningFlagRx<i>, media lane <i>",
                "Type": ["RW", "Adv"],
            },
        },
        232: {
            range(0, 8): {
                "Name": "OutputStatusChangedMaskRx",
                "Description": "Mask for OutputStatusChangedFlagRx<i>, media lane <i>",
                "Type": ["RW", "Rqd"],
            },
        },
    },
}
