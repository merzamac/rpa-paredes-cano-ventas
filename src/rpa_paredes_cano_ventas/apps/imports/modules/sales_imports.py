from uiautomation import WindowControl, SendKeys
from datetime import date
from time import sleep
from pathlib import Path
from rpa_paredes_cano_ventas.apps.base import Process
from rpa_paredes_cano_ventas.utils.controls import wait_control_exist
from rpa_paredes_cano_ventas.utils.excel_manager import ExcelManager

# from contabot_ventas.helpers.excel_errores import (
#     cerrar_excel_abierto,
#     guardar_excel_abierto,
#     leer_columnas_serie_sucursal,
# )


class SalesImports(Process):
    def __init__(self, window: WindowControl) -> None:
        super().__init__(window)

    def select_file(self, file: Path):
        import_file_window = WindowControl(Name="Importar Archivo")
        select_button = self._window.ButtonControl(searchDepth=1, Name="Command7")
        self._wait_until_enabled(select_button)
        select_button.SetFocus()
        select_button.Click(simulateMove=False)
        if not import_file_window.Exists(maxSearchSeconds=3):
            select_button.SetFocus()
            select_button.Click(simulateMove=False)
        assert import_file_window.Exists(maxSearchSeconds=15)
        SendKeys("{Alt}m")
        sleep(1)
        SendKeys(str(file.resolve()))
        sleep(0.5)
        SendKeys("{ENTER}")

    @property
    def upload(self):
        assert self.buttons_area.Exists(maxSearchSeconds=15)
        upload_button = self.buttons_area.ButtonControl(searchDepth=1, Name="Cargar")
        self._wait_until_enabled(upload_button)
        assert upload_button.GetInvokePattern().Invoke()
        self._handle_vfp_dialog()
        self._wait_until_enabled(upload_button)
        sleep(3)

    # def export(self, save_dir: Path, period_date: date) -> Path:

    #     export_button = self.buttons_area.ButtonControl(searchDepth=1, Name="Exportar")
    #     # window_excel = WindowControl(searchDepth=1,Name="Libro2 - Excel")
    #     excel_window: WindowControl = WindowControl(
    #         ClassName="XLMAIN",
    #         RegexName=r"Libro.*",
    #         searchDepth=1,
    #         foundIndex=1,
    #     )
    #     self._wait_until_enabled(export_button)
    #     export_button.Click(simulateMove=False)
    #     sleep(3)
    #     if not excel_window.Exists():
    #         export_button.SetFocus()
    #         export_button.GetInvokePattern().Invoke()
    #     # esperar_excel()
    #     assert excel_window.Exists(maxSearchSeconds=30)
    #     name = f"errores{period_date.month:02d}{str(period_date.year)[-2:]}"
    #     file_dir = self._save_report(excel_window, save_dir, name)
    #     # importaciones = leer_columnas_serie_sucursal()
    #     # # Guardar Excel

    #     # ruta_guardado = guardar_excel_abierto(save_dir, nombre)

    #     # cerrar_excel_abierto()
    #     return file_dir

    # def _save_report(
    #     self, excel_window_control: WindowControl, save_dir: Path, report_name
    # ) -> Path:
    #     # is_ready: bool | None = False

    #     # while not is_ready:
    #     #     is_ready = process_status(excel_window_control.ProcessId)
    #     #     if is_ready is None:
    #     #         break
    #     wait_control_exist(excel_window_control)
    #     # if is_ready is None:
    #     #     raise ValueError("Imposible guardar el excel")
    #     # sleep(3.7)
    #     self.window_app.Minimize()
    #     excel_window: ExcelManager = ExcelManager(excel_window_control)
    #     excel_window.start()
    #     file_dir = excel_window.save(save_dir, report_name)
    #     excel_window.close()
    #     return file_dir

    @property
    def process(self) -> bool:
        """
        True: se encontro informacion para registrar, se debe exportar el exel.

        False: no hay informacion nueva, no se debe exportar
        """
        grid_area_row_1 = self._window.TableControl(
            searchDepth=2, Name="View 1"
        ).CustomControl(searchDepth=1, Name="1")
        process_button = self.buttons_area.ButtonControl(searchDepth=1, Name="Procesar")
        export_button = self.buttons_area.ButtonControl(searchDepth=1, Name="Exportar")
        self._wait_until_enabled(process_button)
        window = (
            self._window.GetParentControl().GetParentControl()
        )  # necesaria para capturar el dialogo
        dialog = window.WindowControl(searchDepth=1, Name="Microsoft Visual FoxPro")
        process_button.Click(simulateMove=False)
        if not dialog.Exists(maxSearchSeconds=3):
            process_button.SetFocus()
            process_button.Click(simulateMove=False)
        self._handle_vfp_dialog()

        sleep(3)
        self._wait_until_enabled(export_button)
        last_column = grid_area_row_1.GetLastChildControl()
        column_value = (
            last_column.EditControl(searchDepth=1, Name="Text1").GetValuePattern().Value
        )
        sleep(7)
        return bool(column_value.strip())

    @property
    def start(self) -> None:
        start_button = self.buttons_area.ButtonControl(searchDepth=1, Name="Iniciar")
        self._wait_until_enabled(start_button)
        assert start_button.GetInvokePattern().Invoke()
        self._handle_vfp_dialog()
