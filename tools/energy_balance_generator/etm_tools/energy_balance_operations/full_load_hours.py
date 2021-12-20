import pandas as pd

class FullLoadHoursCalculator():
    '''Keeps track of powerplants full load hours, and can write the result to csv'''

    TJ_TO_MWH = 277.77777777778

    def __init__(self):
        self.full_load_hours = {}


    def add_plant(self, plant_name, energy_output, capacity):
        '''
        Adds the full load hours of the plant to the log

        Params:
            plant_name (str):      The name of the plant
            energy_output (float): The energy output of the plant in TJ
            capacity (float):      The capacity of the plant in MW

        '''
        self.full_load_hours[plant_name] = self._calculate_flh(energy_output, capacity)


    def _calculate_flh(self, energy_output, capacity):
        '''
        Returns the full load hours of the plant

        Params:
            energy_output (float): The energy output of the plant in TJ
            capacity (float):      The capacity of the plant in MW

        '''
        if not capacity:
            return 0

        return (energy_output * self.TJ_TO_MWH) / capacity


    def to_csv(self, path, country):
        '''
        Update or add the data to the csv specified by the path, if this csv already exists.
        Otherwise create the csv.
        '''
        if path.exists():
            df = pd.read_csv(path, index_col=0)
            df[country] = pd.Series(self.full_load_hours, name=country)
            df.to_csv(path)
        else:
            new_df = pd.Series(self.full_load_hours, name=country)
            new_df.index.name = 'Plant type'
            new_df.to_csv(path)

