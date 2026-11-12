from constants.generated_results import GeneratedResults
from constants.properties_columns import PropertiesColumns

STATIC_PROPERTIES_PLOTS = [

    {
        "file_path":
            f"{GeneratedResults.STATIC_PROPERTIES_DIRECTORY}/"
            "voltage_V_static_properties.csv",

        "y_column":
            PropertiesColumns.RISING_STEADY_STATE_VALUE,

        "y_label":
            "Rising Steady-State Voltage [V]"
    },

    {
        "file_path":
            f"{GeneratedResults.STATIC_PROPERTIES_DIRECTORY}/"
            "current_mA_static_properties.csv",

        "y_column":
            PropertiesColumns.RISING_STEADY_STATE_VALUE,

        "y_label":
            "Rising Steady-State Current [mA]"
    },

    {
        "file_path":
            f"{GeneratedResults.STATIC_PROPERTIES_DIRECTORY}/"
            "power_mW_static_properties.csv",

        "y_column":
            PropertiesColumns.RISING_STEADY_STATE_VALUE,

        "y_label":
            "Rising Steady-State Power [mW]"
    }
]