from .append import Append
from .load import Load
from .lookup import Lookup
from .shift_and_swap import ShiftAndSwap
from .totals import Totals
from .validations import Validations


class EnergyBalance(Append, Load, Lookup, ShiftAndSwap, Totals, Validations):
    '''Representation of an Energy Balance as a pandas DataFrame '''

    def __init__(self, eb, year, area):
        self.eb = eb
        self.year = year
        self.area = area

    def rename(self, old_flow_name, new_flow_name):
        '''Rename a flow'''
        self.eb.rename(index={old_flow_name: new_flow_name}, inplace=True)

    def remove(self, flow):
        '''Delete a flow'''
        self.eb.drop(flow, axis='index', inplace=True)

    def to_csv(self, path):
        '''Exports the EB to a csv is a nice human readable format'''
        self.eb.to_csv(path)

    def transform_to_absolute(self):
        self.eb = self.eb.abs()
