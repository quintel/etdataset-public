from pathlib import Path
import io

import pandas as pd
from etm_tools.utils import EurostatAPI
from etm_tools.energy_balance_operations.input_files import EBConfig

class Load():

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
    def from_eurostat(cls, country, year, eb_type='energy_balance', save_raw=True, output_folder=None):
        '''
        Download an EB file for the given country and year from Eurostat, save the raw data,
        and convert it to an EnergyBalance if necessary.
        '''
        trnsl = EBConfig.load(eb_type=eb_type)

        # Step 1: Download data from Eurostat into a DataFrame
        raw_csv_io = EurostatAPI().get_csv(country, csv_type=eb_type, year=year)

        frame = pd.read_csv(raw_csv_io, index_col=['nrg_bal', 'siec'], usecols=['nrg_bal', 'siec', 'OBS_VALUE', 'geo', 'TIME_PERIOD'])
        frame = frame[frame['geo'] == country]  # Filter by country
        cls.validate_eb(frame)
        area, year = cls.handle_area_and_year(frame)

        # Transform data into human-readable format (pivot, rename, reindex)
        frame = frame.reset_index().pivot('nrg_bal', 'siec', 'OBS_VALUE').fillna(0.0)
        frame.rename(columns=trnsl.product_translation(), index=trnsl.flow_translation(), inplace=True)
        frame = frame.reindex(columns=trnsl.all('products'), index=trnsl.all('flows'), fill_value=0.0)

        # Step 2: Save the raw CSV before applying any transformations
        if save_raw and eb_type == 'energy_balance':
            if output_folder is None:
                # Use a default path if none provided
                output_folder = Path(__file__).parents[4] / 'data'
                print("Using default output folder as from_eurostat was called without a valid output_folder argument.")

            output_folder = Path(output_folder)
            raw_path = output_folder / f'intermediate_energy_balance_raw.csv'
            frame.to_csv(raw_path)

        return cls(frame, year, area)

    @classmethod
    def load_raw_csv(cls, country, year, input_folder=None):
        '''
        Load a raw CSV file saved from Eurostat before any transformations were applied.
        '''
        if input_folder is None:
            print(f"Raw data for {country} in {year} not found. Input folder not provided.")
            return None

        raw_path = input_folder / f'intermediate_energy_balance_raw.csv'
        if not raw_path.exists():
            raise FileNotFoundError(f"Raw data for {country} in {year} not found at {raw_path}.")

        frame = pd.read_csv(raw_path)
        frame.set_index('nrg_bal', inplace=True)
        return cls(frame, year, area=country)

    @staticmethod
    def handle_area_and_year(raw_eb):
        '''Reads area and year from a raw energy balance frame and removes the columns afterwards'''
        area = raw_eb['geo'].unique()[0]
        year = raw_eb['TIME_PERIOD'].unique()[0]
        raw_eb.drop(['geo', 'TIME_PERIOD'], axis='columns', inplace=True)

        return area, year

    @classmethod
    def load_df(cls, frame, country, year):
        return cls(frame, country, year)
