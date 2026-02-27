from numpy import save
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from enum import StrEnum
class DocumentType(StrEnum):
    OTROS:str="0"


class UtilityMut(type):
    __slots__ = []

    def __iter__(cls):
        # __dict__ mantiene el orden de inserción desde Python 3.7
        for key, value in cls.__dict__.items():
            if not key.startswith("_") and not callable(value):
                yield value

    def __call__(cls, *args, **kwargs):
        raise TypeError(
            f"{cls.__name__} es una clase de utilidad y no puede ser instanciada."
        )


class SuffixTypes(metaclass=UtilityMut):
    __slots__ = []
    # Definimos los sufijos como constantes de clase
    CSV = ".csv"
    XLSX = ".xlsx"
    JSON = ".json"
    TXT = ".txt"

    def __init__(self):
        raise TypeError(
            "SuffixTypes es una clase de constantes y no puede ser instanciada."
        )


@dataclass(frozen=True, slots=True)
class DataCSV:
    period: date
    files: tuple[Path, ...]
    save_dir: Path
