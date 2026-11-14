from analyzers.dynamic_properties_analyzer import DynamicPropertiesAnalyzer
from analyzers.static_properties_analyzer import StaticPropertiesAnalyzer
from constants.generated_results import GeneratedResults, GeneratedResultsFilePaths
from csv_mergers.csv_merger import CSVMerger
from first_order_model_validator.first_order_model_validator import FirstOrderModelValidator
from plotters.properties_plot_generator import PropertiesPlotGenerator
from plotters.step_response_plotter import StepResponseAnalyzer
from configurations import datasets
from configurations import plots
from table_generators.generating_table import TableGenerator
from correlation_analysis.time_constant_correlation_analyzer import TimeConstantCorrelationAnalyzer

csv_merger = CSVMerger()
step_response_analyzer = StepResponseAnalyzer()
static_properties_analyzer: StaticPropertiesAnalyzer = StaticPropertiesAnalyzer()
dynamic_properties_analyzer: DynamicPropertiesAnalyzer = DynamicPropertiesAnalyzer()
table_generator: TableGenerator = TableGenerator()
properties_plot_generator: PropertiesPlotGenerator = PropertiesPlotGenerator()
first_order_model_validator: FirstOrderModelValidator = FirstOrderModelValidator()
time_constant_correlation_analysis:TimeConstantCorrelationAnalyzer = TimeConstantCorrelationAnalyzer()

# merging datasets

csv_merger.merge_datasets(
    temperature_file_paths=datasets.TEMPERATURE_FILE_PATHS,
    voltage_current_file_paths=datasets.VOLTAGE_CURRENT_FILE_PATHS,
    merged_file_paths=datasets.MERGED_FILE_PATHS
)

# plotting step responses

for plot in plots.STEP_RESPONSE_PLOTS:
    step_response_analyzer.plot_step_response(
        file_paths=datasets.MERGED_FILE_PATHS,
        labels=datasets.LABELS,
        x_column=plot["x_column"],
        y_column=plot["y_column"],
        x_label=plot["x_label"],
        y_label=plot["y_label"],
        plot_type=plot["plot_type"]
    )


# calculating static and dynamic properties

static_properties_analyzer.generate_static_properties_csvs(
    merged_file_paths=datasets.MERGED_FILE_PATHS,
    labels=datasets.LABELS,
    output_directory=GeneratedResults
        .STATIC_PROPERTIES_DIRECTORY,
    switch_sample=900
)

dynamic_properties_analyzer.generate_dynamic_properties_csvs(
    merged_file_paths=datasets.MERGED_FILE_PATHS,
    labels=datasets.LABELS,
    switch_sample=900,
    sampling_period_s=1.0
)

dynamic_properties_analyzer.generate_nls_dynamic_properties_csvs(
    merged_file_paths=datasets.MERGED_FILE_PATHS,
    labels=datasets.LABELS,
    switch_sample=900,
    sampling_period_s=1.0
)

# table_generator.print_tables(
#     file_paths=
#     GeneratedResultsFilePaths
#     .STATIC_PROPERTIES_FILE_PATHS
# )
#
# table_generator.print_tables(
#     file_paths=
#     GeneratedResultsFilePaths
#     .DYNAMIC_PROPERTIES_RISING_FILE_PATHS
# )
#
# table_generator.print_tables(
#     file_paths=
#     GeneratedResultsFilePaths
#     .DYNAMIC_PROPERTIES_FALLING_FILE_PATHS
# )
#
# table_generator.print_tables(
#     file_paths=
#     GeneratedResultsFilePaths
#     .NLS_DYNAMIC_PROPERTIES_RISING_FILE_PATHS
# )
#
# table_generator.print_tables(
#     file_paths=
#     GeneratedResultsFilePaths
#     .NLS_DYNAMIC_PROPERTIES_FALLING_FILE_PATHS
# )

table_generator.generate_latex_tables(file_paths=
    GeneratedResultsFilePaths.STATIC_PROPERTIES_FILE_PATHS, two_collumns=False, squeeze_table=False)

table_generator.generate_latex_tables(file_paths=
    GeneratedResultsFilePaths
    .DYNAMIC_PROPERTIES_RISING_FILE_PATHS, two_collumns=True, squeeze_table=False)

table_generator.generate_latex_tables(file_paths=
    GeneratedResultsFilePaths
    .DYNAMIC_PROPERTIES_FALLING_FILE_PATHS, two_collumns=True, squeeze_table=False)

table_generator.generate_latex_tables(file_paths=
    GeneratedResultsFilePaths
    .NLS_DYNAMIC_PROPERTIES_RISING_FILE_PATHS, two_collumns=True, squeeze_table=False)

table_generator.generate_latex_tables(file_paths=
    GeneratedResultsFilePaths
    .NLS_DYNAMIC_PROPERTIES_FALLING_FILE_PATHS, two_collumns=True, squeeze_table=False)


# correlation analysis

time_constant_correlation_analysis.calculate_correlation_matrix(
    file_paths=
    GeneratedResultsFilePaths
    .DYNAMIC_PROPERTIES_RISING_FILE_PATHS,

    output_file_path=
    GeneratedResultsFilePaths
    .RISING_TAU_CORRELATION_MATRIX
)

time_constant_correlation_analysis.calculate_correlation_matrix(
    file_paths=
    GeneratedResultsFilePaths
    .DYNAMIC_PROPERTIES_FALLING_FILE_PATHS,

    output_file_path=
    GeneratedResultsFilePaths
    .FALLING_TAU_CORRELATION_MATRIX
)

time_constant_correlation_analysis.calculate_correlation_matrix(
    file_paths=
    GeneratedResultsFilePaths
    .NLS_DYNAMIC_PROPERTIES_RISING_FILE_PATHS,

    output_file_path=
    GeneratedResultsFilePaths
    .RISING_NLS_TAU_CORRELATION_MATRIX
)

time_constant_correlation_analysis.calculate_correlation_matrix(
    file_paths=
    GeneratedResultsFilePaths
    .NLS_DYNAMIC_PROPERTIES_FALLING_FILE_PATHS,

    output_file_path=
    GeneratedResultsFilePaths
    .FALLING_NLS_TAU_CORRELATION_MATRIX
)

# table_generator.print_tables(
#     file_paths=[
#         GeneratedResultsFilePaths
#         .RISING_TAU_CORRELATION_MATRIX,
#         GeneratedResultsFilePaths
#         .FALLING_TAU_CORRELATION_MATRIX,
#         GeneratedResultsFilePaths
#         .RISING_NLS_TAU_CORRELATION_MATRIX,
#         GeneratedResultsFilePaths
#         .FALLING_NLS_TAU_CORRELATION_MATRIX
#     ]
# )

table_generator.generate_latex_tables(file_paths=[
    GeneratedResultsFilePaths
    .RISING_TAU_CORRELATION_MATRIX,
    GeneratedResultsFilePaths
    .FALLING_TAU_CORRELATION_MATRIX,
    GeneratedResultsFilePaths
    .RISING_NLS_TAU_CORRELATION_MATRIX,
    GeneratedResultsFilePaths
    .FALLING_NLS_TAU_CORRELATION_MATRIX
], two_collumns=False, squeeze_table=True)



# generating plots of static and dynamic properties

PropertiesPlotGenerator.generate_all_static_property_plots()
PropertiesPlotGenerator.generate_all_dynamic_property_comparison_plots()

# validating the calculated time constants fit to first order differential equation model

first_order_model_validator.run_validation()

# table_generator.print_tables(
#     file_paths=
#     GeneratedResultsFilePaths
#     .FIRST_ORDER_VALIDATION_RISING_FILE_PATHS
# )
#
# table_generator.print_tables(
#     file_paths=
#     GeneratedResultsFilePaths
#     .FIRST_ORDER_VALIDATION_FALLING_FILE_PATHS
# )

table_generator.generate_latex_tables(file_paths=
    GeneratedResultsFilePaths
    .FIRST_ORDER_VALIDATION_RISING_FILE_PATHS, two_collumns=False, squeeze_table=True)

table_generator.generate_latex_tables(file_paths=
    GeneratedResultsFilePaths
    .FIRST_ORDER_VALIDATION_FALLING_FILE_PATHS, two_collumns=False, squeeze_table=True)

