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
from datetime import date
from rpa_paredes_cano_ventas import routes

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


class ReadOutputCSVPrevious(metaclass=UtilityMut):
    __slots__ = []

    @staticmethod
    def execute(processable_file:ProcessableFile) -> DataCSV :
        """
        Args:
            output_dir (Path): La ruta de la carpeta de salida.

        Returns:
            tuple[ProcessableFile, ...]: Los archivos csv del mes anterior.


        El objetivo de esta clase es obtener los archivos csv del mes anterior.
        el fallo pero si logro crear los masivos del mes anterior.
        """
        input_files: tuple[Path, ...] = (
            *ReadDir.execute(processable_file.output_path, f"*{SuffixTypes.CSV}"),
        )

        return (
            DataCSV(
                period=processable_file.period_date, files=input_files, save_dir=processable_file.output_path
            )
            if input_files
            else None
        )
