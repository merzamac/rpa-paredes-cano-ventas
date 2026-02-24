from datetime import datetime, timedelta
from pathlib import Path
from rpa_paredes_cano_ventas.readers.read_dir import ReadDir
from rpa_paredes_cano_ventas.types import SuffixTypes
from rpa_paredes_cano_ventas.models.processable import (
    ProcessableFile,
    ProcessedFolder,
)
from rpa_paredes_cano_ventas.types import UtilityMut, DataCSV
from locale import setlocale, LC_TIME


class ReadInputDir(metaclass=UtilityMut):
    __slots__ = []

    @staticmethod
    def execute(input_dir: Path) -> tuple[ProcessableFile, ...]:

        input_files: tuple[Path, ...] = (
            *ReadDir.execute(input_dir, f"*{SuffixTypes.XLSX}"),
        )
        return tuple(
            processable_file
            for file_path in input_files
            if (processable_file := ProcessableFile(file_path=file_path))
        )


class ReadOutputDir(metaclass=UtilityMut):
    __slots__ = []

    @staticmethod
    def execute(output_dir: Path) -> tuple[ProcessedFolder, ...]:
        recursive: bool = False
        output_files: tuple[Path, ...] = (
            *ReadDir.execute(dir_path=output_dir, pattern="*/*/", recursive=recursive),
        )
        output_files: tuple[Path, ...] = tuple(
            file
            for file in output_files
            if file.is_dir()
            and file.parent.name.isdigit()
            and len(file.name) >= 4
            and len(file.parent.name) >= 4
        )
        return tuple(
            processable_file
            for file_path in output_files
            if (processable_file := ProcessedFolder(output_path=file_path))
        )


class ReadOutputCSVPreviousMonth(metaclass=UtilityMut):
    __slots__ = []

    @staticmethod
    def execute(output_dir: Path) -> tuple[ProcessableFile, ...] | None:
        """
        Args:
            output_dir (Path): La ruta de la carpeta de salida.

        Returns:
            tuple[ProcessableFile, ...]: Los archivos csv del mes anterior.


        El objetivo de esta clase es obtener los archivos csv del mes anterior.
        el fallo pero si logro crear los masivos del mes anterior.
        """
        setlocale(LC_TIME, "es_ES.UTF-8")
        today = datetime.today()
        month_before = today.replace(day=1) - timedelta(days=1)
        month_str = month_before.strftime("%B").upper()
        year_str = month_before.strftime("%Y")
        file_output_dir = output_dir / year_str / month_str
        input_files: tuple[Path, ...] = (
            *ReadDir.execute(file_output_dir, f"*{SuffixTypes.CSV}"),
        )

        return (
            DataCSV(
                period=month_before.date(), files=input_files, save_dir=file_output_dir
            )
            if input_files
            else None
        )
