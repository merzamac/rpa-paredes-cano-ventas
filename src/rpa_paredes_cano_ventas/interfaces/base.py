from pandas import DataFrame
from abc import ABC, abstractmethod
from pathlib import Path


class FileDataReader(ABC):
    @abstractmethod
    def get_data(self, file_path: Path, chunk_size: int) -> DataFrame:
        """Generador que entrega bloques de datos"""
        pass

    @abstractmethod
    def validate_headers(self, headers):
        """Lógica de validación de columnas"""
        pass
