from asyncio.log import logger
from rpa_paredes_cano_ventas import routes
from rpa_paredes_cano_ventas.types import DataCSV
from rpa_paredes_cano_ventas.models.header import Header
from rpa_paredes_cano_ventas.models.processable import ProcessableFile
from rpa_paredes_cano_ventas.readers.fastexcel_reader import ExcelPLEReader
from rpa_paredes_cano_ventas.orchestrator.file_processor import FileProcessor
from rpa_paredes_cano_ventas.orchestrator.import_platform import ImportPlatform
from rpa_paredes_cano_ventas.orchestrator.aconsys_platform import AconsysPlatform
from rpa_paredes_cano_ventas.orchestrator.business_rules import BusinessRulesWithApps
from rpa_paredes_cano_ventas.readers.read_input_output import ReadOutputCSVPrevious
from rpa_paredes_cano_ventas.utils.state_manager import StateManager

class BotOrchestrator:
    def __init__(self):
        self.file_service = FileProcessor()

    def run(self):
        # 1. Procesamiento Inicial
        processable_files: tuple[ProcessableFile, ...] = (
            self.file_service.get_pending_files(
                input_dir=routes.INPUT_DIR, output_dir=routes.OUTPUT_DIR
            )
        )

        for processable_file in processable_files:
            state = StateManager(routes.BOT_STATE,processable_file.period_date)
            if state.is_first_phase_done and state.is_last_phase_done: 
                continue
            if not state.is_first_phase_done:
                reader: ExcelPLEReader = ExcelPLEReader(
                        sheet_name="SUNAT", expected_headers=tuple(Header)
                )
            
                # Ejecución
                csv_outputs = self.file_service.create_massive_csv(
                    reader=reader,
                    processable=processable_file,
                    batch_size=50000,
                )
                # marca que la primer fase esta hecha
                state.first_phase()
            else:
                csv_outputs = ReadOutputCSVPrevious.execute(processable_file)

            if not csv_outputs.files:
                raise ValueError("La primera fase fue completada pero no hay archivos")
            BusinessRulesWithApps.execute(csv_outputs)
            state.last_phase()
            logger.info("Proceso finalizado con éxito.")



# --- Ejecución ---
if __name__ == "__main__":
    bot = BotOrchestrator()
    bot.run()
