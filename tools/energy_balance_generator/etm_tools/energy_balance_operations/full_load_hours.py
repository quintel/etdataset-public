import pandas as pd

class FullLoadHoursCalculator():
    '''Keeps track of powerplants full load hours, and can write the result to csv'''

    TJ_TO_MWH = 277.77777777778

    def __init__(self):
        self.full_load_hours = {}


    def add_plant(self, plant_name, energy_output, capacity):
        '''
        Adds the full load hours of the plant to the log. If the calculated FLH
        are over 8760, the FLH will be corrected to 8000.

        Params:
            plant_name (str):      The name of the plant
            energy_output (float): The energy output of the plant in TJ
            capacity (float):      The capacity of the plant in MW

        '''
        try:
            self.full_load_hours[plant_name] = self._calculate_flh(energy_output, capacity)
        except FLHOverloadError as err:
            self.full_load_hours[plant_name] = 8000
            FullLoadHoursCalculator.warn_overload(plant_name, err.flh)


    def add_plant_with_flh(self, plant_name, flh):
        '''Adds pre-calculated full load hours of the plant to the log'''
        self.full_load_hours[plant_name] = flh


    def add_copy(self, new_plant_name, original_plant_name):
        '''
        Adds a copy of the plant to the table.
        Ignores plants that don't exist.

        Params:
            new_plant_name (str):       The name of the new plant
            original_plant_name (str):  The name of the plant that should be copied

        '''
        try:
            self.full_load_hours[new_plant_name] = self.full_load_hours[original_plant_name]
        except KeyError:
            pass

    def remove(self, plant_name):
        '''
        Removes the plant from the table.

        If the plant did not exist, nothing happens.
        '''
        self.full_load_hours.pop(plant_name, None)


    def _calculate_flh(self, energy_output, capacity):
        '''
        Returns the full load hours of the plant

        Params:
            energy_output (float): The energy output of the plant in TJ
            capacity (float):      The capacity of the plant in MW

        '''
        if not capacity:
            return 0

        flh = (energy_output * self.TJ_TO_MWH) / capacity
        if flh < 8760:
            return flh

        raise FLHOverloadError(flh)


    def to_csv(self, path, country):
        '''
        Update or add the data to the csv specified by the path, if this csv already exists.
        Otherwise create the csv.
        '''
        # TODO: add new plant types to existing CSV!
        if path.exists():
            df = pd.read_csv(path, index_col=0)
            df[country] = pd.Series(self.full_load_hours, name=country)
            df.to_csv(path)
        else:
            new_df = pd.Series(self.full_load_hours, name=country)
            new_df.index.name = 'Plant type'
            new_df.to_csv(path)


    @staticmethod
    def warn_overload(plant_name, hours):
        print(f'\033[93mFLH Warning: {plant_name}: Based on estimated capacity',
            f'and produced energy FLH will be {hours}, correcting to 8000\033[0m')


class FLHOverloadError(BaseException):
    def __init__(self, flh, *args):
        super().__init__(*args)
        self.flh = flh
