import pandas as pd
import yaml

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


class InvalidInputFileException(BaseException):
    pass


class Translation():
    '''Translations from and to Eurostat EB codes and (human readable) names'''

    def __init__(self, mapping, eb_type='energy_balance'):
        self.mapping = mapping
        self.eb_type = eb_type

        if not eb_type in mapping:
            raise SystemExit(f'Energy balance type {eb_type} was not found in Eurostat config')


    def product_translation(self, direction='to_name'):
        if direction == 'to_name':
            return self._lookup('products')
        elif direction == 'to_code':
            return dict((v,k) for k,v in self._lookup('products').items())

        return {}


    def flow_translation(self, direction='to_name'):
        if direction == 'to_name':
            return self._lookup('flows')
        elif direction == 'to_code':
            return dict((v,k) for k,v in self._lookup('flows').items())

        return {}


    def unique(self, field='Product', kind='names'):
        '''
        Unique values of a column

        Params:
            field (str): Should be one of: Product, Flows or an extra attribute
            kind (str): Should be one of 'codes', or 'names' (default)
        '''
        if field == 'Product':
            return self._lookup_kind('products', kind)
        elif field == 'Flows':
            return self._lookup_kind('flows', kind)
        elif field in self._lookup('extra_attributes'):
            if kind == 'names':
                field
            return self._lookup('extra_attributes')[field]

        return []


    def unit(self):
        return self._lookup('unit')


    def eurostat_code(self):
        return self._lookup('eurostat_code')


    def unique_extra_attributes(self, kind='names'):
        for field in self._lookup('extra_attributes'):
            yield self.unique(field, kind)


    def _lookup(self, key):
        return self.mapping[self.eb_type].get(key, {})


    def _lookup_kind(self, key, kind):
        if kind == 'names':
            return self._lookup(key).values()

        return self._lookup(key).keys()


    @classmethod
    def load(cls, path='config/eurostat.yml', eb_type='energy_balance'):
        with open(path, 'r') as f:
            doc = yaml.load(f, Loader=yaml.FullLoader)

        return cls(doc, eb_type=eb_type)
