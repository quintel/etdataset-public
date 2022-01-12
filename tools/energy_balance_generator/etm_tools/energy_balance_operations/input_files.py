import pandas as pd
import yaml

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


def load_heaters_and_chps():
    '''Loads up the heaters and CHPs config file'''
    with open('config/heaters_and_chps.yml', 'r') as f:
        doc = yaml.load(f, Loader=yaml.FullLoader)
    return doc['heaters_and_chps']


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
            return self.mapping[self.eb_type]['products']
        elif direction == 'to_code':
            return dict((v,k) for k,v in self.mapping[self.eb_type]['products'].items())

        return {}


    def flow_translation(self, direction='to_name'):
        if direction == 'to_name':
            return self.mapping[self.eb_type]['flows']
        elif direction == 'to_code':
            return dict((v,k) for k,v in self.mapping[self.eb_type]['flows'].items())

        return {}


    def unique(self, field='Product names'):
        '''
        Unique values of a column

        Params:
            field (str): Should be one of: Product names, Product codes, Flows names,
                         Flows codes
        '''
        if field == 'Product names':
            return self.mapping[self.eb_type]['products'].values()
        elif field == 'Product codes':
            return self.mapping[self.eb_type]['products'].keys()
        elif field == 'Flows names':
            return self.mapping[self.eb_type]['flows'].values()
        elif field == 'Flows codes':
            return self.mapping[self.eb_type]['flows'].keys()

        return []


    def unit(self):
        return self.mapping[self.eb_type]['unit']


    def eurostat_code(self):
        return self.mapping[self.eb_type]['eurostat_code']


    @classmethod
    def load(cls, path='config/eurostat.yml', eb_type='energy_balance'):
        with open(path, 'r') as f:
            doc = yaml.load(f, Loader=yaml.FullLoader)

        return cls(doc, eb_type=eb_type)
