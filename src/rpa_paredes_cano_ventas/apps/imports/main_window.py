from uiautomation import WindowControl,SendKeys
from datetime import date
from rpa_paredes_cano_ventas.apps.base import TopLevelWindow
from rpa_paredes_cano_ventas.apps.imports import SalesImports,SalesCancellation
# from contabot_ventas.importaciones.utils import navegar_menu_sistema
from time import sleep
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
    
    def navegar_menu_sistema(self,
    pasos_derecha: int = 5,
    pasos_abajo: int = 0,
    enter_count: int = 2,   # 👈 NUEVO
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

            for _ in range(enter_count):      # 👈 CONTROL AQUÍ
                SendKeys("{ENTER}")
                sleep(0.25)


            sleep(1.5)
            return True
        return False

    def _open_system_window(self, window_name: str, **nav_kwargs):
        self.ensure_ready()
        self.navegar_menu_sistema(**nav_kwargs)

        window = self._window.WindowControl(
            searchDepth=3,
            Name=window_name
        )

        if not window.Exists(maxSearchSeconds=15):
            raise TimeoutError(f"No abrió {window_name}")

        return window

