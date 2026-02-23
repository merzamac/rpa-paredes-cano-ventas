from pathlib import Path

from uiautomation import ButtonControl, GroupControl, ProgressBarControl, WindowControl
from uiautomation.uiautomation import ComboBoxControl


class FileExplorerWindow:
    def __init__(self, file_explorer_window: WindowControl) -> None:
        self.file_explorer_window: WindowControl = file_explorer_window

    def load_files(self, parent_dir: Path, file_names: tuple[str, ...]) -> None:
        parent: str = str(parent_dir.resolve())
        progress_bar_control: ProgressBarControl = (
            self.file_explorer_window.PaneControl(foundIndex=3, searchDepth=1)
            .PaneControl(searchDepth=1)
            .PaneControl(foundIndex=3, searchDepth=1)
            .ProgressBarControl(searchDepth=1)
        )

        progress_bar_control.ToolBarControl(
            Name="Barra de herramientas de área de dirección", searchDepth=1
        ).ButtonControl(
            Name="Ubicaciones anteriores", searchDepth=1
        ).GetInvokePattern().Invoke()

        progress_bar_control.PaneControl(searchDepth=1).ComboBoxControl(
            Name="Dirección", searchDepth=1
        ).EditControl(Name="Dirección", searchDepth=1).SendKeys(parent + "{ENTER}")

        self.file_explorer_window.PaneControl(
            searchDepth=1, foundIndex=2
        ).ComboBoxControl(Name="Nombre:", searchDepth=1).EditControl(
            Name="Nombre:", searchDepth=1
        ).SendKeys(
            " ".join(f'"{name}"' for name in file_names)
        )
        self.file_explorer_window.ButtonControl(
            Name="Abrir", searchDepth=1
        ).GetInvokePattern().Invoke()

    def save_as(self, parent_dir: Path, file_name: str) -> None:
        parent: str = str(parent_dir.resolve())
        progress_bar_control: ProgressBarControl = (
            self.file_explorer_window.PaneControl(searchDepth=1, foundIndex=2)
            .PaneControl(searchDepth=1)
            .PaneControl(searchDepth=1, foundIndex=3)
            .ProgressBarControl(searchDepth=1)
        )
        progress_bar_control.ToolBarControl(
            Name="Barra de herramientas de área de dirección", searchDepth=1
        ).ButtonControl(
            Name="Ubicaciones anteriores", searchDepth=1
        ).GetInvokePattern().Invoke()

        progress_bar_control.PaneControl(searchDepth=1).ComboBoxControl(
            Name="Dirección", searchDepth=1
        ).EditControl(Name="Dirección", searchDepth=1).SendKeys(parent + "{ENTER}")
        box_file_name: ComboBoxControl = (
            self.file_explorer_window.PaneControl(searchDepth=1, foundIndex=1)
            .PaneControl(searchDepth=1)
            .PaneControl(searchDepth=1, foundIndex=6)
            .PaneControl(searchDepth=1, foundIndex=3)
            .ComboBoxControl(searchDepth=1, foundIndex=1)
        )
        box_file_name.ButtonControl().GetInvokePattern().Invoke()
        box_file_name.EditControl().SendKeys(file_name)
        self.file_explorer_window.ButtonControl(
            Name="Guardar", searchDepth=1
        ).GetInvokePattern().Invoke()