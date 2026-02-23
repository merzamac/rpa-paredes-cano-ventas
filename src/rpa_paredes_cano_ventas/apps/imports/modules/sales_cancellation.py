from uiautomation import WindowControl
from time import sleep
from rpa_paredes_cano_ventas.apps.base import Process

class SalesCancellation(Process):
    def __init__(self,window: WindowControl)-> None:
        super().__init__(window)
    @property
    def cancel(self)->None:
        assert self.buttons_area.Exists(maxSearchSeconds=15)
        cancel_button = self.buttons_area.ButtonControl(searchDepth=1, Name="Cancelar")
        self._wait_until_enabled(cancel_button)
        cancel_button.Click(simulateMove=False)
        sleep(3)
        self._wait_until_enabled(cancel_button)
        sleep(10)
