import pandas as pd
import yaml

from .translations import flow_translations, product_translations
from .plant import Producer

POWERPLANT_COLUMNS = ['input', 'output', 'input_share', 'output_share', 'code',
    'net_max_generating_capacity_MW']


def load_powerplants(path):
    '''
    Returns a pd.Dataframe from a powerplants input file.
    Validates the file before returning.
    '''
    powerplants = pd.read_csv(path, index_col=0, header=[0,1])

    # ensure_correct_columns(powerplants, POWERPLANT_COLUMNS)
    validate_shares(powerplants)

    return powerplants


def ensure_correct_columns(df, columns):
    if not all((column in df.columns for column in columns)):
        raise InvalidInputFileException(f'File must contain all following columns: {columns}')


def validate_shares(df):
    '''
    Validates that the input shares per (input, output) type add up to 1.0.
    Idem for output shares.
    '''
    grouped = df.reset_index().set_index([('input', 'input'), ('output', 'output')])
    countries = [c for c in grouped.columns.get_level_values(1) if c and not c.startswith('Unnamed')]
    for group, values in grouped.groupby([('input', 'input'), ('output', 'output')]):
        for country in countries:
            if not abs(values[('output_share', country)].sum() - 1) < 0.00001:
                raise InvalidInputFileException(f"Powerplants: Output shares of {country} {group} don't sum to 1")
            if not abs(values[('input_share', country)].sum() - 1) < 0.00001:
                raise InvalidInputFileException(f"Powerplants: Input shares of {country} {group} don't sum to 1")


def load_heaters():
    '''Loads up the heaters and CHPs config file'''
    with open('config/heaters.yml', 'r') as f:
        doc = yaml.load(f, Loader=yaml.FullLoader)
    return [Producer.from_dict(producer) for producer in doc['heaters']]


def load_chp_efficiencies(path):
    '''
    Returns a pd.Dataframe from a chp_efficiencies input file.
    Validates the file before returning.
    '''

    return pd.read_csv(path, index_col=['Gen Tech', 'Network'])

def load_world_chps(path):
    '''
    Returns a pd.Dataframe from a world_chp input file.
    '''
    return pd.read_csv(path, index_col=0)

class InvalidInputFileException(BaseException):
    pass


class EBConfig():
    '''Interface with the EB config files from the config folder'''

    def __init__(self, mapping, eb_type='energy_balance'):
        self.mapping = mapping
        self.eb_type = eb_type

        if not eb_type in mapping:
            raise SystemExit(f'Energy balance type {eb_type} was not found in Eurostat config')

    def product_translation(self) -> dict:
        '''Translate from codes to human readable names. Returns a dict'''
        try:
            return self._translate_products()
        except KeyError as err:
            self.raise_lost_translation_from_err(err)

    def _translate_products(self):
        if self.eb_type == 'world':
            return product_translations.translate_to('world_label')

        # Filter out missing europe_labels
        valid_labels = [label for label in self.all('europe_label') if pd.notna(label)]
        return product_translations.translate_to('europe_code', filters=valid_labels)

    def flow_translation(self) -> dict:
        '''Translate from codes to human readable names. Returns a dict'''
        try:
            return self._translate_flows()
        except KeyError as err:
            self.raise_lost_translation_from_err(err)

    def _translate_flows(self):
        if self.eb_type == 'world':
            return flow_translations.translate_to('world_label')

        # Filter out missing europe_labels
        valid_labels = [label for label in self.all('europe_label') if pd.notna(label)]
        return flow_translations.translate_to('europe_code', filters=valid_labels)

    def all(self, field='products'):
        '''
        All values of a column

        Params:
            field (str): Should be one of: products, flows or an extra attribute
        '''
        if field in self._lookup('extra_attributes'):
            return self._lookup('extra_attributes')[field]

        return self._lookup(field)

    def all_codes(self, field='products'):
        if field == 'flows':
            return self.flow_translation().keys()

        return self.product_translation().keys()

    def unit(self):
        return self._lookup('unit')

    def europe_code(self):
        return self._lookup('europe_code')

    def unique_extra_attributes(self):
        for field in self._lookup('extra_attributes'):
            yield self._lookup('extra_attributes')[field]

    def _lookup(self, key):
        return self.mapping[self.eb_type].get(key, {})

    @classmethod
    def load(cls, path='config/eurostat.yml', eb_type='energy_balance'):
        with open(path, 'r') as f:
            doc = yaml.load(f, Loader=yaml.FullLoader)

        return cls(doc, eb_type=eb_type)

    @staticmethod
    def raise_lost_translation_from_err(err):
        if str(err).startswith("\"["):
            missing_key = str(err)[1:-14]
        else:
            missing_key = str(err)[16:-60]
        raise InvalidInputFileException(
            f'The following codes are missing a translation: {missing_key}'
        ) from err
