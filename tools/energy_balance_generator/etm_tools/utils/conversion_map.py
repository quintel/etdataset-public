import yaml
import pandas as pd

class ConversionMap():
    '''Maps the config files for conversions and source analyses to input parameters'''

    def __init__(self, source='conversions'):
        self.map = self._load(source)
        self.analyses = Analyses()


    def inputs(self, converter, country):
        params = self.map[converter]
        if converter == 'power_plants':
            return {'path': f'data/{params["file"]}.csv'}
        return {param['arg_name']: self.lookup_value(param, country) for param in params}


    def lookup_value(self, param, country):
        if not param['file'] in self.analyses:
            self._add_analysis(param['file'], extended=param['file_type']=='extended')

        return self._get_value(param, country)


    def _get_value(self, param, country):
        return self.analyses.get_value(param['file'], param['field'], country)


    def _add_analysis(self, filename, extended=False):
        try:
            self.analyses.add_by_name(filename, extended=extended)
        except FileNotFoundError as err:
            raise SystemExit(f'Analysis file {filename} was not found') from err


    def _load(self, source):
        with open(f'config/{source}.yml', 'r') as f:
            doc = yaml.load(f, Loader=yaml.FullLoader)

        return doc


class Analysis():
    def __init__(self, name):
        self.name = name
        self.data = self.load()

    def get(self, field, country):
        self.validate(country)

        if field == 'ALL':
            return self.data.loc[country].to_dict()
        if isinstance(field, list):
            return self.data[field][country].to_dict()

        return self.data[field][country]


    def load(self):
        return pd.read_csv(f'data/{self.name}.csv', index_col=0)


    def validate(self, country):
        if not country in self.data.index:
            raise SystemExit(f'Data for {country} was not found in {self.name}')


class SourceAnalysis(Analysis):
    '''Uses a Key column and a value column like the ordinary Source Analysis files'''

    def get(self, field, country, value='Value'):
        self.validate(country)

        if field == 'ALL':
            return self.data.loc[country][value].to_dict()
        if isinstance(field, list):
            return self.data.loc[country].loc[field][value].to_dict()

        return self.data.loc[country, field][value]


    def load(self):
        return pd.read_csv(f'data/{self.name}.csv', index_col=[0,1])


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


    def add_by_name(self, analysis_name, extended=False):
        if extended:
            self.add(SourceAnalysis(analysis_name))
        else:
            self.add(Analysis(analysis_name))
