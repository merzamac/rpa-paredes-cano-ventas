from subprocess import Popen
from pathlib import Path
from typing import Optional
from abc import ABC
from datetime import date
from time import sleep
import _ctypes
from uiautomation import WindowControl,ButtonControl, SendKeys

class BaseWindow:
    """Clase base genérica para ventanas UIAutomation."""

    _window: WindowControl

    @classmethod
    def exists(cls, timeout: int = 0) -> bool:
        return cls._window.Exists(maxSearchSeconds=timeout)

    @classmethod
    def wait_for(cls, timeout: int = 15) -> None:
        if not cls.exists(timeout):
            raise TimeoutError(f"{cls.__name__} no apareció en {timeout}s")

    @classmethod
    def close(cls) -> None:
        if not cls.exists():
            return
        cls._window.GetWindowPattern().Close()

    @classmethod
    def activate(cls) -> None:
        if cls._window.IsOffscreen:
            cls._window.SetTopmost()
            cls._window.SetActive()

    @classmethod
    def ensure_ready(cls, timeout: int = 15) -> None:
        cls.wait_for(timeout)
        cls.activate()


class TopLevelWindow(BaseWindow):
    """Ventana de nivel superior."""

    @classmethod
    def ensure_ready(cls, timeout: int = 15) -> None:
        super().ensure_ready(timeout)
        if not cls._window.IsTopmost():
            cls._window.SetTopmost()


class BaseLoginWindow(TopLevelWindow):
    """Base para ventanas de login con ejecutable."""

    _executable_file: Path
    _popen: Optional[Popen] = None

    def __init__(self, executable_path: Path | str) -> None:
        self._executable_file = Path(executable_path)

        if not self._executable_file.is_file():
            raise ValueError("Ruta al ejecutable inválida.")

    def _launch_if_needed(self) -> None:
        if not self.exists():
            self._popen = Popen(self._executable_file)

        self.ensure_ready()



class Process(ABC):
    """Clase base abstracta para todos los módulos de ventas."""
    
    def __init__(self, window: WindowControl):
        self._window = window
        self._buttons_area = None
    
    @property
    def buttons_area(self) -> ButtonControl:
        """Área de botones común a todos los módulos."""
        if self._buttons_area is None:
            self._buttons_area = self._window.GroupControl(
                searchDepth=1, 
                Name="cnt_principal"
            )
            assert self._buttons_area.Exists(maxSearchSeconds=15)
        return self._buttons_area
    @property
    def window_app(self)->WindowControl:
        window = self._window.GetParentControl()
        assert window.Exists(3)
        return window
    
    def _wait_until_enabled(self, button: ButtonControl) -> None:
        """Espera hasta que un botón esté habilitado."""
        enabled:bool = False
        while not enabled:
            try:
                enabled = button.IsEnabled
            except (TimeoutError, _ctypes.COMError):
                pass
    
    def period(self, period_date: date) -> None:
        """Configura el período en el combo box."""
        format_date = period_date.strftime("%Y%m")
        period_field = self._window.ComboBoxControl(
            searchDepth=1, 
            Name="cmb_PeriodoProceso"
        )
        assert period_field.Exists(maxSearchSeconds=15)
        
        period_field.Click()
        period_field.SetFocus()
        sleep(0.3)
        SendKeys("^a")  # Seleccionar todo
        sleep(0.1)
        SendKeys("{DEL}")
        sleep(0.2)
        SendKeys(format_date)
        sleep(0.2)
        SendKeys("{ENTER}")
        
        assert period_field.GetValuePattern().Value == format_date
    @property
    def exit(self) -> None:
        """Sale del módulo actual."""
        exit_button = self.buttons_area.ButtonControl(searchDepth=3, Name="Salir")
        self._wait_until_enabled(exit_button)
        exit_button.Click(simulateMove=False)
        sleep(5)
        if self._window.Exists():
            exit_button.Click(simulateMove=False)
        assert not self._window.Exists()
    
    def _handle_vfp_dialog(self, action: str = "Sí") -> None:
        """Maneja los diálogos de Microsoft Visual FoxPro."""
        parent = self._window.GetParentControl().GetParentControl()
        dialog = parent.WindowControl(
            searchDepth=1, 
            Name="Microsoft Visual FoxPro"
        )
        assert dialog.Exists(maxSearchSeconds=10)
        accept = dialog.ButtonControl(searchDepth=1,Name=action)
        assert accept.GetInvokePattern().Invoke()
        if dialog.Exists():
            accept.GetInvokePattern().Invoke()