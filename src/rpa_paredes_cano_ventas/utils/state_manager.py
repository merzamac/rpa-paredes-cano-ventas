import json
from pathlib import Path
from datetime import date

class StateManager:
    def __init__(self, file_path:Path, period:date):
        self.file_path = file_path
        self.period_date = period.strftime("%Y-%m-%d")
        self.data = {}
        
        self.load_states()
        self._initialize_today()

    def load_states(self):
        if self.file_path.exists():
            try:
                with open(self.file_path, 'r') as f:
                    self.data = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.data = {}
        else:
            self.data = {}

    def save_states(self):
        """Escribe el estado actual y mantiene un máximo de 7 fechas."""
        # Si hay más de 12 fechas, eliminamos las más antiguas
        if len(self.data) > 12:
            # Ordenamos las fechas y tomamos las 12 más recientes
            sorted_dates = sorted(self.data.keys())
            while len(self.data) > 12:
                oldest_date = sorted_dates.pop(0)
                del self.data[oldest_date]
        
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def _initialize_today(self):
        if self.period_date not in self.data:
            self.data[self.period_date] = {
                "first_phase": False,
                "last_phase": False
            }
            self.save_states()

    @property
    def is_first_phase_done(self) -> bool:
        return self.data[self.period_date].get("first_phase", False)

    @property
    def is_last_phase_done(self) -> bool:
        return self.data[self.period_date].get("last_phase", False)

    def first_phase(self):
        self.data[self.period_date]["first_phase"] = True
        self.save_states()

    def last_phase(self):
        self.data[self.period_date]["last_phase"] = True
        self.save_states()