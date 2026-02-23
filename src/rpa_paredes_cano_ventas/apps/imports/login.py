from uiautomation import WindowControl, SendKeys
from contabot_ventas.apps.base  import BaseLoginWindow
from contabot_ventas.apps.imports.main_window import ImportMainWindow
class ImportLoginWindow(BaseLoginWindow):
    _window = WindowControl(searchDepth=1, Name="Módulo Importación")

    def login(self, username: str, password: str) -> ImportMainWindow:

        if ImportMainWindow.exists():
            return ImportMainWindow()

        self._launch_if_needed()
        self.activate()

        SendKeys(username)
        SendKeys("{Tab}")
        SendKeys(password)
        SendKeys("{Enter}")

        if self.exists(timeout=5):
            raise RuntimeError("Credenciales incorrectas.")

        return ImportMainWindow()