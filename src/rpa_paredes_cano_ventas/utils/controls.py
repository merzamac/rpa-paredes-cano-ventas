from typing import TypeVar

import _ctypes
from uiautomation import Control

TControl = TypeVar("TControl", bound=Control)


def wait_control_exist(
    control: TControl,
) -> None:
    """
    Espera hasta que el control esté disponible.
    Usar el metodo con precaución.

    Args:
        control: Clases derivadas de Control (Control)

    """
    exists: bool = False

    while not exists:
        try:
            exists = control.Exists()
        except (TimeoutError,_ctypes.COMError):
            pass