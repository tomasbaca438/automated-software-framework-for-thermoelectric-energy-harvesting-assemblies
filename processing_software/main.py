from analyzers.dynamic_properties_analyzer import DynamicPropertiesAnalyzer
from analyzers.static_properties_analyzer import StaticPropertiesAnalyzer
from constants.generated_results import GeneratedResults
from csv_mergers.csv_merger import CSVMerger
from plotters.properties_plot_generator import PropertiesPlotGenerator
from plotters.step_response_plotter import StepResponseAnalyzer
from configurations import datasets
from configurations import plots
from table_generators.generating_table import TableGenerator

csv_merger = CSVMerger()
step_response_analyzer = StepResponseAnalyzer()
static_properties_analyzer: StaticPropertiesAnalyzer = StaticPropertiesAnalyzer()
dynamic_properties_analyzer: DynamicPropertiesAnalyzer = DynamicPropertiesAnalyzer()
table_generator: TableGenerator = TableGenerator()
properties_plot_generator: PropertiesPlotGenerator = PropertiesPlotGenerator()

csv_merger.merge_datasets(
    temperature_file_paths=datasets.TEMPERATURE_FILE_PATHS,
    voltage_current_file_paths=datasets.VOLTAGE_CURRENT_FILE_PATHS,
    merged_file_paths=datasets.MERGED_FILE_PATHS
)

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

table_generator.print_tables(
    file_paths=
    GeneratedResults.STATIC_PROPERTIES_FILE_PATHS
)

table_generator.print_tables(
    file_paths=
    GeneratedResults
    .DYNAMIC_PROPERTIES_RISING_FILE_PATHS
)

table_generator.print_tables(
    file_paths=
    GeneratedResults
    .DYNAMIC_PROPERTIES_FALLING_FILE_PATHS
)

table_generator.generate_latex_tables(file_paths=
    GeneratedResults.STATIC_PROPERTIES_FILE_PATHS)

table_generator.generate_latex_tables(file_paths=
    GeneratedResults
    .DYNAMIC_PROPERTIES_RISING_FILE_PATHS)

table_generator.generate_latex_tables(file_paths=
    GeneratedResults
    .DYNAMIC_PROPERTIES_FALLING_FILE_PATHS)

PropertiesPlotGenerator.generate_all_static_property_plots()

PropertiesPlotGenerator.generate_all_dynamic_property_plots()