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

from apis import EtlocalAPI, APIError
from eu_countries import EU27

# Some constants and globals

KEYS = [
    'solar_pv',
    'solar_thermal',
    'wind_coastal_baseline',
    'wind_inland_baseline',
    'wind_offshore_baseline'
    ]
YEAR = 2019
TJ_PER_MWH = 0.0036

etlocal = EtlocalAPI()

def aggregate_flhs(country,key):
    '''
    Retrieves curve from ETDataset
    Retrieves corresponding electricity producton from ETLocal
    Multiplies curve with production to obtain hourly electricity production
    Sums and normalizes the EU-27 hourly electricity production
    Returns the processed curve
    '''

    name = country['name']
    code = country['code']

    if key == 'solar_pv':
        total_yearly_production, flh = etlocal.get_solar_pv(code, get_flh=True)
    if key == 'solar_thermal':
        total_yearly_production, flh = etlocal.get_solar_thermal(code, get_flh=True)
    elif key == 'wind_coastal_baseline':
         # All yearly production for coastal is 0
         # Solution could be to check the output of the coastal file to see if the data is valid
         # Then rerun this function without multiplying the curve by total_yearly_production
         # Instead, it is simply set to 1.0 for each country here
        total_yearly_production, flh = etlocal.get_wind_coastal(code, get_flh=True)
        total_yearly_production = 1.0
    elif key == 'wind_inland_baseline':
        total_yearly_production, flh = etlocal.get_wind_onshore(code, get_flh=True)
    elif key == 'wind_offshore_baseline':
        total_yearly_production, flh = etlocal.get_wind_offshore(code, get_flh=True)

    #print(country['code'],total_yearly_production,flh)

    total_yearly_production = total_yearly_production / TJ_PER_MWH

    return total_yearly_production / flh, total_yearly_production


for key in KEYS:

    total_installed_capacity = 0
    total_yearly_production = 0
    for installed_capacity, yearly_production in (aggregate_flhs(country,key) for country in EU27):
        total_installed_capacity += installed_capacity
        total_yearly_production += yearly_production

    total_flh = total_yearly_production/total_installed_capacity

    print(key,total_flh)


# TODO: check nl2019
