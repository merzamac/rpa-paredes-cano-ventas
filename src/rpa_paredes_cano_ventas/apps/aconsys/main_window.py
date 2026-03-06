from rpa_paredes_cano_ventas.apps.base import TopLevelWindow
from uiautomation import WindowControl, SendKeys
from rpa_paredes_cano_ventas.apps.aconsys import CentroCostos, CuentaCorriente
from rpa_paredes_cano_ventas.ocr_processor.parser import DataParser
from rpa_paredes_cano_ventas.ocr_processor import PyOcr, TesseractEngine
from rpa_paredes_cano_ventas.ocr_processor.helpers import img_to_ndarry, take_screenshot
from rpa_paredes_cano_ventas import routes
from PIL.Image import Image
from rpa_paredes_cano_ventas.utils.pdf_reader import pdf_process
from pathlib import Path

# from contabot_ventas.aconsys.views.main.controls import (
#     change_work_period,
#     cuenta_corriente,
#     cuenta_corriente_crear,
#     exportar_centro_costos,
#     exportar_por_cuenta,
#     open_menu_option,
# )
from datetime import date
from time import sleep


class AconsyMainWindow(TopLevelWindow):
    _window = WindowControl(RegexName="ACONSYS")

    def open_menu(self, menu_name: str, option_name: str) -> None:
        pass

    def change_work_period(self, period_date: date):
        """
        Abre 'Configuraciones -> Cambio Periodo de Trabajo' y selecciona el mes actual.
        """
        menu_name = "Configuraciones"
        option_name = "Cambio Periodo de Trabajo	Ctrl+I"

        self._window.SetActive()
        self._window.SetTopmost(True)
        # menu_bar = self._window.MenuBarControl(searchDepth=1, AutomationId="MenuBar")

        # menu_item = menu_bar.MenuItemControl(searchDepth=1, Name=menu_name)
        # assert menu_item.GetInvokePattern().Invoke()

        # tablas_menu = self._window.MenuControl(searchDepth=1, Name=menu_name)

        # option_item = tablas_menu.MenuItemControl(searchDepth=1, Name=option_name)
        # assert option_item.GetInvokePattern().Invoke()
        ventana_mes = self._window.WindowControl(
            searchDepth=1, Name="Cambio de Periodo de Trabajo"
        )
        SendKeys("{Ctrl}i")
        sleep(5)
        if not ventana_mes.Exists():
            raise ValueError('Window "Cambio de Periodo de Trabajo" not found')
        panel_mes = ventana_mes.PaneControl(
            searchDepth=1, ClassName="ImFrame3DWndClass"
        )
        self._window.SetTopmost(True)
        cuadro_mes = panel_mes.GroupControl(searchDepth=1, ClassName="ThunderRT6Frame")

        rellenar_cuadro = cuadro_mes.EditControl(searchDepth=1, AutomationId="3")

        month_work_period = period_date.strftime("%m")
        year_work_period = period_date.strftime("%Y")

        rellenar_cuadro.GetValuePattern().SetValue(month_work_period)

        cuadro_año = cuadro_mes.EditControl(searchDepth=1, AutomationId="2")
        cuadro_año.GetValuePattern().SetValue(year_work_period)
        cuadro_año.SetFocus()
        sleep(0.3)

        SendKeys("{TAB}")
        sleep(0.5)
        SendKeys("{ENTER}")

        aceptar = ventana_mes.WindowControl(searchDepth=1, Name="ACONSYS")
        aceptar_boton = aceptar.ButtonControl(searchDepth=1, Name="Aceptar")
        assert aceptar_boton.GetInvokePattern().Invoke()

    def _open_child_window(self, menu: str, option: str, window_name: str):
        self.ensure_ready()

        window = self._window.WindowControl(Name=window_name)
        if not window.Exists(maxSearchSeconds=15):
            raise TimeoutError(f"No abrió ventana {window_name}")

        return window

    def _open_menu_option(self, menu_name: str, option_name: str) -> None:
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
        centro_costos_window = self._window.WindowControl(
            Name="Mantenimiento de Centro de Costos"
        )
        assert centro_costos_window.Exists(maxSearchSeconds=15)
        return CentroCostos(centro_costos_window)

    @property
    def cuentas_corrientes(self) -> CuentaCorriente:

        toolbar = self._window.PaneControl(
            searchDepth=1, ClassName="ToolbarWndClass"
        ).ToolBarControl(searchDepth=1, ClassName="ToolbarWindow32")

        btn_ctas_ctes = toolbar.ButtonControl(searchDepth=1, Name="Cuentas Corrientes")

        assert btn_ctas_ctes.GetInvokePattern().Invoke(waitTime=15)

        window_cuenta_corriente = self._window.PaneControl(
            searchDepth=1, Name="Área de trabajo"
        ).WindowControl(searchDepth=1, Name="Cuentas Corrientes")
        assert window_cuenta_corriente.Exists(maxSearchSeconds=15)
        return CuentaCorriente(window_cuenta_corriente)

    @property
    def last_account_number(self) -> int:
        """raise error if accounts list is empty"""
        code: str = "0" * 8
        description: str = "TICKETS"
        module_cc: CuentaCorriente = self.cuentas_corrientes

        module_cc.start
        module_cc.clients
        module_cc.provider
        module_cc.account_code(code)
        module_cc.ruc()
        module_cc.description(description)
        module_cc.search
        module_cc.scroll_until_end

        # OCR
        tesseract: TesseractEngine = TesseractEngine(routes.TESSERACT)
        ocr_tool: PyOcr = PyOcr(engine=tesseract)
        screenshot: Image = take_screenshot(module_cc.content)
        raw_text: str = ocr_tool.process(image_source=img_to_ndarry(screenshot))
        accounts: list[str]
        accounts, _ = DataParser.clean_text(raw_text)

        # accounts, companies = DataParser.clean_text(raw_text)
        # accounts_companies = DataParser.format_results(accounts, companies)
        if not accounts:
            raise ValueError("Somethings wrong, not found account numbers")
        last_account_number: int = max((int(acc) for acc in accounts), default=0)

        return last_account_number

    def get_cost_centers(self, save_dir: Path, name: str) -> dict:
        cost_centers = self.centros_de_costos
        file: Path = cost_centers.exportar_centros_costos(save_dir, name)  # type: ignore
        data: dict = pdf_process(file)
        return data

    def register_accounts(self, new_series: list) -> None:
        if not new_series:
            return
        cuentas_corrientes = self.cuentas_corrientes
        cuentas_corrientes.start
        for series in new_series:
            cuentas_corrientes.new_account
            cuentas_corrientes.clients
            cuentas_corrientes.provider
            num = 323
            num += 1
            cuentas_corrientes.account_code(format(num, "011d"))
            # cuentas_corrientes.account_code(series.cuenta_corriente)
            cuentas_corrientes.ruc()
            cuentas_corrientes.description(series.descripcion_cta)
            cuentas_corrientes.document_type("0")
            # cuentas_corrientes.save
