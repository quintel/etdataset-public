from .base import Converter

class TurnAllPositive(Converter):
    def conversion(self):
        self.energy_balance.transform_to_absolute()
