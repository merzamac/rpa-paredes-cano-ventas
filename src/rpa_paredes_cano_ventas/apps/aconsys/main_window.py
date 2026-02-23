from rpa_paredes_cano_ventas.apps.base import TopLevelWindow
from uiautomation import WindowControl
from rpa_paredes_cano_ventas.apps.aconsys import CentroCostos,CuentaCorriente
# from contabot_ventas.aconsys.views.main.controls import (
#     change_work_period,
#     cuenta_corriente,
#     cuenta_corriente_crear,
#     exportar_centro_costos,
#     exportar_por_cuenta,
#     open_menu_option,
# )
class AconsyMainWindow(TopLevelWindow):
    _window = WindowControl(RegexName="ACONSYS")

    def open_menu(self, menu_name: str, option_name: str) -> None:
        pass

    def change_work_period(self, period_date):
        pass

    def _open_child_window(self, menu: str, option: str, window_name: str):
        self.ensure_ready()
       

        window = self._window.WindowControl(Name=window_name)
        if not window.Exists(maxSearchSeconds=15):
            raise TimeoutError(f"No abrió ventana {window_name}")

        return window
    def _open_menu_option(self, menu_name: str, option_name: str
    ) -> None:
        """
        Abre una opción de menú (ej. 'Tablas' - 'Centro de Costos') desde la ventana principal.
        Funciona para menús clásicos de ACONSYS.
        """

        self._window.SetActive()
        self._window.SetTopmost(True)

        menu_bar = self._window.MenuBarControl(searchDepth=1, AutomationId="MenuBar")

        menu_item = menu_bar.MenuItemControl(searchDepth=1, Name=menu_name)
        assert menu_item.GetInvokePattern().Invoke()

        tablas_menu = self._window.MenuControl(searchDepth=1, Name=menu_name)

        option_item = tablas_menu.MenuItemControl(searchDepth=1, Name=option_name)
        assert option_item.GetInvokePattern().Invoke()

    @property
    def centros_de_costos(self) -> CentroCostos:
        menu_name: str = "Tablas"
        option_name: str = "Centro de Costos"
        self._open_menu_option(menu_name, option_name)
        centro_costos_window = self._window.WindowControl(Name="Mantenimiento de Centro de Costos")
        assert centro_costos_window.Exists(maxSearchSeconds=15)
        return CentroCostos(centro_costos_window)
    @property
    def cuentas_corrientes(self)->CuentaCorriente:
        
        cuenta_corriente_menu = self._window.PaneControl(
            searchDepth=1, ClassName="ToolbarWndClass"
        )

        opcion_cuenta_corriente = cuenta_corriente_menu.ToolBarControl(
            searchDepth=1, ClassName="ToolbarWindow32"
        )

        boton_cuenta_corriente = opcion_cuenta_corriente.ButtonControl(
            searchDepth=1, Name="Cuentas Corrientes"
        )
        
        assert boton_cuenta_corriente.GetInvokePattern().Invoke(waitTime=15)
        

        panel_cuenta_corriente = self._window.PaneControl(searchDepth=1, Name="Área de trabajo")
        

        ventana_cuenta_corriente = panel_cuenta_corriente.WindowControl(
            searchDepth=1, Name="Cuentas Corrientes"
        )
        assert ventana_cuenta_corriente.Exists(maxSearchSeconds=15)
        return CuentaCorriente(ventana_cuenta_corriente)