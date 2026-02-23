from rpa_paredes_cano_ventas.apps.base import BaseLoginWindow
from uiautomation import WindowControl
from rpa_paredes_cano_ventas.apps.aconsys.main_window import AconsyMainWindow

ACONSYS_MAIN_WINDOW = WindowControl(RegexName="ACONSYS")

class AconsyLoginWindow(BaseLoginWindow):
    _window = WindowControl(searchDepth=1, Name="Acceso al Sistema")
    @property
    def _username(self):
        username = self._window.EditControl(searchDepth=3,AutomationId="2")
        assert username.Exists(5)
        return username
    @property
    def _password(self):
        password = self._window.EditControl(searchDepth=3,AutomationId="3")
        assert password.Exists(5)
        return password
    @property
    def _connect(self):
        connect = self._window.ButtonControl(searchDepth=2,Name="Conectar")
        assert connect.Exists(5)
        return connect
    def login(self, user: str, password: str) -> AconsyMainWindow:

        if AconsyMainWindow.exists():
            return AconsyMainWindow()

        self._launch_if_needed()

        self._username.GetValuePattern().SetValue(user)
        self._password.GetValuePattern().SetValue(password)
        self._connect.GetInvokePattern().Invoke()

        if self.exists(timeout=5):
            raise RuntimeError("Credenciales incorrectas.")

        return AconsyMainWindow()