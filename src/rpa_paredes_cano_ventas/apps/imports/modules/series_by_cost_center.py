from rpa_paredes_cano_ventas.apps.base import Process
from time import sleep


class SeriesByCostCenter(Process):
    def __init__(self, window):
        super().__init__(window=window)
    
    @property
    def importar(self)->None:
        assert self.buttons_area.Exists(maxSearchSeconds=15)
        import_button = self.buttons_area.ButtonControl(searchDepth=1, Name="Importar")
        self._wait_until_enabled(import_button)
        import_button.Click(simulateMove=False)
        sleep(3)
        self._wait_until_enabled(import_button)
        sleep(10)
    
