from dataclasses import dataclass
from asyncio.log import logger
from rpa_paredes_cano_ventas.orchestrator.file_processor import FileProcessor
from rpa_paredes_cano_ventas.orchestrator.import_platform import ImportPlatform
from rpa_paredes_cano_ventas.orchestrator.aconsys_platform import AconsysPlatform
from rpa_paredes_cano_ventas.readers.read_input_output import ReadOutputCSVPreviousMonth
from rpa_paredes_cano_ventas import routes
from rpa_paredes_cano_ventas.types import DAtaCSV
from rpa_paredes_cano_ventas.models.processable import ProcessableFile
from rpa_paredes_cano_ventas.readers.fastexcel_reader import ExcelPLEReader
from rpa_paredes_cano_ventas.models.header import Header


class BotOrchestrator:
    def __init__(self):
        self.file_service = FileProcessor()
        self.import_app = ImportPlatform()
        self.aconsys_app = AconsysPlatform()

    def run(self):
        # 1. Procesamiento Inicial
        csv_outputs: DAtaCSV | None = ReadOutputCSVPreviousMonth.execute(
            output_dir=routes.OUTPUT_DIR
        )
        if not csv_outputs:
            processable_files: tuple[ProcessableFile, ...] = (
                self.file_service.get_pending_files(
                    input_dir=routes.INPUT_DIR, output_dir=routes.OUTPUT_DIR
                )
            )

            for processable_file in processable_files:
                reader: ExcelPLEReader = ExcelPLEReader(
                    sheet_name="SUNAT", expected_headers=tuple(Header)
                )

                # Ejecución
                # self.file_service = FileProcessor()
                csv_outputs = self.file_service.create_massive_csv(
                    reader=reader,
                    processable=processable_file,
                    output_dir=routes.OUTPUT_DIR,
                    batch_size=50000,
                )

                BusinessRulesWithApps.execute(csv_outputs)
        BusinessRulesWithApps.execute(csv_outputs)
        print("Proceso de registro de series completado.")


@dataclass(frozen=True, slots=True)
class BusinessRulesWithApps:
    @staticmethod
    def execute(csv_outputs):
        # 2. Carga y Verificación
        import_results = import_app.upload_csvs(csv_outputs)

        if import_results.has_no_details():
            print("Proceso finalizado con éxito.")
            return

        # 3. Gestión de Diferencias (Aconsys)
        aconsys_files = aconsys_app.download_reports()
        new_series = file_service.identify_new_series(import_results, aconsys_files)

        if new_series:
            # 4. Registro en ambas plataformas
            aconsys_app.register_series(new_series)
            import_app.register_series(new_series)


# --- Ejecución ---
if __name__ == "__main__":
    bot = BotOrchestrator()
    bot.run()
