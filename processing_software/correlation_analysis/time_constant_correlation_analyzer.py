import os
import pandas as pd
from tabulate import tabulate

from constants.properties_columns import PropertiesColumns

class TimeConstantCorrelationAnalyzer:

    @classmethod
    def load_tau_data(
            cls,
            file_paths: list[str]
    ) -> pd.DataFrame:

        if len(file_paths) == 0:
            raise ValueError(
                "file_paths cannot be empty"
            )

        first_path = (
            os.path.basename(
                file_paths[0]
            )
        )

        if "rising" in first_path:

            tau_column = (
                PropertiesColumns
                .TAU_RISING_S
            )

            suffixes = [
                "_rising_dynamic_properties.csv",
                "_rising_nls_dynamic_properties.csv"
            ]

        elif "falling" in first_path:

            tau_column = (
                PropertiesColumns
                .TAU_FALLING_S
            )

            suffixes = [
                "_falling_dynamic_properties.csv",
                "_falling_nls_dynamic_properties.csv"
            ]

        else:

            raise ValueError(
                f"Cannot determine tau column "
                f"from path: {first_path}"
            )

        tau_data = None

        for file_path in file_paths:

            variable = (
                os.path.basename(
                    file_path
                )
            )

            for suffix in suffixes:
                variable = (
                    variable.replace(
                        suffix,
                        ""
                    )
                )

            df = pd.read_csv(
                file_path,
                sep=";"
            )

            current_df = (
                df[
                    [
                        PropertiesColumns
                        .LOAD_RESISTANCE,
                        tau_column
                    ]
                ]
                        .rename(
                    columns={
                        tau_column:
                            variable
                    }
                )
            )

            if tau_data is None:

                tau_data = current_df

            else:

                tau_data = tau_data.merge(
                    current_df,
                    on=PropertiesColumns
                    .LOAD_RESISTANCE
                )

        return tau_data

    @classmethod
    def calculate_correlation_matrix(
            cls,
            file_paths: list[str],
            output_file_path: str
    ) -> pd.DataFrame:

        df_tau = cls.load_tau_data(
            file_paths=file_paths
        )

        correlation_matrix = (
            df_tau.drop(
                columns=[
                    PropertiesColumns
                    .LOAD_RESISTANCE
                ]
            )
            .corr(
                method="pearson"
            )
        )

        print(
            "\nTime Constant Correlation Matrix"
        )

        os.makedirs(
            os.path.dirname(
                output_file_path
            ),
            exist_ok=True
        )

        correlation_matrix = (
            correlation_matrix
            .reset_index()
            .rename(
                columns={
                    "index":
                        PropertiesColumns.VARIABLE
                }
            )
        )

        correlation_matrix.to_csv(
            output_file_path,
            sep=";",
            index=False
        )

        print(
            f"Correlation matrix saved: "
            f"{output_file_path}"
        )

        return correlation_matrix