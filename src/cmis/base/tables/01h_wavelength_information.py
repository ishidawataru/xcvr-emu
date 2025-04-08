info = {
    "Name": "WavelengthInformation",
    "Description": "CMIS v5.2 8.3.7 Wavelength Information",
    "Page": 1,
    "Table": {
        (138, 139): {
            (7, 0): {
                "Name": "NominalWavelength",
                "Description": "U16 nominal transmitter output wavelength for a single wavelength module at room temperature in units of 0.05 nm",
                "Type": ["RO", "Cnd"],
            }
        },
        (140, 141): {
            (7, 0): {
                "Name": "WavelengthTolerance",
                "Description": "U16 wavelength tolerance tol as the worst case +/-tol range around the NominalWavelength under all normal operating conditions in units of 0.005 nm",
                "Type": ["RO", "Cnd"],
            }
        },
    },
}
