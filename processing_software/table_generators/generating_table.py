import os

import pandas as pd

from tabulate import tabulate

from constants.latex_table_mappings import LatexTableMappings
from constants.latex_variables import LatexVariables
from constants.properties_columns import PropertiesColumns
from constants.tables_directories import (
    TableDirectories
)
from constants.latex_table_captions import (
    LatexTableCaptions
)
from constants.latex_load_resistances import (
    LatexLoadResistances
)


class TableGenerator:

    @staticmethod
    def print_tables(
        file_paths: list[str]
    ) -> None:

        for file_path in file_paths:

            df = pd.read_csv(
                file_path,
                sep=";"
            )

            print(f"\n{file_path}")

            print(
                tabulate(
                    df,
                    headers="keys",
                    tablefmt="grid",
                    showindex=False
                )
            )

    @staticmethod
    def generate_latex_tables(
        file_paths: list[str]
    ) -> None:

        for file_path in file_paths:

            df = pd.read_csv(
                file_path,
                sep=";"
            )

            file_name = os.path.basename(
                file_path
            ).replace(".csv", ".tex")

            if "static_properties" in file_path:

                output_directory = os.path.join(
                    TableDirectories.GENERATED_TABLES_DIRECTORY,
                    TableDirectories.STATIC_PROPERTIES_SUBDIRECTORY
                )

            elif "rising_dynamic_properties" in file_path:

                output_directory = os.path.join(
                    TableDirectories.GENERATED_TABLES_DIRECTORY,
                    TableDirectories
                    .RISING_DYNAMIC_PROPERTIES_SUBDIRECTORY
                )

            elif "falling_dynamic_properties" in file_path:

                output_directory = os.path.join(
                    TableDirectories.GENERATED_TABLES_DIRECTORY,
                    TableDirectories
                    .FALLING_DYNAMIC_PROPERTIES_SUBDIRECTORY
                )

            else:

                raise ValueError(
                    f"Cannot determine table type "
                    f"from path: {file_path}"
                )

            os.makedirs(
                output_directory,
                exist_ok=True
            )

            output_file_path = os.path.join(
                output_directory,
                file_name
            )

            df_export = df.copy()

            if (
                    PropertiesColumns.LOAD_RESISTANCE
                    in df_export.columns
            ):
                df_export[
                    PropertiesColumns.LOAD_RESISTANCE
                ] = (
                    df_export[
                        PropertiesColumns.LOAD_RESISTANCE
                    ]
                    .replace(
                        LatexLoadResistances.VALUES
                    )
                )

            if "variable" in df_export.columns:
                df_export["variable"] = (
                    df_export["variable"]
                    .replace(
                        LatexVariables.VARIABLES
                    )
                )

            df_export = df_export.rename(
                columns=LatexTableMappings.COLUMN_MAPPING
            )

            table_name = (
                file_name
                .replace(".tex", "")
            )

            caption = (
                LatexTableCaptions.CAPTIONS[
                    table_name
                ]
            )

            label = (
                f"tab:{table_name}"
            )

            latex_tabular = (
                df_export.to_latex(
                    index=False,
                    float_format="%.3f",
                    escape=False
                )
            )

            latex_content = (
                "\\begin{table*}[!t]\n"
                "\\centering\n"
                f"\\caption{{{caption}}}\n"
                f"\\label{{{label}}}\n"
                "\\small\n\n"
                f"{latex_tabular}\n"
                "\\end{table*}\n"
            )
            with open(
                    output_file_path,
                    "w",
                    encoding="utf-8"
            ) as file:

                file.write(
                    latex_content
                )

            print(
                f"Generated LaTeX table: "
                f"{output_file_path}"
            )