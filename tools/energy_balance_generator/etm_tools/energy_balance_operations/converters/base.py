class Converter:
    MARK = 'flexible'

    def __init__(self, energy_balance):
        '''
        Params:
            energy_balance (EnergyBalance): The energy balance to act the conversion out on.
        '''
        self.energy_balance = energy_balance

    @classmethod
    def convert(cls, eb, mark, *args, **kwargs):
        cls.validate(mark)
        return cls(eb).conversion(*args, **kwargs)

    @classmethod
    def validate(cls, mark):
        '''Validates if the selcted converter matches the type of operation'''
        if cls.MARK != 'flexible' and cls.MARK != mark:
            raise InvalidConverterException(
                f'The {cls.__name__} can only be used for {cls.MARK} balances.'
            )

class InvalidConverterException(BaseException):
    pass
