from .base import Converter

class AppendCHPs(Converter):

    MARK = 'world'

    def conversion(self, chps):
        self.energy_balance.append(chps)
