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

from scipy.optimize import curve_fit

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
    def estimate_rising_tau_nls(
            time: np.ndarray,
            measured: np.ndarray,
            initial_value: float,
            rising_steady_state_value: float,
            tau_initial_guess: float
    ) -> tuple[float, np.ndarray] | None:

        def model(
                time: np.ndarray,
                tau: float
        ) -> np.ndarray:

            return (
                    rising_steady_state_value
                    - (
                            rising_steady_state_value
                            - initial_value
                    )
                    * np.exp(
                -time / tau
            )
            )

        try:

            popt, pcov = curve_fit(
                model,
                time,
                measured,
                p0=[tau_initial_guess]
            )

            return (
                float(popt[0]),
                pcov
            )

        except Exception:

            return None

    @staticmethod
    def estimate_falling_tau_nls(
            time: np.ndarray,
            measured: np.ndarray,
            rising_steady_state_value: float,
            falling_steady_state_value: float,
            tau_initial_guess: float
    ) -> tuple[float, np.ndarray] | None:

        def model(
                time: np.ndarray,
                tau: float
        ) -> np.ndarray:

            return (
                    falling_steady_state_value
                    + (
                            rising_steady_state_value
                            - falling_steady_state_value
                    )
                    * np.exp(
                -time / tau
            )
            )

        try:

            popt, pcov = curve_fit(
                model,
                time,
                measured,
                p0=[tau_initial_guess]
            )

            return (
                float(popt[0]),
                pcov
            )

        except Exception:

            return None

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

    @staticmethod
    def calculate_number_of_tau(
            measurement_time_s: float,
            tau_s: float
    ) -> float:

        if (
                pd.isna(tau_s)
                or tau_s <= 0
        ):
            return np.nan

        return (
                measurement_time_s
                / tau_s
        )

    @classmethod
    def calculate_dynamic_properties_from_tau(
            cls,
            tau_s: float
    ) -> dict:

        settling_time_s = (
            cls.calculate_settling_time(
                tau_s
            )
            if not pd.isna(
                tau_s
            )
            else np.nan
        )

        cutoff_frequency_hz = (
            cls.calculate_cutoff_frequency(
                tau_s
            ) * 1000.0
            if (
                    not pd.isna(
                        tau_s
                    )
                    and tau_s > 0
            )
            else np.nan
        )

        cutoff_period_s = (
            1.0
            / cutoff_frequency_hz
            if (
                    not pd.isna(
                        cutoff_frequency_hz
                    )
                    and cutoff_frequency_hz > 0
            )
            else np.nan
        )

        cutoff_period_min = (
            cutoff_period_s
            / 60.0
            if not pd.isna(
                cutoff_period_s
            )
            else np.nan
        )

        return {

            PropertiesColumns.DYNAMIC_SETTLING_TIME:
                settling_time_s,

            PropertiesColumns.DYNAMIC_CUTOFF_FREQUENCY:
                cutoff_frequency_hz,

            PropertiesColumns.DYNAMIC_CUTOFF_PERIOD_S:
                cutoff_period_s,

            PropertiesColumns.DYNAMIC_CUTOFF_PERIOD_MIN:
                cutoff_period_min
        }

    @classmethod
    def calculate_all_dynamic_properties(
            cls,
            df_measurement: pd.DataFrame,
            variable: str,
            static_row: pd.Series,
            switch_sample: int,
            sampling_period_s: float,
            use_nls: bool = False
    ) -> pd.DataFrame:

        measurement_time_rising_s = (
                switch_sample
                * sampling_period_s
        )

        measurement_time_falling_s = (
                (
                        len(df_measurement)
                        - switch_sample
                )
                * sampling_period_s
        )

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

        if use_nls:

            rising_df = (
                df_measurement[
                    df_measurement[
                        CSVColumns.SAMPLE_COLUMN
                    ] <= switch_sample
                    ]
            )

            falling_df = (
                df_measurement[
                    df_measurement[
                        CSVColumns.SAMPLE_COLUMN
                    ] >= switch_sample
                    ]
                .copy()
            )

            falling_df[
                CSVColumns.SAMPLE_COLUMN
            ] = (
                    falling_df[
                        CSVColumns.SAMPLE_COLUMN
                    ]
                    - switch_sample
            )

            if not pd.isna(
                    tau_rising_s
            ):

                rising_result = (
                    cls.estimate_rising_tau_nls(
                        time=rising_df[
                            CSVColumns.SAMPLE_COLUMN
                        ].to_numpy(),
                        measured=rising_df[
                            variable
                        ].to_numpy(),
                        initial_value=initial_value,
                        rising_steady_state_value=steady_high,
                        tau_initial_guess=tau_rising_s
                    )
                )

                if rising_result is not None:
                    tau_rising_s, _ = (
                        rising_result
                    )

            if not pd.isna(
                    tau_falling_s
            ):

                falling_result = (
                    cls.estimate_falling_tau_nls(
                        time=falling_df[
                            CSVColumns.SAMPLE_COLUMN
                        ].to_numpy(),
                        measured=falling_df[
                            variable
                        ].to_numpy(),
                        rising_steady_state_value=steady_high,
                        falling_steady_state_value=steady_low,
                        tau_initial_guess=tau_falling_s
                    )
                )

                if falling_result is not None:
                    tau_falling_s, _ = (
                        falling_result
                    )

        rising_properties = (
            cls.calculate_dynamic_properties_from_tau(
                tau_rising_s
            )
        )

        falling_properties = (
            cls.calculate_dynamic_properties_from_tau(
                tau_falling_s
            )
        )

        number_of_tau_rising = (
            cls.calculate_number_of_tau(
                measurement_time_s=
                measurement_time_rising_s,

                tau_s=
                tau_rising_s
            )
        )

        number_of_tau_falling = (
            cls.calculate_number_of_tau(
                measurement_time_s=
                measurement_time_falling_s,

                tau_s=
                tau_falling_s
            )
        )

        return pd.DataFrame(
            [
                {
                    PropertiesColumns.VARIABLE:
                        variable,

                    PropertiesColumns.TAU_RISING_S:
                        tau_rising_s,

                    PropertiesColumns.TAU_FALLING_S:
                        tau_falling_s,

                    PropertiesColumns.NUMBER_OF_TAU_RISING:
                        number_of_tau_rising,

                    PropertiesColumns.NUMBER_OF_TAU_FALLING:
                        number_of_tau_falling,

                    PropertiesColumns.SETTLING_TIME_RISING_S:
                        rising_properties[
                            PropertiesColumns
                            .DYNAMIC_SETTLING_TIME
                        ],

                    PropertiesColumns.SETTLING_TIME_FALLING_S:
                        falling_properties[
                            PropertiesColumns
                            .DYNAMIC_SETTLING_TIME
                        ],

                    PropertiesColumns.CUTOFF_FREQUENCY_RISING_HZ:
                        rising_properties[
                            PropertiesColumns
                            .DYNAMIC_CUTOFF_FREQUENCY
                        ],

                    PropertiesColumns.CUTOFF_FREQUENCY_FALLING_HZ:
                        falling_properties[
                            PropertiesColumns
                            .DYNAMIC_CUTOFF_FREQUENCY
                        ],

                    PropertiesColumns.CUTOFF_PERIOD_RISING_S:
                        rising_properties[
                            PropertiesColumns
                            .DYNAMIC_CUTOFF_PERIOD_S
                        ],

                    PropertiesColumns.CUTOFF_PERIOD_FALLING_S:
                        falling_properties[
                            PropertiesColumns
                            .DYNAMIC_CUTOFF_PERIOD_S
                        ],

                    PropertiesColumns.CUTOFF_PERIOD_RISING_MIN:
                        rising_properties[
                            PropertiesColumns
                            .DYNAMIC_CUTOFF_PERIOD_MIN
                        ],

                    PropertiesColumns.CUTOFF_PERIOD_FALLING_MIN:
                        falling_properties[
                            PropertiesColumns
                            .DYNAMIC_CUTOFF_PERIOD_MIN
                        ]
                }
            ]
        )

    @staticmethod
    def create_rising_result_row(
            label: str,
            row: pd.Series
    ) -> dict:

        return {

            PropertiesColumns.LOAD_RESISTANCE:
                label,

            PropertiesColumns.TAU_RISING_S:
                row[
                    PropertiesColumns
                    .TAU_RISING_S
                ],

            PropertiesColumns.NUMBER_OF_TAU_RISING:
                row[
                    PropertiesColumns
                    .NUMBER_OF_TAU_RISING
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

    @staticmethod
    def create_falling_result_row(
            label: str,
            row: pd.Series
    ) -> dict:

        return {

            PropertiesColumns.LOAD_RESISTANCE:
                label,

            PropertiesColumns.TAU_FALLING_S:
                row[
                    PropertiesColumns
                    .TAU_FALLING_S
                ],

            PropertiesColumns.NUMBER_OF_TAU_FALLING:
                row[
                    PropertiesColumns
                    .NUMBER_OF_TAU_FALLING
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
            for variable in GeneratedResults.VARIABLES_GENERATED_RESULTS
        }

        falling_results = {
            variable: []
            for variable in GeneratedResults.VARIABLES_GENERATED_RESULTS
        }

        for merged_file_path, label in zip(
                merged_file_paths,
                labels
        ):

            df_measurement = pd.read_csv(
                merged_file_path,
                sep=";"
            )

            for variable in (
                    GeneratedResults.VARIABLES_GENERATED_RESULTS
            ):
                static_file_path = (
                    f"{GeneratedResults.STATIC_PROPERTIES_DIRECTORY}/"
                    f"{variable}_static_properties.csv"
                )

                df_static = pd.read_csv(
                    static_file_path,
                    sep=";"
                )

                static_row = (
                    df_static[
                        df_static[
                            PropertiesColumns.LOAD_RESISTANCE
                        ] == label
                        ]
                    .iloc[0]
                )

                df_dynamic = (
                    cls.calculate_all_dynamic_properties(
                        df_measurement=df_measurement,
                        variable=variable,
                        static_row=static_row,
                        switch_sample=switch_sample,
                        sampling_period_s=sampling_period_s,
                        use_nls=False
                    )
                )

                row = df_dynamic.iloc[0]

                rising_results[
                    variable
                ].append(
                    cls.create_rising_result_row(
                        label=label,
                        row=row
                    )
                )

                falling_results[
                    variable
                ].append(
                    cls.create_falling_result_row(
                        label=label,
                        row=row
                    )
                )

        for variable in (
                GeneratedResults
                        .VARIABLES_GENERATED_RESULTS
        ):
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

    @classmethod
    def generate_nls_dynamic_properties_csvs(
            cls,
            merged_file_paths: list[str],
            labels: list[str],
            switch_sample: int = 900,
            sampling_period_s: float = 1.0
    ) -> None:

        os.makedirs(
            GeneratedResults
            .NLS_DYNAMIC_PROPERTIES_DIRECTORY,
            exist_ok=True
        )

        rising_results = {
            variable: []
            for variable in
            GeneratedResults
            .VARIABLES_GENERATED_RESULTS
        }

        falling_results = {
            variable: []
            for variable in
            GeneratedResults
            .VARIABLES_GENERATED_RESULTS
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

            for variable in (
                    GeneratedResults
                            .VARIABLES_GENERATED_RESULTS
            ):
                static_file_path = (
                    f"{GeneratedResults.STATIC_PROPERTIES_DIRECTORY}/"
                    f"{variable}_static_properties.csv"
                )

                df_static = pd.read_csv(
                    static_file_path,
                    sep=";"
                )

                static_row = (
                    df_static[
                        df_static[
                            PropertiesColumns
                            .LOAD_RESISTANCE
                        ] == label
                        ]
                            .iloc[0]
                )

                df_dynamic = (
                    cls.calculate_all_dynamic_properties(
                        df_measurement=df_measurement,
                        variable=variable,
                        static_row=static_row,
                        switch_sample=switch_sample,
                        sampling_period_s=sampling_period_s,
                        use_nls=True
                    )
                )

                row = df_dynamic.iloc[0]

                rising_results[
                    variable
                ].append(
                    cls.create_rising_result_row(
                        label=label,
                        row=row
                    )
                )

                falling_results[
                    variable
                ].append(
                    cls.create_falling_result_row(
                        label=label,
                        row=row
                    )
                )

        for variable in (
                GeneratedResults
                        .VARIABLES_GENERATED_RESULTS
        ):
            pd.DataFrame(
                rising_results[
                    variable
                ]
            ).to_csv(
                (
                    f"{GeneratedResults.NLS_DYNAMIC_PROPERTIES_DIRECTORY}/"
                    f"{variable}_rising_nls_dynamic_properties.csv"
                ),
                sep=";",
                index=False
            )

            pd.DataFrame(
                falling_results[
                    variable
                ]
            ).to_csv(
                (
                    f"{GeneratedResults.NLS_DYNAMIC_PROPERTIES_DIRECTORY}/"
                    f"{variable}_falling_nls_dynamic_properties.csv"
                ),
                sep=";",
                index=False
            )

            print(
                f"NLS dynamic properties saved for "
                f"{variable}"
            )