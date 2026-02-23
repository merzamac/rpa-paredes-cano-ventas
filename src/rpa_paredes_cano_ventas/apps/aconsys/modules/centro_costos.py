from uiautomation import WindowControl
from pathlib import Path
from loguru import logger
from time import sleep

class CentroCostos:
    def __init__(self, centro_costos_window: WindowControl):
        self.centro_costos_window: WindowControl = centro_costos_window

    def exportar_centros_costos(self,save_dir:Path, filename: str) -> Path:
        ventana = self.centro_costos_window
        logger.debug(f"dentro de {ventana}")
        job_area = self.centro_costos_window.GetParentControl()
        window = job_area.GetParentControl()
        panel = ventana.PaneControl(searchDepth=1, ClassName="ImFrame3DWndClass")
        logger.debug(f"dentro de {panel}")

        imprimir = panel.ButtonControl(searchDepth=1, Name="Imprimir")
        assert imprimir.GetInvokePattern().Invoke()
        logger.debug(f"click hecho en {imprimir}")

        ventana_imprimir = WindowControl(searchDepth=1, Name="Imprimir")
        logger.debug(f"Dentro de {ventana_imprimir}")

        panel_imprimir = ventana_imprimir.PaneControl(ClassName="SHELLDLL_DefView")
        logger.debug(f"Dentro de {panel_imprimir}")

        pdf_seleccionar = panel_imprimir.ListControl(Name="Vista de carpetas")
        logger.debug(f"Dentro de {pdf_seleccionar}")

        clic_pdf = pdf_seleccionar.ListItemControl(
            searchDepth=1, Name="Microsoft Print to PDF"
        )
        assert clic_pdf.GetSelectionItemPattern()
        logger.debug(f"click hecho en {clic_pdf}")

        clic_pdf_imprimir = ventana_imprimir.ButtonControl(searchDepth=1, Name="Imprimir")
        assert clic_pdf_imprimir.GetInvokePattern().Invoke()
        logger.debug(f"CLick en {clic_pdf_imprimir}")

        sleep(10)

        #ventana_principal = ancestro1.PaneControl(searchDepth=1, Name="Área de trabajo")
        logger.debug(f"dentro de {job_area}")
        ventana.GetWindowPattern().Close()
        ventana = job_area.WindowControl(
            searchDepth=1, ClassName="ThunderRT6FormDC"
        )
        logger.debug(f"dentro de {ventana}")

        ventana_panel = ventana.PaneControl(searchDepth=1, Name="")
        logger.debug(f"dentro de {ventana_panel}")

        barra_principal = ventana_panel.TextControl(
            searchDepth=1, ClassName="ATL:CrystalReports105.ActiveXReportViewer.1.STATIC"
        )
        logger.debug(f"dentro de {barra_principal}")

        barra_oficial = barra_principal.PaneControl(searchDepth=1, AutomationId="120")
        logger.debug(f"dentro de {barra_oficial}")
        # TIENE VARIOS HERMANOS
        barra_herramientas = barra_oficial.ToolBarControl(
            searchDepth=1, AutomationId="203"
        )  # ID PODRIA CAMBIAR
        logger.debug(f"dentro de {barra_herramientas}")

        icono_exportar = barra_herramientas.ButtonControl(
            searchDepth=1, Name="Exportar informe"
        )
        assert icono_exportar.GetInvokePattern().Invoke()
        logger.debug(f"Clic en icono de {icono_exportar}")

        ventana_export = window.WindowControl(searchDepth=1, Name="Export")
        logger.debug(f"dentro de {ventana_export}")

        ok_export = ventana_export.ButtonControl(searchDepth=1, Name="OK")
        assert ok_export.GetInvokePattern().Invoke()
        logger.debug(f"click en  {ok_export}")

        ok_export2 = window.WindowControl(searchDepth=1, Name="Export Options")
        logger.debug(f"dentro de {ok_export2}")

        clic_export2 = ok_export2.ButtonControl(searchDepth=1, Name="OK")
        assert clic_export2.GetInvokePattern().Invoke()
        logger.debug(f"click en {clic_export2}")

        ventana_guardar = window.WindowControl(searchDepth=1, Name="Choose export file")
        logger.debug(f"Dentro de {ventana_guardar}")

        cuadro_nombre_pdf = ventana_guardar.PaneControl(
            searchDepth=1,foundIndex=2
            #Name="RptTablasComunConta.pdf" 
            #AutomationId="1148" NO WORK
            #ClassName="ComboBoxEx32"  NO WORK
        )
        #childre = ventana_guardar.PaneControl(searchDepth=1, foundIndex=2)
        logger.debug(f"dentro de {cuadro_nombre_pdf}")

        # nombre_pdf = cuadro_nombre_pdf.ComboBoxControl(searchDepth=1, Name="Nombre:")
        # logger.debug(f"dentro de {nombre_pdf}")

        rellenar_nombre = cuadro_nombre_pdf.EditControl(searchDepth=2, foundIndex=1)
        file_dir:Path = save_dir.resolve()/f"{filename}.pdf"
        #rellenar_nombre.GetValuePattern().SetValue(str(file))
        rellenar_nombre.SendKeys(str(file_dir))
        logger.debug(f"se escribio dentro de {rellenar_nombre}")

        guardar = ventana_guardar.ButtonControl(searchDepth=1, Name="Guardar")
        assert guardar.GetInvokePattern().Invoke()

        logger.debug(f"se dio clic a {guardar}")

        sleep(5)
        menu_bar = window.MenuBarControl(searchDepth=1, AutomationId="MenuBar")
        logger.debug("Barra de menú encontrada.")

        cerrar_imprimir = menu_bar.ButtonControl(searchDepth=1, Name="Cerrar")
        cerrar_imprimir.DoubleClick()
        print(f"se cerro y se dio clic a {cerrar_imprimir}")
        ventana.GetWindowPattern().Close()

        return file_dir