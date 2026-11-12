from constants.csv_columns import CSVColumns


class GeneratedResults:

    STATIC_PROPERTIES_DIRECTORY = (
        "datasets_static_properties_csv"
    )

    DYNAMIC_PROPERTIES_DIRECTORY = (
        "datasets_dynamic_properties_csv"
    )

    VARIABLES_STATIC = [
        CSVColumns.TEMPERATURE_HOT_COLUMN,
        CSVColumns.TEMPERATURE_COLD_COLUMN,
        CSVColumns.TEMPERATURE_DIFFERENCE_COLUMN,
        CSVColumns.CURRENT_COLUMN,
        CSVColumns.VOLTAGE_COLUMN,
        CSVColumns.POWER_COLUMN,
        # CSVColumns.SEEBECK_COEFFICIENT_COLUMN
    ]

    VARIABLES_DYNAMIC= [
        CSVColumns.TEMPERATURE_HOT_COLUMN,
        CSVColumns.TEMPERATURE_COLD_COLUMN,
        CSVColumns.TEMPERATURE_DIFFERENCE_COLUMN,
        CSVColumns.CURRENT_COLUMN,
        CSVColumns.VOLTAGE_COLUMN,
        # CSVColumns.POWER_COLUMN,
        # CSVColumns.SEEBECK_COEFFICIENT_COLUMN
    ]

    STATIC_PROPERTIES_FILE_PATHS = [
        (
            "datasets_static_properties_csv/"
            f"{variable}_static_properties.csv"
        )
        for variable in VARIABLES_STATIC
    ]

    DYNAMIC_PROPERTIES_RISING_FILE_PATHS = [
        (
            "datasets_dynamic_properties_csv/"
            f"{variable}_rising_dynamic_properties.csv"
        )
        for variable in VARIABLES_DYNAMIC
    ]

    DYNAMIC_PROPERTIES_FALLING_FILE_PATHS = [
        (
            "datasets_dynamic_properties_csv/"
            f"{variable}_falling_dynamic_properties.csv"
        )
        for variable in VARIABLES_DYNAMIC
    ]