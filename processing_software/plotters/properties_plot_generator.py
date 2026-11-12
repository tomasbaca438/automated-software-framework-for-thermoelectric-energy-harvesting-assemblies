import os

import matplotlib.pyplot as plt
import pandas as pd

from configurations.dynamic_properties_plots import DYNAMIC_PROPERTIES_PLOTS
from configurations.static_properties_plots import STATIC_PROPERTIES_PLOTS
from constants.figures_directories import (
    FiguresDirectories
)

from constants.properties_columns import (
    PropertiesColumns
)

class PropertiesPlotGenerator:

    @staticmethod
    def resistance_to_numeric(
        resistance: str
    ) -> float:

        mapping = {
            "33K": 33000,
            "3K3": 3300,
            "330R": 330,
            "33R": 33,
            "3R3": 3.3
        }

        return mapping[resistance]

    @classmethod
    def plot_property_vs_load_resistance(
        cls,
        file_path: str,
        y_column: str,
        y_label: str
    ) -> None:

        df = pd.read_csv(
            file_path,
            sep=";"
        )

        df["load_resistance_numeric"] = (
            df[
                PropertiesColumns
                .LOAD_RESISTANCE
            ].map(
                cls.resistance_to_numeric
            )
        )

        df = df.sort_values(
            "load_resistance_numeric"
        )

        plt.figure()

        plt.semilogx(
            df[
                "load_resistance_numeric"
            ],
            df[
                y_column
            ],
            marker="o"
        )

        plt.grid(
            True,
            which="both"
        )

        plt.xlabel(
            "Load Resistance [$\\Omega$]"
        )

        plt.ylabel(
            y_label
        )

        plt.title(
            f"{y_label} vs Load Resistance"
        )

        os.makedirs(
            FiguresDirectories
            .GENERATED_PROPERTIES_PICTURES_DIRECTORY,
            exist_ok=True
        )

        base_name = os.path.splitext(
            os.path.basename(
                file_path
            )
        )[0]

        file_name = (
            f"{base_name}_{y_column}_vs_load_resistance"
        )

        for extension in (
            FiguresDirectories
            .GENERATED_PICTURES_EXTENSIONS
        ):

            plt.savefig(
                (
                    f"{FiguresDirectories.GENERATED_PROPERTIES_PICTURES_DIRECTORY}/"
                    f"{file_name}.{extension}"
                ),
                dpi=300,
                bbox_inches="tight"
            )

        plt.show()

    @classmethod
    def generate_all_static_property_plots(
        cls
    ) -> None:

        for config in (
            STATIC_PROPERTIES_PLOTS
        ):

            cls.plot_property_vs_load_resistance(
                file_path=
                    config["file_path"],

                y_column=
                    config["y_column"],

                y_label=
                    config["y_label"]
            )

    @classmethod
    def generate_all_dynamic_property_plots(
            cls
    ) -> None:

        for config in (
                DYNAMIC_PROPERTIES_PLOTS
        ):
            cls.plot_property_vs_load_resistance(
                file_path=
                config["file_path"],

                y_column=
                config["y_column"],

                y_label=
                config["y_label"]
            )