from rpa_paredes_cano_ventas.exceptions.structure_sunat import (
    SheetNameNotFoundError,
    ColumnMismatchTemplateError,
    PositionSheetNameNotZeroError,
)
from rpa_paredes_cano_ventas.interfaces.base import FileDataReader
from loguru import logger
from fastexcel import read_excel
from pathlib import Path
from pandas import DataFrame


class ExcelPLEReader(FileDataReader):
    def __init__(self, sheet_name: str, expected_headers: tuple):
        self.sheet_name = sheet_name
        self.expected_headers = expected_headers

    def validate_headers(self, metadata_header: tuple) -> None:
        headers = tuple(str(column.name) for column in metadata_header)
        if self.expected_headers and headers != self.expected_headers:
            raise ColumnMismatchTemplateError(headers, self.expected_headers)

    def get_data(self, file_path: Path, chunk_size: int = 50000) -> DataFrame:
        # Usamos read_only para eficiencia de memoria
        wb = read_excel(source=file_path)

        # 2. Validar que la hoja exista (Evita errores silenciosos)
        if self.sheet_name not in wb.sheet_names:
            raise SheetNameNotFoundError(sheet_name, wb.sheet_names)

        if not (self.sheet_name == wb.sheet_names[0]):
            raise PositionSheetNameNotZeroError(self.sheet_name, wb.sheet_names)
        # 3. Obtener metadatos iniciales sin cargar toda la hoja
        metadata = wb.load_sheet(
            idx_or_name=0,
            dtypes="string",  # Forzamos string para evitar problemas de tipos mixtos
            n_rows=0,
        )
        self.validate_headers(tuple(metadata.selected_columns))
        total_rows = metadata.total_height

        logger.info(f"Procesando {total_rows} filas en bloques de {chunk_size}...")

        # 4. Bucle de procesamiento por bloques
        skip_rows = 0
        while skip_rows < total_rows:
            # Cargamos solo el bloque actual
            sheet = wb.load_sheet(
                idx_or_name=0,
                dtypes="string",  # Forzamos string para evitar problemas de tipos mixtos
                n_rows=chunk_size,
                skip_rows=skip_rows,
            )

            df: DataFrame = sheet.to_pandas()

            yield df
            logger.info(f"Procesado bloque: {skip_rows} a {skip_rows + len(df)}")
            # ------------------------------------------
            skip_rows += chunk_size
