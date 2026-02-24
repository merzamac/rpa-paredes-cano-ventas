from uiautomation import WindowControl, SendKeys
from datetime import date
from pathlib import Path
from rpa_paredes_cano_ventas.apps.base import TopLevelWindow
from rpa_paredes_cano_ventas.types import DataCSV
from typing import Optional
from rpa_paredes_cano_ventas.apps.imports import (
    SalesImports,
    SalesCancellation,
    SeriesByCostCenter,
)

# from contabot_ventas.importaciones.utils import navegar_menu_sistema
from time import sleep

NOMBRE_MESES = [
    "enero",
    "febrero",
    "marzo",
    "abril",
    "mayo",
    "junio",
    "julio",
    "agosto",
    "septiembre",
    "octubre",
    "noviembre",
    "diciembre",
]

now = date.today()
mes = NOMBRE_MESES[now.month - 1].capitalize()
anio = now.year

IMPORT_MAIN_WINDOW = WindowControl(
    Name=f" Módulo Importación - Bijou - Ventas ({mes} de {anio})"
)

IMPORT_LOGIN_WINDOW = WindowControl(searchDepth=1, Name="Módulo Importación")


class ImportMainWindow(TopLevelWindow):
    _window = IMPORT_MAIN_WINDOW

    @property
    def sales_imports(self):
        window = self._open_system_window("Importación Ventas", pasos_derecha=5)
        return SalesImports(window)

    @property
    def sales_cancellation(self):
        window = self._open_system_window(
            "Cancelación de Ventas", pasos_derecha=5, pasos_abajo=1, enter_count=1
        )
        return SalesCancellation(window)

    def import_files(self, data_csv: DataCSV) -> Optional[Path]:
        importacion = self.sales_imports
        importacion.period(data_csv.period)
        importacion.start

        for file in data_csv.files:
            importacion.select_file(file)
            importacion.upload

        excel_file: Optional[Path] = None
        # Solo intentamos exportar si la plataforma indica que hay algo que procesar
        if importacion.process:
            # Asumimos que el primer archivo nos da la ruta base
            excel_file = importacion.export(data_csv.save_dir, data_csv.period)

        importacion.exit

        # Verificamos que el archivo realmente exista antes de devolverlo
        if excel_file and excel_file.exists():
            return excel_file

        return None

    @property
    def series_by_cost_center(self) -> SeriesByCostCenter:
        window = self._open_system_window(
            "Series por Centro de Costo", pasos_derecha=2, pasos_abajo=1, enter_count=1
        )
        return SeriesByCostCenter(window)

    def download_series(self, save_dir: Path) -> Path:
        file_name = "series.xlsx"
        file = save_dir / file_name
        window = self.series_by_cost_center
        return Path()

    def navegar_menu_sistema(
        self,
        pasos_derecha: int = 5,
        pasos_abajo: int = 0,
        enter_count: int = 2,  # 👈 NUEVO
        reintentos: int = 3,
    ):

        menu_sistema = self._window.MenuBarControl(Name="Sistema")
        if not menu_sistema.Exists(maxSearchSeconds=3):
            return False

        for intento in range(1, reintentos + 1):

            self._window.SetActive()
            self._window.SetTopmost(True)
            sleep(0.3)

            menu_sistema.SetFocus()
            sleep(0.4)

            SendKeys("{Down}")
            sleep(0.4)

            for _ in range(pasos_derecha):
                SendKeys("{Right}")
                sleep(0.3)

            for _ in range(pasos_abajo):
                SendKeys("{Down}")
                sleep(0.3)

            for _ in range(enter_count):  # 👈 CONTROL AQUÍ
                SendKeys("{ENTER}")
                sleep(0.25)

            sleep(1.5)
            return True
        return False

    def _open_system_window(self, window_name: str, **nav_kwargs):
        self.ensure_ready()
        self.navegar_menu_sistema(**nav_kwargs)

        window = self._window.WindowControl(searchDepth=3, Name=window_name)

        if not window.Exists(maxSearchSeconds=15):
            raise TimeoutError(f"No abrió {window_name}")

        return window
