'''
Script that retrieves curves data for all EU-27 countries, and combines
them to EU-27 curve, using the relevant respective electricity production as weights.

Writes EU-27 curves to csvs.
'''

import sys
import numpy as np
import pandas as pd
from pathlib import Path
sys.path.append('../supply/script_utils')
sys.path.append('../supply/solar/script/weather_years')

from apis import EtlocalAPI, APIError
from eu_countries import EU27
from process_irradiation_data import normalize

# Some constants and globals

KEYS = [
    'solar_pv',
    'wind_coastal_baseline',
    'wind_onshore_baseline',
    'wind_offshore_baseline'
    ]
YEAR = 2019

etlocal = EtlocalAPI()


def export_data_to_csv(data, name, country, year, curve_type, header=True):
    """
    Export data to output CSV file
    """
    filename = (Path(__file__).resolve().parents[1] / 'supply' / curve_type / 
                'data' / country / year / 'output' / '{}.csv'.format(name))
    filename.parent.mkdir(exist_ok=True, parents=True)
    data.to_csv(filename, index=None, header=header)


def aggregate_curve(country,key):
    '''
    Retrieves curve from ETDataset
    Retrieves corresponding electricity producton from ETLocal
    Multiplies curve with production to obtain hourly electricity production
    Sums and normalizes the EU-27 hourly electricity production
    Returns the processed curve
    '''

    name = country['name']
    code = country['code']
    curve_type = 'wind'
    
    if key == 'solar_pv':
        total_yearly_production = etlocal.get_solar_pv(code)
        curve_type = 'solar'
    elif key == 'wind_coastal_baseline':
        # All yearly production for coastal is 0
        # Solution could be to check the output of the coastal file to see if the data is valid
        # Then rerun this function without multiplying the curve by total_yearly_production
        # Instead, it is simply set to 1.0 for each country here
        # total_yearly_production = etlocal.get_wind_coastal(code)
        total_yearly_production = 1.0
    elif key == 'wind_onshore_baseline':
        total_yearly_production = etlocal.get_wind_onshore(code)
    elif key == 'wind_offshore_baseline':
        total_yearly_production = etlocal.get_wind_offshore(code)

    print(country['code'],total_yearly_production)

    curve = pd.read_csv(f'../supply/{curve_type}/data/{name}/{YEAR}/output/{key}.csv', header=None, squeeze=True)

    return curve * total_yearly_production


for key in KEYS:
    print(key)

    eu27_curve = normalize(sum((aggregate_curve(country,key) for country in EU27)))
    curve_type = 'solar' if key == 'solar_pv' else 'wind'
    export_data_to_csv(eu27_curve, key, 'EU_27', str(YEAR), curve_type, header=False)

    print(eu27_curve.sum())

# TODO: check nl2019
