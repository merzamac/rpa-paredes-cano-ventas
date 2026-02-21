from pathlib import Path
from rpa_paredes_cano_ventas.models.processable import (
    ProcessableFile,
    ProcessedFolder,
)
from rpa_paredes_cano_ventas.readers.read_input_output import (
    ReadInputDir,
    ReadOutputDir,
)
from rpa_paredes_cano_ventas.types import UtilityMut


class GetInputFilesToProcess(metaclass=UtilityMut):
    __slots__ = []

    @staticmethod
    def execute(input_dir: Path, output_dir: Path) -> tuple[ProcessableFile, ...]:
        processable_input_files: tuple[ProcessableFile, ...] = ReadInputDir.execute(
            input_dir=input_dir
        )
        processable_output_folders: tuple[ProcessedFolder, ...] = ReadOutputDir.execute(
            output_dir=output_dir
        )

        input_files_to_process: set[ProcessableFile] = set(
            processable_input_files
        ) - set(processable_output_folders)

        return tuple(input_files_to_process)
