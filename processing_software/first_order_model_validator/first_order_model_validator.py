import numpy as np
import pandas as pd
from configurations.datasets import MERGED_FILE_PATHS
from constants.csv_columns import CSVColumns
from constants.generated_results import GeneratedResults, GeneratedResultsFilePaths
from constants.properties_columns import PropertiesColumns
import os

class FirstOrderModelValidator:

    @classmethod
    def load_static_properties(
            cls
    ) -> dict[str, pd.DataFrame]:

        static_properties = {}

        for path in GeneratedResultsFilePaths.STATIC_PROPERTIES_FILE_PATHS:

            variable = (
                path.split("/")[-1]
                .replace("_static_properties.csv", "")
            )

            static_properties[variable] = pd.read_csv(
                path,
                sep=";"
            )

        return static_properties

    @classmethod
    def generate_theoretical_responses(
            cls,
            measurement_duration_s: int = 900,
            use_nls: bool = False,
    ) -> dict[str, pd.DataFrame]:

        theoretical_responses = {}

        static_properties = cls.load_static_properties()

        variables = (
            GeneratedResults
            .VARIABLES_GENERATED_RESULTS
        )

        samples = np.arange(
            measurement_duration_s + 1
        )

        for variable in variables:

            if use_nls:

                rising_path = (
                    f"{GeneratedResults.NLS_DYNAMIC_PROPERTIES_DIRECTORY}/"
                    f"{variable}_rising_nls_dynamic_properties.csv"
                )

                falling_path = (
                    f"{GeneratedResults.NLS_DYNAMIC_PROPERTIES_DIRECTORY}/"
                    f"{variable}_falling_nls_dynamic_properties.csv"
                )

            else:

                rising_path = (
                    f"{GeneratedResults.DYNAMIC_PROPERTIES_DIRECTORY}/"
                    f"{variable}_rising_dynamic_properties.csv"
                )

                falling_path = (
                    f"{GeneratedResults.DYNAMIC_PROPERTIES_DIRECTORY}/"
                    f"{variable}_falling_dynamic_properties.csv"
                )

            rising_df = pd.read_csv(
                rising_path,
                sep=";"
            )

            falling_df = pd.read_csv(
                falling_path,
                sep=";"
            )

            static_df = static_properties[
                variable
            ]

            variable_df = pd.DataFrame()

            variable_df[
                CSVColumns.SAMPLE_COLUMN
            ] = samples

            for row_idx in range(
                    len(rising_df)
            ):
                load_label = rising_df.iloc[
                    row_idx,
                    0
                ]

                tau_r = rising_df.loc[
                    row_idx,
                    PropertiesColumns.TAU_RISING_S
                ]

                tau_f = falling_df.loc[
                    row_idx,
                    PropertiesColumns.TAU_FALLING_S
                ]

                static_row = static_df[
                    static_df[
                        PropertiesColumns.LOAD_RESISTANCE
                    ] == load_label
                    ].iloc[0]

                initial_value = static_row[
                    PropertiesColumns.INITIAL_VALUE
                ]

                rise_ss = static_row[
                    PropertiesColumns.RISING_STEADY_STATE_VALUE
                ]

                fall_ss = static_row[
                    PropertiesColumns.FALLING_STEADY_STATE_VALUE
                ]

                rising_response = (
                        rise_ss
                        - (
                                rise_ss
                                - initial_value
                        )
                        * np.exp(
                    -samples
                    / tau_r
                )
                )

                falling_response = (
                        fall_ss
                        + (
                                rise_ss
                                - fall_ss
                        )
                        * np.exp(
                    -samples
                    / tau_f
                )
                )

                label_mapping = {
                    "33KΩ": "33K",
                    "3.3KΩ": "3K3",
                    "330Ω": "330R",
                    "33Ω": "33R",
                    "3.3Ω": "3R3"
                }

                load_label = label_mapping.get(
                    load_label,
                    load_label
                )

                variable_df[
                    f"{load_label}_rising"
                ] = rising_response

                variable_df[
                    f"{load_label}_falling"
                ] = falling_response

            theoretical_responses[
                variable
            ] = variable_df

        return theoretical_responses

    @classmethod
    def load_dynamic_responses(
            cls,
            switch_sample: int = 900
    ) -> dict[str, pd.DataFrame]:

        variables = (
            GeneratedResults
            .VARIABLES_GENERATED_RESULTS
        )

        responses = {}

        for variable in variables:

            variable_df = pd.DataFrame()

            variable_df[
                CSVColumns.SAMPLE_COLUMN
            ] = np.arange(
                switch_sample + 1
            )

            for path in MERGED_FILE_PATHS:
                label = (
                    path.split("/")[-1]
                    .replace("_merged.csv", "")
                )

                df = pd.read_csv(
                    path,
                    sep=";"
                )

                response = df[
                    variable
                ].values

                rising_response = response[
                    0: switch_sample + 1
                ]

                falling_response = response[
                    switch_sample:
                    switch_sample * 2 + 1
                ]

                # if falling response is longer
                falling_response = falling_response[
                    :switch_sample + 1
                ]

                variable_df[
                    f"{label}_rising"
                ] = rising_response

                variable_df[
                    f"{label}_falling"
                ] = falling_response

            responses[
                variable
            ] = variable_df

        return responses

    @staticmethod
    def calculate_metrics(
            measured: np.ndarray,
            theoretical: np.ndarray
    ) -> dict[str, float]:

        residuals = (
                measured
                - theoretical
        )

        rmse = np.sqrt(
            np.mean(
                residuals ** 2
            )
        )

        mae = np.mean(
            np.abs(
                residuals
            )
        )

        ss_res = np.sum(
            residuals ** 2
        )

        ss_tot = np.sum(
            (
                    measured
                    - np.mean(
                measured
            )
            ) ** 2
        )

        r2 = (
            1
            - ss_res / ss_tot
            if ss_tot > 0
            else 1.0
        )

        return {
            PropertiesColumns.RMSE:
                rmse,

            PropertiesColumns.MAE:
                mae,

            PropertiesColumns.R2:
                r2
        }

    @classmethod
    def calculate_validation_properties(
            cls,
            switch_sample: int = 900,
            measurement_duration_s: int = 900
    ) -> dict[str, dict[str, dict[str, float]]]:

        measured_responses = (
            cls.load_dynamic_responses(
                switch_sample=switch_sample
            )
        )

        theoretical_responses_original = (
            cls.generate_theoretical_responses(
                measurement_duration_s=
                measurement_duration_s,
                use_nls=False
            )
        )

        theoretical_responses_nls = (
            cls.generate_theoretical_responses(
                measurement_duration_s=
                measurement_duration_s,
                use_nls=True
            )
        )

        validation_results = {}

        for variable in theoretical_responses_original:

            validation_results[
                variable
            ] = {}

            measured_df = (
                measured_responses[
                    variable
                ]
            )

            theoretical_original_df = (
                theoretical_responses_original[
                    variable
                ]
            )

            theoretical_nls_df = (
                theoretical_responses_nls[
                    variable
                ]
            )

            for column in measured_df.columns:

                if (
                        column
                        ==
                        CSVColumns.SAMPLE_COLUMN
                ):
                    continue

                measured = (
                    measured_df[
                        column
                    ]
                    .to_numpy()
                )

                theoretical_original = (
                    theoretical_original_df[
                        column
                    ]
                    .to_numpy()
                )

                theoretical_nls = (
                    theoretical_nls_df[
                        column
                    ]
                    .to_numpy()
                )

                metrics_original = (
                    cls.calculate_metrics(
                        measured=
                        measured,

                        theoretical=
                        theoretical_original
                    )
                )

                metrics_nls = (
                    cls.calculate_metrics(
                        measured=
                        measured,

                        theoretical=
                        theoretical_nls
                    )
                )

                validation_results[
                    variable
                ][
                    column
                ] = {

                    PropertiesColumns.RMSE_ORIGINAL:
                        metrics_original[
                            PropertiesColumns.RMSE
                        ],

                    PropertiesColumns.MAE_ORIGINAL:
                        metrics_original[
                            PropertiesColumns.MAE
                        ],

                    PropertiesColumns.R2_ORIGINAL:
                        metrics_original[
                            PropertiesColumns.R2
                        ],

                    PropertiesColumns.RMSE_NLS:
                        metrics_nls[
                            PropertiesColumns.RMSE
                        ],

                    PropertiesColumns.MAE_NLS:
                        metrics_nls[
                            PropertiesColumns.MAE
                        ],

                    PropertiesColumns.R2_NLS:
                        metrics_nls[
                            PropertiesColumns.R2
                        ]
                }

        return validation_results

    @classmethod
    def save_validation_properties(
            cls,
            validation_results: dict[
                str,
                dict[
                    str,
                    dict[str, float]
                ]
            ]
    ) -> None:

        os.makedirs(
            GeneratedResults
            .FIRST_ORDER_VALIDATION_DIRECTORY,
            exist_ok=True
        )

        for variable in validation_results:

            rising_rows = []
            falling_rows = []

            for response_name in (
                    validation_results[
                        variable
                    ]
            ):

                result = (
                    validation_results[
                        variable
                    ][
                        response_name
                    ]
                )

                load_resistance = (
                    response_name
                    .replace("_rising", "")
                    .replace("_falling", "")
                )

                load_resistance_mapping = {
                    "33K": "33KΩ",
                    "3K3": "3.3KΩ",
                    "330R": "330Ω",
                    "33R": "33Ω",
                    "3R3": "3.3Ω"
                }

                load_resistance = (
                    load_resistance_mapping.get(
                        load_resistance,
                        load_resistance
                    )
                )

                row = {

                    PropertiesColumns.LOAD_RESISTANCE:
                        load_resistance,

                    PropertiesColumns.RMSE_ORIGINAL:
                        result[
                            PropertiesColumns
                            .RMSE_ORIGINAL
                        ],

                    PropertiesColumns.MAE_ORIGINAL:
                        result[
                            PropertiesColumns
                            .MAE_ORIGINAL
                        ],

                    PropertiesColumns.R2_ORIGINAL:
                        result[
                            PropertiesColumns
                            .R2_ORIGINAL
                        ],

                    PropertiesColumns.RMSE_NLS:
                        result[
                            PropertiesColumns
                            .RMSE_NLS
                        ],

                    PropertiesColumns.MAE_NLS:
                        result[
                            PropertiesColumns
                            .MAE_NLS
                        ],

                    PropertiesColumns.R2_NLS:
                        result[
                            PropertiesColumns
                            .R2_NLS
                        ]
                }

                if response_name.endswith(
                        "_rising"
                ):

                    rising_rows.append(
                        row
                    )

                elif response_name.endswith(
                        "_falling"
                ):

                    falling_rows.append(
                        row
                    )

            rising_df = pd.DataFrame(
                rising_rows
            )

            falling_df = pd.DataFrame(
                falling_rows
            )

            rising_path = (
                f"{GeneratedResults.FIRST_ORDER_VALIDATION_DIRECTORY}/"
                f"{variable}_rising_first_order_validation.csv"
            )

            falling_path = (
                f"{GeneratedResults.FIRST_ORDER_VALIDATION_DIRECTORY}/"
                f"{variable}_falling_first_order_validation.csv"
            )

            rising_df.to_csv(
                rising_path,
                sep=";",
                index=False
            )

            falling_df.to_csv(
                falling_path,
                sep=";",
                index=False
            )

            print(
                f"Validation saved: "
                f"{rising_path}"
            )

            print(
                f"Validation saved: "
                f"{falling_path}"
            )

    @classmethod
    def run_validation(cls) -> None:

        validation_results = (
            cls.calculate_validation_properties()
        )

        cls.save_validation_properties(
            validation_results
        )

        for variable in validation_results:

            for response_name in (
                    validation_results[
                        variable
                    ]
            ):
                result = (
                    validation_results[
                        variable
                    ][
                        response_name
                    ]
                )