import pandas as pd
from pathlib import Path

COUNTRY_FOLDER_MAPPING = {
    'AT': 'AT_austria',
    'BE': 'BE_belgium',
    'BG': 'BG_bulgaria',
    'CH': 'CH_switzerland',
    'CY': 'CY_cyprus',
    'CZ': 'CZ_czechia',
    'DE': 'DE_germany',
    'DK': 'DK_denmark',
    'EE': 'EE_estonia',
    'EU27_2020': 'EU27_european_union',
    'ES': 'ES_spain',
    'FI': 'FI_finland',
    'FR': 'FR_france',
    'EL': 'EL_greece',
    'HR': 'HR_croatia',
    'HU': 'HU_hungary',
    'IE': 'IE_ireland',
    'IT': 'IT_italy',
    'LT': 'LT_lithuania',
    'LU': 'LU_luxembourg',
    'LV': 'LV_latvia',
    'MT': 'MT_malta',
    'NL': 'NL_netherlands',
    'NO': 'NO_norway',
    'PL': 'PL_poland',
    'PT': 'PT_portugal',
    'RO': 'RO_romania',
    'RS': 'RS_serbia',
    'SE': 'SE_sweden',
    'SI': 'SI_slovenia',
    'SK': 'SK_slovakia',
    'UK': 'UK_united_kingdom'
}

# Set the path for output data storage
OUTPUT_PATH = Path(__file__).parents[4] / 'data'

class Analyser():
    def __init__(self, country, year, mark):
        '''
        Params:
            country (str): Two-character country code
        '''
        self.country = country
        self.year = year
        self.mark = mark

    def write_to_analysis(self, new_data, analysis_name):
        '''
        Creates a new analysis file if there isn't one yet, and otherwise (re)places the
        country data in the existing analysis file.

        Params:
            new_data (Dict[str, float]): Values for the columns
            anaysis_name (str): Name of the output file
        '''
        path = Analyser.fetch_output_folder_path(self.country, self.year, 'industry') / f'intermediate_{analysis_name}.csv'
        df = pd.DataFrame(new_data, index=[self.country])

        df.to_csv(path)

    @classmethod
    def generate_analyses(cls, country, year, *args, **kwargs):
        output_folder = Analyser.fetch_output_folder_path(country, year, 'industry')
        return cls(country, year, mark=kwargs.get('mark')).generate_analysis(*args, **kwargs, output_folder=output_folder)

    def fetch_output_folder_path(country, year, category):
        '''Returns the output folder for the energy balance data'''
        country_folder = COUNTRY_FOLDER_MAPPING.get(country, country)
        output_folder = OUTPUT_PATH / country_folder / year / category
        output_folder.mkdir(exist_ok=True, parents=True)
        return output_folder
