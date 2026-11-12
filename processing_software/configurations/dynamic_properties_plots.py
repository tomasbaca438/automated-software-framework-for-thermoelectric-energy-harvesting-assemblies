from constants.generated_results import GeneratedResults
from constants.properties_columns import PropertiesColumns

DYNAMIC_PROPERTIES_PLOTS = [

    {
        "file_path":
            (
                f"{GeneratedResults.DYNAMIC_PROPERTIES_DIRECTORY}/"
                "temperature_difference_C"
                "_rising_dynamic_properties.csv"
            ),

        "y_column":
            PropertiesColumns.TAU_RISING_S,

        "y_label":
            "Thermal Time Constant [s]"
    },

    {
        "file_path":
            (
                f"{GeneratedResults.DYNAMIC_PROPERTIES_DIRECTORY}/"
                "temperature_difference_C"
                "_rising_dynamic_properties.csv"
            ),

        "y_column":
            PropertiesColumns.SETTLING_TIME_RISING_S,

        "y_label":
            "Settling Time [s]"
    },

    {
        "file_path":
            (
                f"{GeneratedResults.DYNAMIC_PROPERTIES_DIRECTORY}/"
                "temperature_difference_C"
                "_rising_dynamic_properties.csv"
            ),

        "y_column":
            PropertiesColumns.CUTOFF_FREQUENCY_RISING_HZ,

        "y_label":
            "Cutoff Frequency [Hz]"
    }
]