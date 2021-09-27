'''
Normalises the capacity profile to 1/3600 for the first profile is finds
that matches the regions id
'''

import sys
from pathlib import Path

import pandas as pd

DATA_FOLDER = Path(__file__).resolve().parents[1] / 'data'
NORM_TO = 1 / 3600

def normalise_curve(year, country):
    '''Normalises curve to 1/3600'''
    base_folder = DATA_FOLDER / country / year
    # grab first csv with correctish name
    file = next((base_folder / 'input').glob('solar_pv_capacity_*.csv'), None)
    input_curve = pd.read_csv(file, squeeze=True, usecols=lambda x: country in x)

    if not isinstance(input_curve, pd.Series):
        # Use first col if mutliple were returned
        input_curve = input_curve.iloc[:, 0]

    flh = input_curve.sum()

    print('Processing country', country)
    print('FLH: ', flh)

    ((input_curve / flh) * NORM_TO).to_csv(
        base_folder / 'output' / 'solar_pv.csv',
        index=False,
        header=False
    )

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Use: <year> <country1> <country2> ...')
        sys.exit(1)

    year = sys.argv[1]
    countries = sys.argv[2:]

    for country in countries:
        normalise_curve(year, country)
