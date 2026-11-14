import os

from constants.generated_results import (
    GeneratedResults
)

class TableDirectories:
    GENERATED_TABLES_DIRECTORY = os.path.join(
        GeneratedResults.RESULTS_DIRECTORY,
        "generated_tables"
    )
    STATIC_PROPERTIES_SUBDIRECTORY: str = "static_properties"
    RISING_DYNAMIC_PROPERTIES_SUBDIRECTORY: str = "rising_dynamic_properties"
    FALLING_DYNAMIC_PROPERTIES_SUBDIRECTORY: str = "falling_dynamic_properties"
    RISING_FIRST_ORDER_VALIDATION_SUBDIRECTORY:str = "rising_first_order_validation"
    FALLING_FIRST_ORDER_VALIDATION_SUBDIRECTORY: str = "falling_first_order_validation"
    RISING_NLS_DYNAMIC_PROPERTIES_SUBDIRECTORY = (
        "rising_nls_dynamic_properties"
    )

    FALLING_NLS_DYNAMIC_PROPERTIES_SUBDIRECTORY = (
        "falling_nls_dynamic_properties"
    )

    TAU_CORRELATION_SUBDIRECTORY = (
        "tau_correlation"
    )


    GENERATED_FILES_EXTENSION: str = "tex"