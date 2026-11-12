import os
import pandas as pd
import matplotlib.pyplot as plt
from constants.plot_types import PlotTypes
from constants.figures_directories import FiguresDirectories


class StepResponseAnalyzer:
    @staticmethod
    def plot_step_response(
            file_paths: list[str],
            labels: list[str],
            x_column: str,
            y_column: str,
            x_label: str,
            y_label: str,
            plot_type: str) -> None:
        plt.figure()
        for file_path, label in zip(file_paths, labels):
            df = pd.read_csv(file_path, sep=";")
            if plot_type == PlotTypes.SCATTER:
                plt.scatter(df[x_column], df[y_column], label=label, s=5)
            elif plot_type == PlotTypes.LINE:
                plt.plot(df[x_column], df[y_column], label=label)
            else:
                raise ValueError(f"Unsupported plot type: {plot_type}")
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        title = f"{x_label} vs {y_label}"
        plt.title(title)
        plt.grid(True)
        plt.legend()
        os.makedirs(
            FiguresDirectories.GENERATED_PICTURES_DIRECTORY,
            exist_ok=True)
        file_name = (
            title.replace("/", "_")
                 .replace(" ", "_")
                 .replace("[", "")
                 .replace("]", "")
                 .replace("°", "deg")
        )
        for extension in (
                FiguresDirectories
                        .GENERATED_PICTURES_EXTENSIONS
        ):
            plt.savefig(
                f"{FiguresDirectories.GENERATED_PICTURES_DIRECTORY}/"
                f"{file_name}.{extension}",
                dpi=300,
                bbox_inches="tight"
            )
        plt.show()
