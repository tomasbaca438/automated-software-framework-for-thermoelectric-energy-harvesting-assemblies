from constants.csv_columns import CSVColumns
from constants.plot_labels import PlotLabels
from constants.plot_types import PlotTypes

STEP_RESPONSE_PLOTS = [
    {
        "x_column": CSVColumns.SAMPLE_COLUMN,
        "y_column": CSVColumns.TEMPERATURE_HOT_COLUMN,
        "x_label": PlotLabels.SAMPLE,
        "y_label": PlotLabels.TEMPERATURE_HOT,
        "plot_type": PlotTypes.LINE
    },
    {
        "x_column": CSVColumns.SAMPLE_COLUMN,
        "y_column": CSVColumns.TEMPERATURE_COLD_COLUMN,
        "x_label": PlotLabels.SAMPLE,
        "y_label": PlotLabels.TEMPERATURE_COLD,
        "plot_type": PlotTypes.LINE
    },
    {
        "x_column": CSVColumns.SAMPLE_COLUMN,
        "y_column": CSVColumns.TEMPERATURE_DIFFERENCE_COLUMN,
        "x_label": PlotLabels.SAMPLE,
        "y_label": PlotLabels.TEMPERATURE_DIFFERENCE,
        "plot_type": PlotTypes.LINE
    },
    {
        "x_column": CSVColumns.SAMPLE_COLUMN,
        "y_column": CSVColumns.VOLTAGE_COLUMN,
        "x_label": PlotLabels.SAMPLE,
        "y_label": PlotLabels.VOLTAGE,
        "plot_type": PlotTypes.LINE
    },
    {
        "x_column": CSVColumns.SAMPLE_COLUMN,
        "y_column": CSVColumns.CURRENT_COLUMN,
        "x_label": PlotLabels.SAMPLE,
        "y_label": PlotLabels.CURRENT,
        "plot_type": PlotTypes.LINE
    },
    {
        "x_column": CSVColumns.SAMPLE_COLUMN,
        "y_column": CSVColumns.POWER_COLUMN,
        "x_label": PlotLabels.SAMPLE,
        "y_label": PlotLabels.POWER,
        "plot_type": PlotTypes.LINE
    },
    {
        "x_column": CSVColumns.SAMPLE_COLUMN,
        "y_column": CSVColumns.SEEBECK_COEFFICIENT_COLUMN,
        "x_label": PlotLabels.SAMPLE,
        "y_label": PlotLabels.SEEBECK_COEFFICIENT,
        "plot_type": PlotTypes.LINE
    },
    {
        "x_column": CSVColumns.TEMPERATURE_DIFFERENCE_COLUMN,
        "y_column": CSVColumns.POWER_COLUMN,
        "x_label": PlotLabels.TEMPERATURE_DIFFERENCE,
        "y_label": PlotLabels.POWER,
        "plot_type": PlotTypes.SCATTER
    },
    {
        "x_column": CSVColumns.TEMPERATURE_DIFFERENCE_COLUMN,
        "y_column": CSVColumns.VOLTAGE_COLUMN,
        "x_label": PlotLabels.TEMPERATURE_DIFFERENCE,
        "y_label": PlotLabels.VOLTAGE,
        "plot_type": PlotTypes.SCATTER
    },
    {
        "x_column": CSVColumns.TEMPERATURE_DIFFERENCE_COLUMN,
        "y_column": CSVColumns.CURRENT_COLUMN,
        "x_label": PlotLabels.TEMPERATURE_DIFFERENCE,
        "y_label": PlotLabels.CURRENT,
        "plot_type": PlotTypes.SCATTER
    },
    {
        "x_column": CSVColumns.TEMPERATURE_DIFFERENCE_COLUMN,
        "y_column": CSVColumns.SEEBECK_COEFFICIENT_COLUMN,
        "x_label": PlotLabels.TEMPERATURE_DIFFERENCE,
        "y_label": PlotLabels.SEEBECK_COEFFICIENT,
        "plot_type": PlotTypes.SCATTER
    },
    {
        "x_column": CSVColumns.VOLTAGE_COLUMN,
        "y_column": CSVColumns.CURRENT_COLUMN,
        "x_label": PlotLabels.VOLTAGE,
        "y_label": PlotLabels.CURRENT,
        "plot_type": PlotTypes.SCATTER
    },
    {
        "x_column": CSVColumns.VOLTAGE_COLUMN,
        "y_column": CSVColumns.POWER_COLUMN,
        "x_label": PlotLabels.VOLTAGE,
        "y_label": PlotLabels.POWER,
        "plot_type": PlotTypes.SCATTER
    }
]