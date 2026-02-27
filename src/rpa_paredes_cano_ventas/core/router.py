from configparser import ConfigParser
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


@dataclass(frozen=True, slots=True)
class Route:
    """Class to store paths such as bot's root, config, src directories, etc."""

    ROOT: Path
    DOT_DATA: Path
    CONFIG_DIR: Path
    PROJECT_DIR: Path
    LOGS_DIR: Path
    INPUT_DIR: Path
    OUTPUT_DIR: Path
    IMPORTACION_PATH: Path
    ACONSYS_PATH: Path
    DOC_PATH : Path
    TEMPLATE_PATH :Path
    TESSERACT:Path

    @classmethod
    def config(cls, bot_path: str, cp: ConfigParser) -> "Route":
        parents: Sequence[Path] = Path(bot_path).parents
        root: Path = parents[2]
        config_dir: Path = root / "config"
        project_dir: Path = parents[0]
        dot_data: Path = root / ".data"
        logs_dir: Path = dot_data / "logs"
        input_dir: Path = Path(
            cp.get("PATHS", "INPUT_PATH", fallback=dot_data / "input")
        )
        output_dir: Path = Path(
            cp.get("PATHS", "OUTPUT_PATH", fallback=dot_data / "output")
        )
        importacion_path: Path = Path(cp["PATHS"]["IMPORTACION_PATH"])
        aconsys_path: Path = Path(cp["PATHS"]["ACONSYS_PATH"])
        template_path: Path = Path(cp["PATHS"]["TEMPLATE_FILE_VENTAS"])
        doc_path: Path = Path(cp["PATHS"]["RUTA_DOC"])
        tesseract: Path = Path(cp["PATHS"]["TESSERACT"])

        for path in (logs_dir, dot_data):
            path.mkdir(parents=True, exist_ok=True)

        return cls(
            ROOT=root,
            PROJECT_DIR=project_dir,
            CONFIG_DIR=config_dir,
            DOT_DATA=dot_data,
            LOGS_DIR=logs_dir,
            INPUT_DIR=input_dir,
            OUTPUT_DIR=output_dir,
            IMPORTACION_PATH=importacion_path,
            ACONSYS_PATH=aconsys_path,
            TEMPLATE_PATH = template_path,
            DOC_PATH= doc_path,
            TESSERACT=tesseract,
        )