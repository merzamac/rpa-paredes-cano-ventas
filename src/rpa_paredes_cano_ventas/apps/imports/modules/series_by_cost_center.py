from rpa_paredes_cano_ventas.apps.base import Process


class SeriesByCostCenter(Process):
    def __init__(self, window):
        self.window = window
        self._buttons_area = None
