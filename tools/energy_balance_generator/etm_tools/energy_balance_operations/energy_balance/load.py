from pathlib import Path

import pandas as pd
from etm_tools.utils import EurostatAPI
from etm_tools.energy_balance_operations.input_files import EBConfig

class Load():

    INPUT_PATH = Path('data', 'conversions_input').resolve()

    # Change this one to also import from world format csv
    @classmethod
    def from_csv(cls, path):
        '''Sets up an EnergyBalance from an Eurostat energy balance csv file'''
        frame = pd.read_csv(path, index_col=['FLOWS','PRODUCTS'],
            usecols=['FLOWS', 'PRODUCTS','OBS_VALUE', 'geo', 'TIME_PERIOD'])

        cls.validate_eb(frame)
        area, year = cls.handle_area_and_year(frame)

        frame = frame.reset_index().pivot('FLOWS','PRODUCTS','OBS_VALUE').fillna(0.0)

        return cls(frame, year, area)

    @classmethod
    def from_world_balance_file(cls, area, year, path=''):
        '''Grab country and year from the path or the frame'''
        trnsl = EBConfig.load(eb_type='world', path='config/world.yml')
        path = cls.INPUT_PATH / year / 'raw_world_balances' / f'{area}.csv' if not path else path
        frame = pd.read_csv(path, index_col=0)

        frame.rename(
            columns=trnsl.product_translation(),
            index=trnsl.flow_translation(),
            inplace=True
        )

        frame = frame.reindex(
            columns=trnsl.all('products'),
            index=trnsl.all('flows'),
            fill_value=0.0)

        return cls(frame, year, area)

    @classmethod
    def from_eurostat(cls, country, year, eb_type='energy_balance'):
        '''
        Download an EB file for the given country and year from Eurostat, and
        convert it to an EnergyBalance

        TODO: allow for diiferent cols!!
        '''
        trnsl = EBConfig.load(eb_type=eb_type)

        # Download into dataframe
        frame = pd.read_csv(
            EurostatAPI().get_csv(country, csv_type=eb_type, year=year),
            index_col=['nrg_bal', 'siec'],
            usecols=['nrg_bal', 'siec', 'OBS_VALUE', 'geo', 'TIME_PERIOD'])

        # Remove unwanted countries
        frame = frame[frame['geo']==country]

        # Validation
        cls.validate_eb(frame)
        area, year = cls.handle_area_and_year(frame)

        # Put it the human readable format: pivot into table view, fill in the translations
        frame = frame.reset_index().pivot('nrg_bal','siec','OBS_VALUE').fillna(0.0)
        frame.rename(
            columns=trnsl.product_translation(),
            index=trnsl.flow_translation(),
            inplace=True)
        frame = frame.reindex(
            columns=trnsl.all('products'),
            index=trnsl.all('flows'),
            fill_value=0.0)

        return cls(frame, year, area)

    @staticmethod
    def handle_area_and_year(raw_eb):
        '''Reads area and year from a raw energy balance frame and removes the columns afterwards'''
        area = raw_eb['geo'].unique()[0]
        year = raw_eb['TIME_PERIOD'].unique()[0]
        raw_eb.drop(['geo', 'TIME_PERIOD'], axis='columns', inplace=True)

        return area, year
