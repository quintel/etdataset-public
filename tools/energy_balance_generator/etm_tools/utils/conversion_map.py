import yaml
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

class ConversionMap():
    '''Maps the config files for conversions and source analyses to input parameters'''

    def __init__(self, year=2019, source='conversions', mark=None):
        self.year = year
        self.map = self._load(source, mark)
        self.analyses = Analyses()
        self.mark = mark

    def inputs(self, converter, country):
        params = self.map[converter]
        if converter in ['power_plants', 'chps', 'append_world_chps']:
            return {'path': resolve_csv_path(params["file"], self.year, country)}
        return {param['arg_name']: self.lookup_value(param, country) for param in params}

    def lookup_value(self, param, country):
        if param['file'] not in self.analyses:
            file_type = param.get('file_type')
            self._add_analysis(param['file'], country, file_type=file_type)
        return self._get_value(param, country)

    def _get_value(self, param, country):
        return self.analyses.get_value(param['file'], param['field'], country)

    def _add_analysis(self, filename, country, file_type=None):
        try:
            self.analyses.add_by_name(filename, self.year, country, file_type=file_type)
        except FileNotFoundError as err:
            raise SystemExit(f'Analysis file {filename} was not found') from err

    def _load(self, source, mark):
        with open(f'config/{source}.yml', 'r') as f:
            doc = yaml.load(f, Loader=yaml.FullLoader)

            # If the mark is 'world', exclude the specified entries in the 'industry_chemical' section
            if mark == 'world' and 'industry_chemical' in doc:
                # Define the list of arg_names to exclude
                exclude_args = [
                    'shares_chemical_network_gas_non_energetic',
                    'shares_chemical_crude_oil_non_energetic',
                    'shares_chemical_coal_non_energetic'
                ]
                doc['industry_chemical'] = [
                    entry for entry in doc['industry_chemical']
                    if entry['arg_name'] not in exclude_args
                ]

        return doc

def resolve_csv_path(path, year, country):
    components = path.split('/')
    category = components[0]
    filename = components[1]
    country_folder = COUNTRY_FOLDER_MAPPING.get(country)
    if not country_folder:
        raise ValueError(f"Country code {country} not found in COUNTRY_FOLDER_MAPPING")

    base_path = Path(__file__).parents[4] / 'data' / country_folder / str(year) / category
    full_path = base_path / f'{filename}.csv'
    return full_path


class Analysis():
    def __init__(self, name, year, country):
        self.name = name
        self.country = country
        self.data = self.load(year, country)

    def get(self, field, country):
        self.validate(country)
        if field == 'ALL':
            return self.data.loc[country].to_dict()
        if isinstance(field, list):
            return self.data.loc[country, field].to_dict()
        return self.data.loc[country, field]

    def load(self, year, country):
        return pd.read_csv(resolve_csv_path(self.name, year, country), index_col=0)

    def validate(self, country):
        if country not in self.data.index:
            raise SystemExit(f'Data for {country} was not found in {self.name}')


class SourceAnalysis(Analysis):
    '''Handles both multi-country and single-country source analysis files'''

    def load(self, year, country):
        df = pd.read_csv(resolve_csv_path(self.name, year, country))
        if 'Country' in df.columns:
            df.set_index(['Country', 'Key'], inplace=True)
        else:
            df.set_index('Key', inplace=True)
        return df

    def validate(self, country):
        if 'Country' in self.data.index.names:
            if country not in self.data.index.get_level_values('Country'):
                raise SystemExit(f'Data for {country} was not found in {self.name}')
        else:
            # No validation needed for single-country data
            pass

    def get(self, field, country=None, value='Value'):
        if 'Country' in self.data.index.names:
            self.validate(country)
            if field == 'ALL':
                return self.data.loc[country][value].to_dict()
            elif isinstance(field, list):
                return self.data.loc[country].loc[field][value].to_dict()
            else:
                return self.data.loc[(country, field), value]
        else:
            # Single-country data
            if field == 'ALL':
                return self.data[value].to_dict()
            elif isinstance(field, list):
                return self.data.loc[field][value].to_dict()
            else:
                return self.data.loc[field, value]

class Analyses():
    def __init__(self):
        self.collection = {}

    def add(self, analysis):
        self.collection[analysis.name] = analysis

    def __contains__(self, analysis_name):
        return analysis_name in self.collection

    def get(self, analysis_name):
        return self.collection[analysis_name]

    def get_value(self, analysis_name, field, country, **kwargs):
        return self.get(analysis_name).get(field, country, **kwargs)

    def add_by_name(self, analysis_name, year, country, file_type=None):
        if file_type == 'extended':
            self.add(SourceAnalysis(analysis_name, year, country))
        else:
            self.add(Analysis(analysis_name, year, country))
