from uiautomation import WindowControl
from subprocess import Popen
from pathlib import Path
from typing import Optional

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