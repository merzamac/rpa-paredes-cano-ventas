# from rpa_paredes_cano_ventas.readers.input_files import GetInputFilesToProcess
# from pathlib import Path
# from rpa_paredes_cano_ventas.processor.chunk_processor import DataProcessor
# from rpa_paredes_cano_ventas.readers.fastexcel_reader import ExcelPLEReader
# from rpa_paredes_cano_ventas.models.header import Header


# def test_input_ventas(input_dir: Path, output_dir: Path):


#     for processable_file in GetInputFilesToProcess.execute(
#         input_dir=input_dir, output_dir=output_dir
#     ):
#         # Configuración
#         lector_excel = ExcelPLEReader(
#             sheet_name="SUNAT", expected_headers=tuple(Header)
#         )

#         # Ejecución
#         procesador = DataProcessor(lector_excel)
#         procesador.execute(processable_file, output_dir, batch_size=50000)
#     # subir los archivos y obtener los resultados
#     # obtener los centros de costo y cuentas corrientes del aconsys
