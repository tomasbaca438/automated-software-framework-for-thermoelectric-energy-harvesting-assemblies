from constants.csv_columns import CSVColumns
import os

class GeneratedResults:

    RESULTS_DIRECTORY = (
        "results"
    )

    os.makedirs(
        RESULTS_DIRECTORY,
        exist_ok=True
    )

    STATIC_PROPERTIES_DIRECTORY = os.path.join(
        RESULTS_DIRECTORY,
        "datasets_static_properties_csv"
    )

    DYNAMIC_PROPERTIES_DIRECTORY = os.path.join(
        RESULTS_DIRECTORY,
        "datasets_dynamic_properties_csv"
    )

    NLS_DYNAMIC_PROPERTIES_DIRECTORY = os.path.join(
        RESULTS_DIRECTORY,
        "datasets_nls_dynamic_properties_csv"
    )

    FIRST_ORDER_VALIDATION_DIRECTORY = os.path.join(
        RESULTS_DIRECTORY,
        "datasets_first_order_validation_csv"
    )

    CORRELATION_ANALYSIS_DIRECTORY = (
        f"{RESULTS_DIRECTORY}/"
        "datasets_correlation_analysis_csv"
    )

    VARIABLES_GENERATED_RESULTS = [
        CSVColumns.TEMPERATURE_HOT_COLUMN,
        CSVColumns.TEMPERATURE_COLD_COLUMN,
        CSVColumns.TEMPERATURE_DIFFERENCE_COLUMN,
        CSVColumns.CURRENT_COLUMN,
        CSVColumns.VOLTAGE_COLUMN,
        CSVColumns.POWER_COLUMN,
    ]

class GeneratedResultsFilePaths:
    STATIC_PROPERTIES_FILE_PATHS = [
        (
            f"{GeneratedResults.STATIC_PROPERTIES_DIRECTORY}/"
            f"{variable}_static_properties.csv"
        )
        for variable in GeneratedResults.VARIABLES_GENERATED_RESULTS
    ]

    DYNAMIC_PROPERTIES_RISING_FILE_PATHS = [
        (
            f"{GeneratedResults.DYNAMIC_PROPERTIES_DIRECTORY}/"
            f"{variable}_rising_dynamic_properties.csv"
        )
        for variable in GeneratedResults.VARIABLES_GENERATED_RESULTS
    ]

    DYNAMIC_PROPERTIES_FALLING_FILE_PATHS = [
        (
            f"{GeneratedResults.DYNAMIC_PROPERTIES_DIRECTORY}/"
            f"{variable}_falling_dynamic_properties.csv"
        )
        for variable in GeneratedResults.VARIABLES_GENERATED_RESULTS
    ]

    NLS_DYNAMIC_PROPERTIES_RISING_FILE_PATHS = [
        (
            f"{GeneratedResults.NLS_DYNAMIC_PROPERTIES_DIRECTORY}/"
            f"{variable}_rising_nls_dynamic_properties.csv"
        )
        for variable in
        GeneratedResults.VARIABLES_GENERATED_RESULTS
    ]

    NLS_DYNAMIC_PROPERTIES_FALLING_FILE_PATHS = [
        (
            f"{GeneratedResults.NLS_DYNAMIC_PROPERTIES_DIRECTORY}/"
            f"{variable}_falling_nls_dynamic_properties.csv"
        )
        for variable in
        GeneratedResults.VARIABLES_GENERATED_RESULTS
    ]

    FIRST_ORDER_VALIDATION_RISING_FILE_PATHS = [
        (
            f"{GeneratedResults.FIRST_ORDER_VALIDATION_DIRECTORY}/"
            f"{variable}_rising_first_order_validation.csv"
        )
        for variable in GeneratedResults.VARIABLES_GENERATED_RESULTS
    ]

    FIRST_ORDER_VALIDATION_FALLING_FILE_PATHS = [
        (
            f"{GeneratedResults.FIRST_ORDER_VALIDATION_DIRECTORY}/"
            f"{variable}_falling_first_order_validation.csv"
        )
        for variable in GeneratedResults.VARIABLES_GENERATED_RESULTS
    ]

    RISING_TAU_CORRELATION_MATRIX = (
        f"{GeneratedResults.CORRELATION_ANALYSIS_DIRECTORY}/"
        "rising_tau_correlation_matrix.csv"
    )

    FALLING_TAU_CORRELATION_MATRIX = (
        f"{GeneratedResults.CORRELATION_ANALYSIS_DIRECTORY}/"
        "falling_tau_correlation_matrix.csv"
    )

    RISING_NLS_TAU_CORRELATION_MATRIX = (
        f"{GeneratedResults.CORRELATION_ANALYSIS_DIRECTORY}/"
        "rising_nls_tau_correlation_matrix.csv"
    )

    FALLING_NLS_TAU_CORRELATION_MATRIX = (
        f"{GeneratedResults.CORRELATION_ANALYSIS_DIRECTORY}/"
        "falling_nls_tau_correlation_matrix.csv"
    )



