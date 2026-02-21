# ""from calendar import month
# from openpyxl import load_workbook
# from dataclasses import dataclass, fields

# import locale
# from pathlib import Path
# from datetime import date


# class PLEStructureError(Exception):
#     """Clase base para excepciones del PLE."""

#     pass


# class DifferentTemplateLengthError(PLEStructureError):
#     """Se lanza cuando el número de columnas no coincide con el esperado."""

#     def __init__(self, actual, expected):
#         self.message = (
#             f"Column count mismatch: Excel has {actual}, expected {expected}."
#         )
#         super().__init__(self.message)


# class ColumnMismatchTemplateError(PLEStructureError):
#     """Se lanza cuando el nombre o posición de una columna no coincide."""

#     def __init__(self, index, actual, expected, attribute_name):
#         self.message = (
#             f"Column mismatch at index {index} (Attribute: {attribute_name}): "
#             f"Found '{actual}', expected '{expected}'."
#         )
#         super().__init__(self.message)


# class PLEValidator:
#     """Clase especializada en validar la integridad de archivos PLE."""

#     @staticmethod
#     def header_structure(first_row_ws, header_desc_cls) -> None:
#         # 1. Preparar headers (Excel vs Template)
#         header = tuple(str(cell.value).strip().lower() for cell in first_row_ws)
#         fields_template = fields(header_desc_cls)
#         header_template = tuple(f.default for f in fields_template)

#         # 2. Validar Longitud
#         if len(header) != len(header_template):
#             raise DifferentTemplateLengthError(len(header), len(header_template))

#         # 3. Validar Contenido y Orden
#         for index_column, column_template in enumerate(header_template):
#             column_data = header[index_column]
#             if column_data != column_template:
#                 # Obtenemos el nombre del atributo (ej: 'periodo') para el error
#                 attr_name = fields_template[index_column].name
#                 raise ColumnMismatchTemplateError(
#                     index_column, column_data, column_template, attr_name
#                 )


# def test_excel():
#     sheet_name = "SUNAT"
#     archivo = "01. PLE ENERO.26.xlsx"
#     bloque_size = 50000
#     wb = load_workbook(filename=archivo, read_only=True, data_only=True)
#     # Seleccionar la hoja
#     if sheet_name:
#         ws = wb[sheet_name]
#     else:
#         ws = wb.active
#     # --- Procesamiento por bloques ---
#     bloque_actual = []

#     PLEValidator.header_structure(ws[1], HeaderDescripcion)
#     # --- Procesamiento por bloques ---
#     # ultima fila con datos

#     # Iterar sobre las filas de la hoja
#     for row in ws.iter_rows(
#         min_row=2, values_only=True
#     ):  # values_only=True nos da los valores directamente
#         value_first_column = row[0]
#         if not value_first_column:
#             # esta fila empiza vacio, por ende, es la ultima
#             break
#         bloque_actual.append(row)
#         # Si alcanzamos el tamaño del bloque, lo entregamos y reiniciamos
#         if len(bloque_actual) == bloque_size:
#             return bloque_actual
#             bloque_actual = []  # Reiniciar el bloque

#     # No olvidar entregar el último bloque (que puede ser más pequeño)
#     if bloque_actual:

#         return bloque_actual

#     # Es muy importante cerrar el workbook
#     wb.close()


# @dataclass(frozen=True, slots=True)
# class HeaderDescripcion:
#     """
#     Fuente única de verdad. El orden aquí define el índice en HeaderPLE.
#     Los valores son los nombres exactos de las columnas en el Excel.
#     """

#     periodo: str = "periodo"
#     tipo_cuo: str = "tipo cuo"
#     nro_cuo: str = "nº cuo"
#     fecha_emision: str = "fecha emisión comprobante"
#     fecha_vencimiento: str = "fecha de vencimiento"
#     tipo_comprobante: str = "tipo\ncomprobante"
#     serie_comprobante: str = "serie comprobante"
#     nro_comprobante_ini: str = "nº comprobante inicial"
#     nro_comprobante_fin: str = "nº comprobante final"
#     dif: str = "dif"
#     tipo_doc_cliente: str = "tipo de doc. cliente"
#     nro_doc_cliente: str = "nº de doc. cliente"
#     nombre_razon_social: str = "nombre/razon social"
#     bi_exportacion: str = "bi._exportacion"
#     bi_gravado: str = "bi adq. vtas. grav"
#     dscto_bi: str = "dscto bi"
#     igv_gravado: str = "igv adq. vtas. grav"
#     dscto_igv: str = "dscto igv"
#     exonerado: str = "imp. total adquicisiones exoneradas"
#     inafecto: str = "imp. total operaciones inafectas"
#     isc: str = "isc"
#     bi_arroz: str = "bi. operaciones gravadas c/ el igv del arroz pilado"
#     igv_arroz: str = "imp. a las ventas del arroz pilado"
#     otros: str = "otros"
#     importe: str = "importe"
#     moneda: str = "cod moneda"
#     tipo_cambio: str = "tipo cambio"
#     fecha_modifica: str = "fecha emision comprobantes pago que modifica"
#     tipo_modifica: str = "tipo comprobante pago modifica"
#     serie_modifica: str = "nº serie comprobante modifica"
#     nro_modifica: str = "nº comprobante pago modifica"
#     id_contrato: str = "identif del contrato"
#     error_1: str = "error tipo 1"
#     indicador_cp: str = "indicador comprobantes de pago"
#     estado: str = "estado"
#     segmento_negocio: str = "segmentodenegocio"
#     sucursal: str = "sucursal"
#     nro_caja: str = "nro_caja"
#     centro_costo: str = "centro de costo"


# class MetaInmutable(type):
#     """
#     Metaclase para proteger HeaderPLE contra modificaciones.
#     """

#     def __setattr__(cls, name, value):
#         raise AttributeError("HeaderPLE es inmutable. No puedes cambiar los índices.")


# class HeaderPLE(metaclass=MetaInmutable):
#     """
#     Mapeo de índices autogenerado desde HeaderDescripcion.
#     Uso: row[HeaderPLE.moneda] -> Accede a la columna 25.
#     """

#     __slots__ = ()
#     # Generación dinámica de índices (periodo=0, tipo_cuo=1, etc.)
#     for i, campo in enumerate(fields(HeaderDescripcion)):
#         locals()[campo.name] = i

#     def __init__(self):
#         raise TypeError("HeaderPLE es estática y no puede ser instanciada.")


# def test_sistema_ple():
#     print("--- Iniciando Pruebas de HeaderPLE ---")

#     # 1. Prueba de Índices Autogenerados
#     try:
#         assert HeaderPLE.periodo == 0
#         assert HeaderPLE.centro_costo == 38
#         assert HeaderPLE.moneda == 25
#         print("✅ Prueba de índices: PASADA")
#     except AssertionError:
#         print("❌ Prueba de índices: FALLÓ")

#     # 3. Prueba de Inmutabilidad (Protección de la Metaclase)
#     try:
#         HeaderPLE.periodo = 99
#     except AttributeError as e:
#         print(f"✅ Prueba de inmutabilidad (Protección activa): PASADA -> {e}")
#     else:
#         print("❌ Prueba de inmutabilidad: FALLÓ (Se permitió modificar el índice)")

#     # 4. Prueba de Prohibición de Instancia
#     try:
#         h = HeaderPLE()
#     except TypeError as e:
#         print(f"✅ Prueba de no-instanciación: PASADA -> {e}")

#     # 5. Simulación de procesamiento de fila
#     fila_simulada = ["20260100", "CUO-001", "1", "2026-01-15"] + ["..."] * 35
#     print(f"\nSimulando fila:")
#     print(
#         f" - Periodo (Índice {HeaderPLE.periodo}): {fila_simulada[HeaderPLE.periodo]}"
#     )
#     print(f" - CUO (Índice {HeaderPLE.nro_cuo}): {fila_simulada[HeaderPLE.nro_cuo]}")


# from abc import ABC, abstractmethod


# class FileDataReader(ABC):
#     @abstractmethod
#     def get_data(self, file_path, chunk_size):
#         """Generador que entrega bloques de datos"""
#         pass

#     @abstractmethod
#     def validate_headers(self, headers):
#         """Lógica de validación de columnas"""
#         pass


# class ExcelPLEReader(FileDataReader):
#     def __init__(self, sheet_name: str, expected_headers: tuple):
#         self.sheet_name = sheet_name
#         self.expected_headers = expected_headers

#     def validate_headers(self, row_values) -> None:
#         headers = tuple(str(cell).strip().lower() for cell in row_values)
#         if self.expected_headers and headers != self.expected_headers:
#             raise ValueError(
#                 f"Invalid headers: {headers}. Expected: {self.expected_headers}"
#             )

#     def get_data(self, file_path, chunk_size=50000):
#         # Usamos read_only para eficiencia de memoria
#         wb = load_workbook(filename=file_path, read_only=True, data_only=True)
#         try:
#             if self.sheet_name not in wb.sheetnames:
#                 raise ValueError(
#                     f"Sheetname {self.sheet_name} not found in the Excel file. Available sheetnames: {wb.sheetnames}"
#                 )
#             ws = wb[self.sheet_name]
#             # Obtener y validar cabeceras (Fila 1)
#             header_row = next(ws.iter_rows(min_row=1, max_row=1, values_only=True))
#             self.validate_headers(header_row)

#             bloque = []
#             for row in ws.iter_rows(min_row=2, values_only=True):
#                 if not row[0]:  # Celda vacía marca el fin
#                     break

#                 bloque.append(row)

#                 if len(bloque) == chunk_size:
#                     yield bloque
#                     bloque = []

#             if bloque:
#                 yield bloque
#         finally:
#             wb.close()


# class DataProcessor:
#     def __init__(self, reader: FileDataReader):
#         self.reader = reader

#     def execute(self, file_path: Path, batch_size: int):
#         print(f"Iniciando procesamiento de: {file_path}")
#         int_sheet_name = 0
#         for i, chunk in enumerate(self.reader.get_data(file_path, batch_size), 1):

#             int_sheet_name += len(chunk)
#             # Aquí va tu lógica de negocio para cada bloque
#             self._process_chunk(chunk, int_sheet_name)

#         print("Procesamiento finalizado con éxito.")

#     def _process_chunk(self, chunk, int_sheet_name: int):
#         print(f"Procesando bloque {int_sheet_name} con {len(chunk)} registros...")


# def test_excel():
#     file_input = Path(
#         r"C:\Users\merzamac\Desktop\universidad\servicio-comunitario-uc\2025\01. PLE ENERO 26.xlsx"
#     )
#     expected_headers = tuple(cell.default for cell in fields(HeaderDescripcion))
#     # Configuración
#     lector_excel = ExcelPLEReader(sheet_name="SUNAT", expected_headers=expected_headers)

#     # Ejecución
#     procesador = DataProcessor(lector_excel)
#     procesador.execute(file_input, batch_size=50000)


# from typing import Any

# from datetime import date
# from pathlib import Path
# from pydantic import (
#     BaseModel,
#     validator,
#     model_validator,
#     field_validator,
#     ConfigDict,
#     Field,
# )


# # class ProcessableFile(BaseModel):
# #     model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)
# #     file_path: Path
# #     output_path: Path = None
# #     period_date: date = None
# #     month: str = None
# #     year: str = None

# #     @field_validator("file_path")
# #     @classmethod
# #     def validate_file_path(cls, value: Path) -> Path:
# #         # Validaciones previas
# #         if not value.exists():
# #             raise FileNotFoundError(f"File not found: {value}")

# #         if not value.is_file():
# #             raise ValueError(f"It is not a file: {value}")

# #         if value.suffix.lower() != ".xlsx":
# #             raise ValueError(f"It is not an Excel file: {value.suffix.lower()}")
# #         return value

# #     @model_validator(mode="after")
# #     def _validate_others(self) -> "ProcessableFile":
# #         folder_year = self.file_path.parent.name
# #         stem_parts = self.file_path.stem.strip().split()

# #         month_number = stem_parts[0].replace(".", "")
# #         ple = stem_parts[1].upper()
# #         month = stem_parts[2].upper()
# #         year = stem_parts[3]

# #         if not folder_year.isdigit():
# #             raise ValueError(f"Invalid file name: {folder_year} is not a number")
# #         if not (
# #             len(month_number) == 2
# #             and len(month) >= 4
# #             and len(year) == 2
# #             and len(ple) == 3
# #             and len(folder_year) == 4
# #         ):
# #             raise ValueError(
# #                 f"Invalid file name: {month_number} == 2, {month}>= 4, {year}== 2, {ple}== 3, {folder_year}== 4"
# #             )

# #         # Usar object.__setattr__ porque usamos frozen=True
# #         object.__setattr__(
# #             self, "period_date", date(int(folder_year), int(month_number), 1)
# #         )
# #         object.__setattr__(self, "month", month)
# #         object.__setattr__(self, "year", folder_year)
# #         object.__setattr__(self, "output_path", Path(folder_year) / month)

# #         return self

# #     def __hash__(self) -> int:
# #         """Hash basado en la ruta (única para cada archivo)."""
# #         return hash(self.period_date)

# #     def __eq__(self, other):
# #         if not hasattr(other, "period_date"):
# #             return False
# #         return self.period_date == other.period_date


# # from dateparser import parse
# # from datetime import datetime


# # from pydantic import BaseModel, ConfigDict, model_validator
# # from pathlib import Path
# # from datetime import date
# # from dateparser import parse


# # class ProcessedFolder(BaseModel):
# #     model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)
# #     output_path: Path
# #     period_date: date = None

# #     @model_validator(mode="after")
# #     def parse_folder_date(self) -> "ProcessedFolder":
# #         # folder_path.parts descompone la ruta: ('2026', 'ENERO')
# #         year, month = self.output_path.parts[-2:]
# #         if not year.isdigit():
# #             raise ValueError(f"Invalid folder name OUTPUT {year}: {self.output_path}")

# #         if not (len(month) >= 4) and not month.isalpha():
# #             raise ValueError(f"Invalid folder name OUTPUT {month}: {self.output_path}")
# #         # Usamos dateparser para convertir "ENERO" a objeto datetime
# #         parsed = parse(f"1 {month} {year}", languages=["es"])
# #         if not parsed:
# #             raise ValueError(f"Invalid folder name OUTPUT {month}/{year}")

# #         object.__setattr__(self, "period_date", parsed.date())
# #         return self

# #     def __hash__(self):
# #         return hash(self.period_date)

# #     def __eq__(self, other):
# #         if not hasattr(other, "period_date"):
# #             return False
# #         return self.period_date == other.period_date


# # def test_archivos_procesables():
# #     ruta_base = Path(r"C:\Users\merzamac\Desktop\universidad\servicio-comunitario-uc")

# #     folder_tuple = tuple(
# #         p for p in ruta_base.glob("*/*/") if p.is_dir() and p.parent.name.isdigit()
# #     )
# #     file_input = Path(
# #         r"C:\Users\merzamac\Desktop\universidad\servicio-comunitario-uc\2025\01. PLE ENERO 26.xlsx"
# #     )

# #     files_to = ProcessableFile(file_path=file_input)
# #     output = ProcessedFolder(output_path=folder_tuple[0])

# #     input_set = set([files_to])
# #     output_set = set([output])
# #     solo_input = input_set - output_set
# #     assert solo_input


# from datetime import date
# from pathlib import Path
# from typing import Optional, Set

# from dateparser import parse
# from pydantic import (
#     BaseModel,
#     ConfigDict,
#     Field,
#     field_validator,
#     model_validator,
# )


# class FileProcessorError(Exception):
#     """Base exception for the file processing module."""

#     pass


# class InvalidFileNameError(FileProcessorError):
#     """Raised when the Excel file name doesn't match the expected 'XX. PLE MONTH YY' format."""

#     pass


# class InvalidFolderPathError(FileProcessorError):
#     """Raised when the folder path doesn't have the expected 'YEAR/MONTH' structure."""

#     pass


# class DateParsingError(FileProcessorError):
#     """Raised when dateparser fails to interpret the provided month/year strings."""

#     pass


# class BasePeriodModel(BaseModel):
#     """Base class to handle shared equality and hashing logic."""

#     model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)
#     period_date: Optional[date] = None

#     def __hash__(self) -> int:
#         return hash(self.period_date)

#     def __eq__(self, other: object) -> bool:
#         if not isinstance(other, BasePeriodModel):
#             return False
#         return self.period_date == other.period_date


# class ProcessableFile(BasePeriodModel):
#     file_path: Path
#     output_path: Optional[Path] = None
#     month: Optional[str] = None
#     year: Optional[str] = None

#     @field_validator("file_path")
#     @classmethod
#     def validate_file_path(cls, value: Path) -> Path:
#         if not value.exists():
#             raise FileNotFoundError(f"File not found: {value}")
#         if value.suffix.lower() != ".xlsx":
#             raise ValueError(f"Not an Excel file: {value.suffix}")
#         return value

#     @model_validator(mode="before")
#     @classmethod
#     def extract_metadata(cls, data: dict) -> dict:
#         """Parses the file path to populate fields before the model is frozen."""
#         if isinstance(data, dict) and "file_path" in data:
#             path = Path(data["file_path"])
#             folder_year = path.parent.name

#             # Logic: "01. PLE ENERO 26.xlsx" -> ['01.', 'PLE', 'ENERO', '26']
#             stem_parts = path.stem.strip().split()
#             len_parts = len(stem_parts)
#             if len_parts < 4 or not folder_year.isdigit():
#                 raise InvalidFileNameError(
#                     f"Filename format unexpected: {path.name}... len_parts: {len_parts} folder_year: {folder_year}"
#                 )

#             month_number = stem_parts[0].replace(".", "")
#             month = stem_parts[2].upper()
#             if not (
#                 len(month_number) == 2 and len(month) >= 4 and len(folder_year) == 4
#             ):
#                 raise InvalidFileNameError(f"Filename format unexpected: {path.name}")

#             # Populate the data dict so Pydantic initializes them normally
#             data["year"] = folder_year
#             data["month"] = month
#             data["period_date"] = date(int(folder_year), int(month_number), 1)
#             data["output_path"] = Path(folder_year) / month

#         return data


# class ProcessedFolder(BasePeriodModel):
#     output_path: Path

#     @model_validator(mode="before")
#     @classmethod
#     def parse_folder_date(cls, data: dict) -> dict:
#         if isinstance(data, dict) and "output_path" in data:
#             path = Path(data["output_path"])
#             # parts[-2:] gives (year, month)
#             try:
#                 year, month = path.parts[-2:]
#             except ValueError:
#                 raise InvalidFolderPathError(f"Path too short: {path}")

#             parsed = parse(f"1 {month} {year}", languages=["es"])
#             if not parsed:
#                 raise DateParsingError(f"Could not parse date from:  {month}/{year}")

#             data["period_date"] = parsed.date()
#         return data


# # --- Test Logic ---
# def test_archivos_procesables():
#     ruta_base = Path(
#         "C:/Users/merzamac/Desktop/universidad/servicio-comunitario-uc/botVentas"
#     )
#     folder_output = tuple(
#         p for p in ruta_base.glob("*/*/") if p.is_dir() and p.parent.name.isdigit()
#     )
#     folder_output = tuple(ruta_base.glob(pattern="*/*/"))

#     file_input = Path(
#         r"C:\Users\merzamac\Desktop\universidad\servicio-comunitario-uc\2025\01. PLE ENERO 26.xlsx"
#     )

#     # Both objects will have period_date = 2025-01-01
#     file_obj = ProcessableFile(file_path=file_input)
#     folder_obj = ProcessedFolder(output_path=folder_output[0])

#     input_set: Set[BasePeriodModel] = {file_obj}
#     output_set: Set[BasePeriodModel] = {folder_obj}

#     # Difference works because hashes and __eq__ match via period_date
#     solo_input = input_set - output_set

#     assert len(solo_input) == 0
#     print("Test passed: File and Folder match correctly!")


# import python_calamine


# def test_excel_calamine():
#     file_input = Path(
#         r"C:\Users\merzamac\Desktop\universidad\servicio-comunitario-uc\2025\01. PLE ENERO 26.xlsx"
#     )
#     chunk_size = 50000
#     with open(file_input, "rb") as f:
#         wb = python_calamine.CalamineWorkbook.from_filelike(f)
#         if "SUNAT" not in wb.sheet_names:
#             raise ValueError(
#                 f"Sheetname  not found in the Excel file. Available sheetnames: {wb.sheetnames}"
#             )
#             # Obtener la hoja por índice (más rápido que por nombre)
#         sheet_idx = wb.sheet_names.index("SUNAT")
#         sheet = wb.get_sheet_by_index(sheet_idx)
#         all_rows = sheet.to_python()
#         if not all_rows:
#             return

#             # La primera fila son los headers
#         header_row = all_rows[0]
#         # self.validate_headers(header_row)

#         # Procesar el resto por bloques
#         bloque_actual = []
#         total_filas = len(all_rows)

#         for idx in range(1, total_filas):  # Empezar desde la fila 1 (saltando headers)
#             row = all_rows[idx]

#             # Si la primera columna está vacía, asumimos que es el final
#             if not row or len(row) == 0 or row[0] is None:
#                 print(f"📌 Fin detectado en fila {idx + 1} (primera columna vacía)")
#                 break

#             bloque_actual.append(tuple(row))  # Convertir a tuple para consistencia

#             if len(bloque_actual) == chunk_size:
#                 print(f"📦 Entregando bloque con {len(bloque_actual)} filas")
#                 # yield bloque_actual
#                 bloque_actual = []

#             # Último bloque
#         if bloque_actual:
#             print(f"📦 Entregando bloque final con {len(bloque_actual)} filas")
#             # yield bloque_actual


# import fastexcel
# import polars as pl
# import pandas as pd


# def test_fastexcel():
#     file_input = Path(
#         r"C:\Users\merzamac\Desktop\universidad\servicio-comunitario-uc\2025\01. PLE ENERO 26.xlsx"
#     )
#     file_path = Path(r"C:\Users\merzamac\Desktop\01. PLE ENERO.26.xlsx")
#     chunk_size = 50000
#     sheet_name = "SUNAT"
#     # 1. Cargar el libro
#     excel = fastexcel.read_excel(file_path)

#     # 2. Validar que la hoja exista (Evita errores silenciosos)
#     if sheet_name not in excel.sheet_names:
#         raise ValueError(
#             f"La hoja '{sheet_name}' no existe. Disponibles: {excel.sheet_names}"
#         )

#     # 3. Obtener metadatos iniciales sin cargar toda la hoja
#     # Usamos n_rows=0 solo para obtener el 'total_height'
#     metadata = excel.load_sheet(0, n_rows=0)
#     total_rows = metadata.total_height

#     print(f"Procesando {total_rows} filas en bloques de {chunk_size}...")

#     # 4. Bucle de procesamiento por bloques
#     skip_rows = 0
#     while skip_rows < total_rows:
#         # Cargamos solo el bloque actual
#         sheet = excel.load_sheet(
#             idx_or_name=sheet_name,
#             dtypes="string",  # Forzamos string para evitar problemas de tipos mixtos
#             n_rows=chunk_size,
#             skip_rows=skip_rows,
#         )

#         df = sheet.to_pandas()

#         # --- Aquí va tu lógica de procesamiento ---
#         # Ejemplo: yield df (si quieres usarlo como generador)
#         print(f"Procesado bloque: {skip_rows} a {skip_rows + len(df)}")
#         # ------------------------------------------

#         skip_rows += chunk_size
""""""
