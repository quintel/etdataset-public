class Validations():
    '''Validations and warnings'''

    @staticmethod
    def validate_eb(raw_eb):
        '''Make sure the data is for one year and one area only'''
        Validations.raise_for_not_unique(raw_eb, 'geo')
        Validations.raise_for_not_unique(raw_eb, 'TIME_PERIOD')

    @staticmethod
    def raise_for_not_unique(raw_eb, column):
        if len(raw_eb[column].unique()) > 1:
            raise InvalidEnergyBalanceException(
                f'Column {column} in the Energy Balance must contain the same value for all rows.')

    @staticmethod
    def warn_change(amount_wanted, flow, product, amount_possible):
        print(f'\033[93mCould not move full amount of {amount_wanted} TJ from {flow} {product},',
              f'limiting the shift to {amount_possible} TJ\033[0m')

    @staticmethod
    def warn_swap_overload(max_shift, from_flow, to_flow, from_products, to_products):
         print(f'\033[93mCan only swap {max_shift} TJ from {from_flow} to {to_flow} when',
               f'exchanging {from_products} for {to_products}, limiting the swap\033[0m')

class InvalidEnergyBalanceException(BaseException):
    pass
