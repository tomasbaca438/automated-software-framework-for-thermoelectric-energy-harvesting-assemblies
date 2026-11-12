import numpy as np
import pandas as pd

from constants.csv_columns import CSVColumns
from constants.properties_columns import (
    PropertiesColumns
)
from constants.generated_results import (
    GeneratedResults
)
import os


class DynamicPropertiesAnalyzer:

    @staticmethod
    def calculate_rising_target(
            initial_value: float,
            steady_state: float
    ) -> float:

        return (
            initial_value
            + 0.632121
            * (steady_state - initial_value)
        )

    @staticmethod
    def calculate_falling_target(
            steady_high: float,
            steady_low: float
    ) -> float:

        return (
            steady_low
            + 0.367879
            * (steady_high - steady_low)
        )

    @staticmethod
    def extract_rising_tau(
            df: pd.DataFrame,
            csv_column: str,
            switch_sample: int,
            target_rising: float
    ) -> int | None:

        rising_samples = df[
            (df[CSVColumns.SAMPLE_COLUMN] < switch_sample)
            & (df[csv_column] >= target_rising)
        ]

        if rising_samples.empty:
            return None

        return int(
            rising_samples[
                CSVColumns.SAMPLE_COLUMN
            ].iloc[0]
        )

    @staticmethod
    def extract_falling_tau(
            df: pd.DataFrame,
            csv_column: str,
            switch_sample: int,
            target_falling: float
    ) -> int | None:

        falling_samples = df[
            (df[CSVColumns.SAMPLE_COLUMN] >= switch_sample)
            & (df[csv_column] <= target_falling)
        ]

        if falling_samples.empty:
            return None

        return int(
            falling_samples[
                CSVColumns.SAMPLE_COLUMN
            ].iloc[0]
            - switch_sample
        )

    @staticmethod
    def calculate_settling_time(
            tau: float
    ) -> float:

        return 5.0 * tau

    @staticmethod
    def calculate_cutoff_frequency(
            tau: float
    ) -> float:

        return (
            1.0
            / (2.0 * np.pi * tau)
        )

    @classmethod
    def calculate_all_dynamic_properties(
            cls,
            df_measurement: pd.DataFrame,
            variable: str,
            static_row: pd.Series,
            switch_sample: int,
            sampling_period_s: float
    ) -> pd.DataFrame:

        initial_value = static_row[
            PropertiesColumns.INITIAL_VALUE
        ]

        steady_high = static_row[
            PropertiesColumns.RISING_STEADY_STATE_VALUE
        ]

        steady_low = static_row[
            PropertiesColumns.FALLING_STEADY_STATE_VALUE
        ]

        target_rising = (
            cls.calculate_rising_target(
                initial_value=initial_value,
                steady_state=steady_high
            )
        )

        target_falling = (
            cls.calculate_falling_target(
                steady_high=steady_high,
                steady_low=steady_low
            )
        )

        tau_rising_samples = (
            cls.extract_rising_tau(
                df=df_measurement,
                csv_column=variable,
                switch_sample=switch_sample,
                target_rising=target_rising
            )
        )

        tau_falling_samples = (
            cls.extract_falling_tau(
                df=df_measurement,
                csv_column=variable,
                switch_sample=switch_sample,
                target_falling=target_falling
            )
        )

        tau_rising_s = (
            tau_rising_samples
            * sampling_period_s
            if tau_rising_samples is not None
            else np.nan
        )

        tau_falling_s = (
            tau_falling_samples
            * sampling_period_s
            if tau_falling_samples is not None
            else np.nan
        )

        settling_time_rising_s = (
            cls.calculate_settling_time(
                tau_rising_s
            )
            if not pd.isna(tau_rising_s)
            else np.nan
        )

        settling_time_falling_s = (
            cls.calculate_settling_time(
                tau_falling_s
            )
            if not pd.isna(tau_falling_s)
            else np.nan
        )

        cutoff_frequency_rising_hz = (
            cls.calculate_cutoff_frequency(
                tau_rising_s
            )
            if (
                    not pd.isna(tau_rising_s)
                    and tau_rising_s > 0
            )
            else np.nan
        )

        cutoff_frequency_falling_hz = (
            cls.calculate_cutoff_frequency(
                tau_falling_s
            )
            if (
                    not pd.isna(tau_falling_s)
                    and tau_falling_s > 0
            )
            else np.nan
        )

        cutoff_period_rising_s = (
            1.0 / cutoff_frequency_rising_hz
            if (
                    not pd.isna(
                        cutoff_frequency_rising_hz
                    )
                    and cutoff_frequency_rising_hz > 0
            )
            else np.nan
        )

        cutoff_period_falling_s = (
            1.0 / cutoff_frequency_falling_hz
            if (
                    not pd.isna(
                        cutoff_frequency_falling_hz
                    )
                    and cutoff_frequency_falling_hz > 0
            )
            else np.nan
        )

        cutoff_period_rising_min = (
            cutoff_period_rising_s / 60.0
            if not pd.isna(
                cutoff_period_rising_s
            )
            else np.nan
        )

        cutoff_period_falling_min = (
            cutoff_period_falling_s / 60.0
            if not pd.isna(
                cutoff_period_falling_s
            )
            else np.nan
        )

        return pd.DataFrame(
            [
                {
                    PropertiesColumns.VARIABLE:
                        variable,

                    PropertiesColumns.TAU_RISING_SAMPLES:
                        tau_rising_samples,

                    PropertiesColumns.TAU_RISING_S:
                        tau_rising_s,

                    PropertiesColumns.TAU_FALLING_SAMPLES:
                        tau_falling_samples,

                    PropertiesColumns.TAU_FALLING_S:
                        tau_falling_s,

                    PropertiesColumns.SETTLING_TIME_RISING_S:
                        settling_time_rising_s,

                    PropertiesColumns.SETTLING_TIME_FALLING_S:
                        settling_time_falling_s,

                    PropertiesColumns.CUTOFF_FREQUENCY_RISING_HZ:
                        cutoff_frequency_rising_hz,

                    PropertiesColumns.CUTOFF_FREQUENCY_FALLING_HZ:
                        cutoff_frequency_falling_hz,

                    PropertiesColumns.CUTOFF_PERIOD_RISING_S:
                        cutoff_period_rising_s,

                    PropertiesColumns.CUTOFF_PERIOD_FALLING_S:
                        cutoff_period_falling_s,

                    PropertiesColumns.CUTOFF_PERIOD_RISING_MIN:
                        cutoff_period_rising_min,

                    PropertiesColumns.CUTOFF_PERIOD_FALLING_MIN:
                        cutoff_period_falling_min
                }
            ]
        )

    @classmethod
    def generate_dynamic_properties_csvs(
            cls,
            merged_file_paths: list[str],
            labels: list[str],
            switch_sample: int = 900,
            sampling_period_s: float = 1.0
    ) -> None:

        os.makedirs(
            GeneratedResults.DYNAMIC_PROPERTIES_DIRECTORY,
            exist_ok=True
        )

        rising_results = {
            variable: []
            for variable in GeneratedResults.VARIABLES_DYNAMIC
        }

        falling_results = {
            variable: []
            for variable in GeneratedResults.VARIABLES_DYNAMIC
        }

        for (
                merged_file_path,
                label
        ) in zip(
            merged_file_paths,
            labels
        ):

            df_measurement = pd.read_csv(
                merged_file_path,
                sep=";"
            )

            for variable in GeneratedResults.VARIABLES_DYNAMIC:
                static_file_path = (
                    f"{GeneratedResults.STATIC_PROPERTIES_DIRECTORY}/"
                    f"{variable}_static_properties.csv"
                )

                df_static = pd.read_csv(
                    static_file_path,
                    sep=";"
                )

                static_row = df_static[
                    df_static[
                        PropertiesColumns.LOAD_RESISTANCE
                    ] == label
                    ].iloc[0]

                df_dynamic = (
                    cls.calculate_all_dynamic_properties(
                        df_measurement=df_measurement,
                        variable=variable,
                        static_row=static_row,
                        switch_sample=switch_sample,
                        sampling_period_s=sampling_period_s
                    )
                )

                row = df_dynamic.iloc[0]

                rising_results[
                    variable
                ].append(
                    {
                        PropertiesColumns.LOAD_RESISTANCE:
                            label,

                        PropertiesColumns.TAU_RISING_SAMPLES:
                            row[
                                PropertiesColumns
                                .TAU_RISING_SAMPLES
                            ],

                        PropertiesColumns.TAU_RISING_S:
                            row[
                                PropertiesColumns
                                .TAU_RISING_S
                            ],

                        PropertiesColumns.SETTLING_TIME_RISING_S:
                            row[
                                PropertiesColumns
                                .SETTLING_TIME_RISING_S
                            ],

                        PropertiesColumns.CUTOFF_FREQUENCY_RISING_HZ:
                            row[
                                PropertiesColumns
                                .CUTOFF_FREQUENCY_RISING_HZ
                            ],

                        PropertiesColumns.CUTOFF_PERIOD_RISING_S:
                            row[
                                PropertiesColumns
                                .CUTOFF_PERIOD_RISING_S
                            ],

                        PropertiesColumns.CUTOFF_PERIOD_RISING_MIN:
                            row[
                                PropertiesColumns
                                .CUTOFF_PERIOD_RISING_MIN
                            ]
                    }
                )

                falling_results[
                    variable
                ].append(
                    {
                        PropertiesColumns.LOAD_RESISTANCE:
                            label,

                        PropertiesColumns.TAU_FALLING_SAMPLES:
                            row[
                                PropertiesColumns
                                .TAU_FALLING_SAMPLES
                            ],

                        PropertiesColumns.TAU_FALLING_S:
                            row[
                                PropertiesColumns
                                .TAU_FALLING_S
                            ],

                        PropertiesColumns.SETTLING_TIME_FALLING_S:
                            row[
                                PropertiesColumns
                                .SETTLING_TIME_FALLING_S
                            ],

                        PropertiesColumns.CUTOFF_FREQUENCY_FALLING_HZ:
                            row[
                                PropertiesColumns
                                .CUTOFF_FREQUENCY_FALLING_HZ
                            ],

                        PropertiesColumns.CUTOFF_PERIOD_FALLING_S:
                            row[
                                PropertiesColumns
                                .CUTOFF_PERIOD_FALLING_S
                            ],

                        PropertiesColumns.CUTOFF_PERIOD_FALLING_MIN:
                            row[
                                PropertiesColumns
                                .CUTOFF_PERIOD_FALLING_MIN
                            ]
                    }
                )

        for variable in GeneratedResults.VARIABLES_DYNAMIC:
            pd.DataFrame(
                rising_results[variable]
            ).to_csv(
                (
                    f"{GeneratedResults.DYNAMIC_PROPERTIES_DIRECTORY}/"
                    f"{variable}_rising_dynamic_properties.csv"
                ),
                sep=";",
                index=False
            )

            pd.DataFrame(
                falling_results[variable]
            ).to_csv(
                (
                    f"{GeneratedResults.DYNAMIC_PROPERTIES_DIRECTORY}/"
                    f"{variable}_falling_dynamic_properties.csv"
                ),
                sep=";",
                index=False
            )

            print(
                f"Dynamic properties saved for "
                f"{variable}"
            )