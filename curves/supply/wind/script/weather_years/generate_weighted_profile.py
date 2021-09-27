'''
Script that retrieves irridiation data for all municipalities, and combines it
to an NL curve, using their respective installed PV as weigths.

Writes irridiation data and curves for all municpaities to csvs.
Writes aggregated irridiation curve for NL to csv.
'''

import sys
import pandas as pd
import numpy as np
sys.path.append('../../../script_utils')

from apis import WeatherXAPI, EtlocalAPI, APIError
from config.municipality_coordinates import MUNICIPALITIES
from generate_wind_curves_weather_years import (
    calculate_wind_at_hub_height, smooth_curve_with_moving_average, calculate_output_power
)

YEAR = 2019

# Some constants and globals
MOVING_AVERAGES = 4
WIND_TURBINE = {'cut_in_wind_speed': 3.5, 'rated_output_wind_speed': 13, 'cut_off_wind_speed': 25}
CONVERSION_HUB_HEIGHTS = {
    'inland': {'measurement_height': 10, 'hub_height': 80, 'roughness_factor': 0.143},
    'coastal': {'measurement_height': 10, 'hub_height': 80, 'roughness_factor': 0.143},
    'offshore': {'measurement_height': 10, 'hub_height': 80, 'roughness_factor': 0.07}
}

# API's
api = WeatherXAPI(f'{YEAR}-01-01 00:00',f'{YEAR}-12-31 23:59')
etlocal = EtlocalAPI()
logger = {}
flh = {'coastal': {'total_flh': 0.0, 'total_weight': 0.0}, 'inland' : {'total_flh': 0.0, 'total_weight': 0.0}}

def export_data_to_csv(curve, wind_type, country, year, subtitle, subfolder, header=True):
    curve.to_csv(
        f"../../data/{country}/{year}/{subfolder}/wind_{wind_type}_{subtitle}.csv",
        header=header,
        index=None
    )

def normalise(curve):
    return curve / sum(curve) / 3600.0

def ffill_cols(a, startfillval=0):
    '''https://stackoverflow.com/questions/62038693/numpy-fill-nan-with-values-from-previous-row'''
    mask = np.isnan(a)
    tmp = a[0].copy()
    a[0][mask[0]] = startfillval
    mask[0] = False
    idx = np.where(~mask,np.arange(mask.shape[0])[:,None],0)
    out = np.take_along_axis(a,np.maximum.accumulate(idx,axis=0),axis=0)
    a[0] = tmp
    print(out)
    print(a)
    return out

def print_info(print_name, turbine_type, installed, flh_message, warning=False):
    print(print_name, f'({turbine_type})')
    print('-   weight: ', installed)
    if warning:
        print(f"\033[93m-   No FLH could be determined: {flh_message}\033[0m")
        print('\033[93m-   Skipping...\033[0m')
        logger[print_name] = installed
    else:
        print('-   FLH (not normalised): ', flh_message)
        print(f'-   Normalising and multiplying with weight {installed}')

def get_smooth_curve(wind_speed_curve, turbine_type, print_name, installed):
    ''' Smoothes and normalises the wind speed curve and prints some info, saves the curve to csv'''

    # Fill up any gaps with data from the previous day if > 2% missing
    missing = wind_speed_curve.isna().sum()
    if missing > 180:
        print_info(print_name, turbine_type, installed, f'{missing} datapoints missing', True)
        return np.zeros(8760)
    elif missing:
        wind_speed_curve = np.reshape(ffill_cols(np.reshape(wind_speed_curve, (-1, 24))), 8760)

    wind_at_hub_height = calculate_wind_at_hub_height(
        CONVERSION_HUB_HEIGHTS,
        turbine_type,
        wind_speed_curve
    ).apply(lambda x: calculate_output_power(WIND_TURBINE, x))

    smooth_wind = smooth_curve_with_moving_average(MOVING_AVERAGES, wind_at_hub_height)

    flh_from_curve = round(sum(np.array(smooth_wind)), 1)
    print_info(print_name, turbine_type, installed, flh_from_curve)

    flh[turbine_type]['total_flh'] += flh_from_curve * installed
    flh[turbine_type]['total_weight'] += installed

    curve = normalise(smooth_wind)

    # Save the municipality profile
    # export_data_to_csv(
    #     pd.Series(curve), turbine_type, 'nl', str(YEAR), print_name, 'output', header=False
    # )

    return curve

def processed_curves(municipality):
    '''
    Retrieves weather data from the API and fashions a curve from it
    Writes input and outputs files for the municupality
    Returns the processed curves (Arrays), for inland and coastal
    '''
    wind_installed = etlocal.get_wind_production(municipality['name'])

    try:
        dataframe = api.get_dataframe(municipality['lat'], municipality['lon'], ['WIND'])
    except APIError as exc:
        print_info(municipality['name'], 'all types', wind_installed, exc, True)
        return np.zeros(8760), np.zeros(8760)

    # Make it pretty and record dataframe with municipality wind data
    # dataframe.drop(['lat', 'lon'], 'columns', inplace=True)
    # dataframe.insert(0, 'municipality', municipality['name'])
    # export_data_to_csv(dataframe, 'measurements', 'nl', str(YEAR), municipality['name'], 'input')

    # FH: uurgemiddelde windsnelheid (in 0.1 m/s) -> convert to m/s
    wind_speed_curve = dataframe['FH'] / 10.0

    inland_curve = get_smooth_curve(
        wind_speed_curve, 'inland', municipality['name'], wind_installed
    )

    if municipality['has_water']:
        coastal_curve = get_smooth_curve(
            wind_speed_curve, 'coastal', municipality['name'], wind_installed
        )
    else:
        coastal_curve = np.zeros(8760) # empty curve

    return inland_curve * wind_installed, coastal_curve * wind_installed


# Aggregating and normailising the curve
curve_generator = (processed_curves(muni) for muni in MUNICIPALITIES)
nl_inland_curve = np.zeros(8760)
nl_coastal_curve = np.zeros(8760)
for inland, coastal in curve_generator:
    nl_inland_curve += inland
    nl_coastal_curve += coastal

export_data_to_csv(
    pd.Series(normalise(nl_inland_curve)),
    'inland', 'nl', str(YEAR), 'weighted_nl', 'output', header=False
)
export_data_to_csv(
    pd.Series(normalise(nl_coastal_curve)),
    'coastal', 'nl', str(YEAR), 'weighted_nl', 'output', header=False
)

print('')
print('=============== DONE ==================')
print('Exported weighted curves to data folder.')
print('')
print(f'Skipped {len(logger.keys())} municiplities, with a total weight of {sum(logger.values())}.')
if logger:
    print('')
    print('Affected municipalities:')
    print(logger)

print('')
print('Average FLH were:')
print(f"-   inland: {flh['inland']['total_flh']/flh['inland']['total_weight']}")
print(f"-   coastal: {flh['coastal']['total_flh']/flh['coastal']['total_weight']}")


