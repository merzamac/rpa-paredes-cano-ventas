from datetime import datetime
from pathlib import Path
from time import sleep

from psutil import Process
from uiautomation import ButtonControl, GroupControl, ProgressBarControl, WindowControl
from .file_explorer import FileExplorerWindow


class ExcelManager:
    def __init__(self, excel_window_control: WindowControl) -> None:
        self.excel_window_control = excel_window_control
        self.excel_window_control.SetTopmost(True)

    def _dialog_panel_enable(self, title: str) -> bool:

        return self.excel_window_control.PaneControl(
            ClassName=title, searchDepth=1
        ).Exists()

    def _cerrar_dialog_asistencia_activacion(self) -> None:

        cerrar_button: ButtonControl = (
            self.excel_window_control.PaneControl(ClassName="NUIDialog", searchDepth=1)
            .TitleBarControl(searchDepth=1)
            .ButtonControl()
        )
        cerrar_button.GetInvokePattern().Invoke()

    def start(self) -> None:
        """Ubica la ventana a la vista"""
        if self._dialog_panel_enable("NUIDialog"):
            self._cerrar_dialog_asistencia_activacion()

        # if not self.excel_window_control.IsMaximize():
        #     self.excel_window_control.Maximize()
        # if not self.excel_window_control.IsTopmost():
        #    self.excel_window_control.Maximize()

    def save(self, save_dir: Path, name: str) -> Path:
        file_name: str = f"{name}.xlsx"

        self.excel_window_control.SetFocus()
        self.excel_window_control.SendKeys("{F12}")
        # sleep(1)
        save_as: WindowControl = self.excel_window_control.WindowControl(
            Name="Guardar como", searchDepth=1
        )

        file_explorer_window: FileExplorerWindow = FileExplorerWindow(save_as)
        file = file_explorer_window.save_as(save_dir, file_name)

        return file

    def close(self) -> None:

        self.excel_window_control.SetFocus()
        sleep(0.5)
        self.excel_window_control.GetWindowPattern().Close()