import shutil

from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
from pathlib import Path

import pandas as pd

# You should have `pandas` and `openpyxl` installed with pip

POTENCIA_YEAR = 2018
POTENCIA_URL = f'https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/POTEnCIA/Central_{POTENCIA_YEAR}/'

ANALYSIS_YEAR = 2019
COUNTRY_CODES =  ['AT', 'BE', 'BG', 'CY', 'CZ', 'DE', 'DK', 'EE', 'ES', 'FI', 'FR', 'UK', 'EL',
    'HR', 'HU', 'IE', 'IT', 'LT', 'LU', 'LV', 'NL', 'PL', 'PT', 'RO', 'SE', 'SI', 'SK',]

RESIDENTIAL_TAB_KEYS = ['RES_hh_fec', 'RES_se-appl', 'RES_hhdet_fec']
RESIDENTIAL_SHORT = 'RES'

TRANSPORT_TAB_KEYS = ['TRA_Fuels']
TRANSPORT_SHORT = 'TRA'

TERTIARY_TAB_KEYS = ['SER_hh_fec', 'SER_se-appl']
TERTIARY_SHORT = 'SER'

TMP = Path(__file__).parent / 'tmp'
TMP.mkdir(exist_ok=True)

OUTPUT = Path(__file__).parent / 'output' / str(ANALYSIS_YEAR)
OUTPUT.mkdir(exist_ok=True, parents=True)

# SUPPORT ------------------------------------------------------------------------------------------

class Country:
    def __init__(self, name):
        self.name = name


    def annual_reports(self):
        return TMP / self.name / 'Annual_reports'


    def det_yearly_file(self, split):
        if split == 'res':
            folder = 'Residential'
        elif split == 'ser':
            split = 'ter'
            folder = 'Tertiary'
        elif split == 'tra':
            folder = 'Transport'
        else:
            raise ValueError('Only split types res, ter and tra are supported')

        return self.annual_reports() / folder / f'Central_{POTENCIA_YEAR}_{self.name}_{split}_det_yearly.xlsx'


    def extract_potencia_to_tmp(self):
        '''Extract zip contents to tmp folder from the URL'''
        # TODO: Add some try catch stuff to this
        with urlopen(f'{POTENCIA_URL}Central_{POTENCIA_YEAR}_{self.name}.zip') as zipresp:
            with ZipFile(BytesIO(zipresp.read())) as zfile:
                zfile.extractall(TMP)


    def extract_values(self, keys, short):
        '''
        Extract values from a det_yearly excelfile

        Params:
            keys (list[str]): a list of tab keys
            short (str): the short name of the split

        Returns:
            dict[str, pd.Dataframe]: dictionary where the keys are the sheet names
        '''
        return self.__extract_xls(pd.ExcelFile(self.det_yearly_file(short.lower()), engine='openpyxl',), keys)


    def __extract_xls(self, xls, keys):
        '''TODO: See if we need different settings here, like selecting certain columns or indices'''
        return pd.read_excel(xls, sheet_name=keys, index_col=0)


class OutputFile:
    def __init__(self, name):
        self.name = name
        self.frame = None


    def add(self, df):
        '''Merges a dataframe into the file'''
        if self.frame is None:
            self.frame = self.prepare_frame(df)
        else:
            self.frame = pd.concat([self.frame, self.prepare_frame(df)], axis='columns')

    def prepare_frame(self, df):
        country = df.index.name.split(' ')[0]
        df.index.rename(ANALYSIS_YEAR, inplace=True)
        df.rename(columns={ANALYSIS_YEAR: country}, inplace=True)
        return df[country]


    def write(self):
        self.frame.to_csv(OUTPUT / f'{self.name}.csv')


class OutputFileCollection:
    def __init__(self):
        self.files = {}


    def add(self, file):
        self.files[file.name] = file


    def create_files(self, keys):
        '''Create files base on given keys list[str] and short str'''
        for key in keys:
            self.add(OutputFile(key))

    def get(self, filename):
        return self.files.get(filename)


    def write_all(self):
        for _,file in self.files.items():
            file.write()


    def write(self, names):
        '''Writes the files with the given names list[str]'''
        for name in names:
            if not name in self.files:
                print(f'Unknown file: {name}')
                continue
            self.files.get(name).write()


# THE REAL DEAL ------------------------------------------------------------------------------------

# Create a nice new list to hold the countries
countries = [Country(country_name) for country_name in COUNTRY_CODES]

# Extract all downloads!
print('Extracting zips... This may take a while...')
for country in countries:
    print(f'-- Extracting zip for {country.name}')
    country.extract_potencia_to_tmp()


# Set up the output files
output_files = OutputFileCollection()


# Creating the RESIDENCES stuff
print('Merging and writing residential data...')
# Create output files
output_files.create_files(RESIDENTIAL_TAB_KEYS)
# Extract data from all countries
for country in countries:
    dataframes = country.extract_values(RESIDENTIAL_TAB_KEYS, RESIDENTIAL_SHORT)
    for key, df in dataframes.items():
        output_files.get(key).add(df)
# Write csv's
output_files.write_all()


# Creating the TERTIARY stuff
print('Merging and writing tertiary data...')
# Create output files
output_files.create_files(TERTIARY_TAB_KEYS)
# Extract data from all countries
for country in countries:
    dataframes = country.extract_values(TERTIARY_TAB_KEYS, TERTIARY_SHORT)
    for key, df in dataframes.items():
        output_files.get(key).add(df)
# Write csv's
output_files.write(TERTIARY_TAB_KEYS)


# Creating the TRANSPORT stuff
print('Merging and writing transport data...')
# Create output files
output_files.create_files(TRANSPORT_TAB_KEYS)
# Extract data from all countries
for country in countries:
    dataframes = country.extract_values(TRANSPORT_TAB_KEYS, TRANSPORT_SHORT)
    for key, df in dataframes.items():
        output_files.get(key).add(df)
# Write csv's
output_files.write(TRANSPORT_TAB_KEYS)


# Clean up the tmp folder!
shutil.rmtree(TMP)

print('All done!')
