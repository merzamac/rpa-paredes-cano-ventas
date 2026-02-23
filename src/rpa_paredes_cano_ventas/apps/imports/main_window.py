from uiautomation import WindowControl
from datetime import date
from contabot_ventas.apps.base import TopLevelWindow
from contabot_ventas.apps.imports import SalesImports,SalesCancellation
from contabot_ventas.importaciones.utils import navegar_menu_sistema
NOMBRE_MESES = [
    "enero","febrero","marzo","abril","mayo","junio",
    "julio","agosto","septiembre","octubre","noviembre","diciembre"
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

    # def open_menu(self, menu_name: str, option_name: str, pasos_derecha: int):
    #     open_menu_option(self._window, menu_name, option_name, pasos_derecha)

    def _open_system_window(self, window_name: str, **nav_kwargs):
        self.ensure_ready()
        navegar_menu_sistema(self._window, **nav_kwargs)

        window = self._window.WindowControl(
            searchDepth=3,
            Name=window_name
        )

        if not window.Exists(maxSearchSeconds=15):
            raise TimeoutError(f"No abrió {window_name}")

        return window

    @property
    def sales_imports(self):
        window = self._open_system_window(
            "Importación Ventas",
            pasos_derecha=5
        )
        return SalesImports(window)

    @property
    def sales_cancellation(self):
        window = self._open_system_window(
            "Cancelación de Ventas",
            pasos_derecha=5,
            pasos_abajo=1,
            enter_count=1

        )
        return SalesCancellation(window)

