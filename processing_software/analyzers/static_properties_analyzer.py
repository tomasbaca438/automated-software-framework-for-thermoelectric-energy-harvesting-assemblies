import os

import pandas as pd

from constants.properties_columns import (
    PropertiesColumns
)

from constants.generated_results import (
    GeneratedResults
)


class StaticPropertiesAnalyzer:

    @staticmethod
    def calculate_steady_state(
        data: pd.Series,
        switch_sample: int
    ) -> tuple[float, float, float]:

        initial_value = (
            data.iloc[:10]
            .mean()
        )

        steady_high = (
            data.iloc[:switch_sample]
            .tail(100)
            .mean()
        )

        steady_low = (
            data.iloc[switch_sample:]
            .tail(100)
            .mean()
        )

        return (
            initial_value,
            steady_high,
            steady_low
        )

    @classmethod
    def generate_static_properties_csvs(
        cls,
        merged_file_paths: list[str],
        labels: list[str],
        output_directory: str,
        switch_sample: int = 900
    ) -> None:

        results = {
            variable: []
            for variable in GeneratedResults.VARIABLES_GENERATED_RESULTS
        }

        for merged_file_path, label in zip(
            merged_file_paths,
            labels
        ):

            df = pd.read_csv(
                merged_file_path,
                sep=";"
            )

            for variable in GeneratedResults.VARIABLES_GENERATED_RESULTS:

                (
                    initial_value,
                    steady_high,
                    steady_low
                ) = cls.calculate_steady_state(
                    data=df[variable],
                    switch_sample=switch_sample
                )

                results[
                    variable
                ].append(
                    {
                        PropertiesColumns
                        .LOAD_RESISTANCE:
                            label,

                        PropertiesColumns
                        .INITIAL_VALUE:
                            initial_value,

                        PropertiesColumns
                        .RISING_STEADY_STATE_VALUE:
                            steady_high,

                        PropertiesColumns
                        .FALLING_STEADY_STATE_VALUE:
                            steady_low
                    }
                )

        os.makedirs(
            output_directory,
            exist_ok=True
        )

        for variable, rows in results.items():

            output_file_path = os.path.join(
                GeneratedResults.STATIC_PROPERTIES_DIRECTORY,
                f"{variable}_static_properties.csv"
            )

            pd.DataFrame(rows).to_csv(
                output_file_path,
                sep=";",
                index=False
            )

            print(
                f"Static properties saved: "
                f"{output_file_path}"
            )