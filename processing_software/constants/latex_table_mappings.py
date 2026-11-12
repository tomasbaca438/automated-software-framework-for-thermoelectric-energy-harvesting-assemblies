from constants.properties_columns import (
    PropertiesColumns
)

from constants.latex_table_columns import (
    LatexTableColumns
)


class LatexTableMappings:

    COLUMN_MAPPING = {

        PropertiesColumns.VARIABLE:
            LatexTableColumns.VARIABLE,

        PropertiesColumns.INITIAL_VALUE:
            LatexTableColumns.INITIAL_VALUE,

        PropertiesColumns.RISING_STEADY_STATE_VALUE:
            LatexTableColumns.RISING_STEADY_STATE_VALUE,

        PropertiesColumns.FALLING_STEADY_STATE_VALUE:
            LatexTableColumns.FALLING_STEADY_STATE_VALUE,

        PropertiesColumns.TAU_RISING_SAMPLES:
            LatexTableColumns.TAU_RISING_SAMPLES,

        PropertiesColumns.TAU_RISING_S:
            LatexTableColumns.TAU_RISING_S,

        PropertiesColumns.SETTLING_TIME_RISING_S:
            LatexTableColumns.SETTLING_TIME_RISING_S,

        PropertiesColumns.CUTOFF_FREQUENCY_RISING_HZ:
            LatexTableColumns.CUTOFF_FREQUENCY_RISING_HZ,

        PropertiesColumns.CUTOFF_PERIOD_RISING_S:
            LatexTableColumns.CUTOFF_PERIOD_RISING_S,

        PropertiesColumns.CUTOFF_PERIOD_RISING_MIN:
            LatexTableColumns.CUTOFF_PERIOD_RISING_MIN,

        PropertiesColumns.TAU_FALLING_SAMPLES:
            LatexTableColumns.TAU_FALLING_SAMPLES,

        PropertiesColumns.TAU_FALLING_S:
            LatexTableColumns.TAU_FALLING_S,

        PropertiesColumns.SETTLING_TIME_FALLING_S:
            LatexTableColumns.SETTLING_TIME_FALLING_S,

        PropertiesColumns.CUTOFF_FREQUENCY_FALLING_HZ:
            LatexTableColumns.CUTOFF_FREQUENCY_FALLING_HZ,

        PropertiesColumns.CUTOFF_PERIOD_FALLING_S:
            LatexTableColumns.CUTOFF_PERIOD_FALLING_S,

        PropertiesColumns.CUTOFF_PERIOD_FALLING_MIN:
            LatexTableColumns.CUTOFF_PERIOD_FALLING_MIN,

        PropertiesColumns.LOAD_RESISTANCE:
            LatexTableColumns.LOAD_RESISTANCE,
    }