from pandas import DataFrame, ExcelWriter
from pathlib import Path
from loguru import logger
from pathlib import Path
from rpa_paredes_cano_ventas.types import SuffixTypes


class Export:
    """Estrategia para recibir bloques de datos y consolidarlos directamente."""

    def __init__(self, output_path: Path) -> None:
        output_path.mkdir(parents=True, exist_ok=True)
        self.current_row = 0
        self.writer = ExcelWriter(
            (output_path / f"import{SuffixTypes.XLSX}"), engine="xlsxwriter"
        )

    def add_block(self, df_block: DataFrame, sheet_name: str = "IMPORT"):
        """Recibe un DataFrame de 50k filas y lo pega al Excel inmediatamente."""
        is_first = self.current_row == 0
        # Limpieza rápida antes de escribir
        # df_block = df_block.fillna("")

        # Escritura al vuelo
        df_block.to_excel(
            excel_writer=self.writer,
            sheet_name=sheet_name,
            startrow=self.current_row,
            index=False,
            header=is_first,
        )

        # Actualizar puntero (Filas + 1 si hubo cabecera)
        self.current_row += len(df_block) + (1 if is_first else 0)

    def csv(self, chunk: DataFrame, output_path: Path, int_sheet_name: int) -> Path:
        output_path = output_path / f"{int_sheet_name}{SuffixTypes.CSV}"
        chunk.to_csv(
            output_path,
            index=False,
            header=True,
            encoding="utf-8",
        )
        return output_path

    def close(self):
        """Cierra el archivo y libera la memoria."""
        self.writer.close()
