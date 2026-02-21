from pathlib import Path
from typing import Generator
from rpa_paredes_cano_ventas.types import UtilityMut


class ReadDir(metaclass=UtilityMut):
    __slots__ = []

    @staticmethod
    def execute(
        dir_path: Path, pattern: str, recursive: bool = True
    ) -> Generator[Path, None, None]:
        """
        Retorna un generador de rutas de archivos.

        Args:
            dir_path: Ruta del directorio.
            pattern: Patrón de búsqueda (ej. '*.csv').
            recursive: Si es True usa rglob (recursivo), si es False usa glob (solo nivel actual).
        """
        # Usamos un operador ternario para retornar el generador directamente.
        # Esto evita cargar listas en memoria y mantiene la evaluación perezosa (lazy).
        return (
            dir_path.rglob(pattern, case_sensitive=False)
            if recursive
            else dir_path.glob(pattern, case_sensitive=False)
        )
