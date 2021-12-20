class Converter:
    def __init__(self, energy_balance):
        '''
        Params:
            energy_balance (EnergyBalance): The energy balance to act the conversion out on.
        '''
        self.energy_balance = energy_balance

    @classmethod
    def convert(cls, eb, *args, **kwargs):
        return cls(eb).conversion(*args, **kwargs)
