from uiautomation import WindowControl
from pathlib import Path
from loguru import logger
from time import sleep

class CentroCostos:
    def __init__(self, centro_costos_window: WindowControl):
        self.centro_costos_window: WindowControl = centro_costos_window

    def exportar_centros_costos(self,save_dir:Path, filename: str) -> Path:
        ventana = self.centro_costos_window
        job_area = ventana.GetParentControl()
        window = job_area.GetParentControl()
        
        # Abrir impresión y seleccionar PDF
        panel = ventana.PaneControl(searchDepth=1, ClassName="ImFrame3DWndClass")
        panel.ButtonControl(searchDepth=1, Name="Imprimir").GetInvokePattern().Invoke()
        
        ventana_imprimir = WindowControl(searchDepth=1, Name="Imprimir")
        pdf_list = ventana_imprimir.PaneControl(ClassName="SHELLDLL_DefView").ListControl(Name="Vista de carpetas")
        pdf_list.ListItemControl(searchDepth=1, Name="Microsoft Print to PDF").GetSelectionItemPattern()
        ventana_imprimir.ButtonControl(searchDepth=1, Name="Imprimir").GetInvokePattern().Invoke()
        sleep(10)
        
        ventana.GetWindowPattern().Close()
        
        # Navegar a la ventana de exportación
        ventana_reporte = job_area.WindowControl(searchDepth=1, ClassName="ThunderRT6FormDC")
        barra = ventana_reporte.PaneControl(searchDepth=1, Name="").TextControl(
            searchDepth=1, ClassName="ATL:CrystalReports105.ActiveXReportViewer.1.STATIC"
        ).PaneControl(searchDepth=1, AutomationId="120").ToolBarControl(searchDepth=1, AutomationId="203")
        barra.ButtonControl(searchDepth=1, Name="Exportar informe").GetInvokePattern().Invoke()
        
        # Configurar exportación
        window.WindowControl(searchDepth=1, Name="Export").ButtonControl(searchDepth=1, Name="OK").GetInvokePattern().Invoke()
        window.WindowControl(searchDepth=1, Name="Export Options").ButtonControl(searchDepth=1, Name="OK").GetInvokePattern().Invoke()
        
        # Guardar archivo
        ventana_guardar = window.WindowControl(searchDepth=1, Name="Choose export file")
        file_dir = save_dir.resolve() / f"{filename}.pdf"
        ventana_guardar.PaneControl(searchDepth=1, foundIndex=2).EditControl(searchDepth=2, foundIndex=1).SendKeys(str(file_dir))
        ventana_guardar.ButtonControl(searchDepth=1, Name="Guardar").GetInvokePattern().Invoke()
        
        # Manejar sobreescritura
        dialog = window.WindowControl(searchDepth=1, Name="File already exists")
        if dialog.Exists():
            dialog.ButtonControl(searchDepth=1, Name="Sí").GetInvokePattern().Invoke()
        
        sleep(5)
        ventana_reporte.GetWindowPattern().Close()
        return file_dir