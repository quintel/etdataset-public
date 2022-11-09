import pandas as pd
from pathlib import Path

PATH_TO_DATA_FOLDER = Path(__file__).parents[2] / 'data' / 'source_analyses_output'

class Analyser():
    def __init__(self, country, year):
        '''
        Params:
            country (str): Two-character country code
        '''
        self.country = country
        self.year = year

    def write_to_analysis(self, new_data, analysis_name):
        '''
        Creates a new analysis file if there isn't one yet, and otherwise (re)places the
        country data in the existing analysis file.

        Params:
            new_data (Dict[str, float]): Values for the columns
            anaysis_name (str): Name of the output file
        '''
        path = PATH_TO_DATA_FOLDER / self.year / (analysis_name + '_analysis.csv')

        if path.exists():
            new_row = pd.Series(new_data, name=self.country)
            df = pd.read_csv(path, index_col=0)
            if self.country in df.index:
                df.loc[self.country] = new_row
            else:
                df = df.append(new_row)
        else:
            df = pd.DataFrame(new_data, index=[self.country])

        df.to_csv(path)

    @classmethod
    def generate_analyses(cls, country, year, *args, **kwargs):
        return cls(country, year).generate_analysis(*args, **kwargs)
