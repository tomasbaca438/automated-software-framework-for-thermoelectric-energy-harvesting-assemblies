from constants.generated_results import GeneratedResults
from constants.properties_columns import PropertiesColumns

ORIGINAL_FILE = (
    f"{GeneratedResults.DYNAMIC_PROPERTIES_DIRECTORY}/"
    "temperature_difference_C"
    "_rising_dynamic_properties.csv"
)

NLS_FILE = (
    f"{GeneratedResults.NLS_DYNAMIC_PROPERTIES_DIRECTORY}/"
    "temperature_difference_C"
    "_rising_nls_dynamic_properties.csv"
)

DYNAMIC_PROPERTIES_PLOTS = [

    {
        "original_file_path": ORIGINAL_FILE,
        "nls_file_path": NLS_FILE,
        "y_column": PropertiesColumns.TAU_RISING_S,
        "y_label": "Thermal Time Constant [s]"
    },

    {
        "original_file_path": ORIGINAL_FILE,
        "nls_file_path": NLS_FILE,
        "y_column": PropertiesColumns.SETTLING_TIME_RISING_S,
        "y_label": "Settling Time [s]"
    },

    {
        "original_file_path": ORIGINAL_FILE,
        "nls_file_path": NLS_FILE,
        "y_column": PropertiesColumns.CUTOFF_FREQUENCY_RISING_HZ,
        "y_label": "Cutoff Frequency [Hz]"
    }
]