import os

from constants.generated_results import (
    GeneratedResults
)

class FiguresDirectories:
    GENERATED_PICTURES_DIRECTORY = os.path.join(
        GeneratedResults.RESULTS_DIRECTORY,
        "generated_step_response_pictures"
    )

    GENERATED_PROPERTIES_PICTURES_DIRECTORY = os.path.join(
        GeneratedResults.RESULTS_DIRECTORY,
        "generated_properties_pictures"
    )

    GENERATED_PICTURES_EXTENSIONS: list[str] = [
        "pdf",
        "png"
    ]