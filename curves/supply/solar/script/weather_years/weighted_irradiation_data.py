'''
Script that retrieves irradiation data for all municipalities, and combines it
to an NL curve, using their respective installed PV as weigths.

Writes irradiation data and curves for all municpaities to csvs.
Writes aggregated irradiation curve for NL to csv.
'''
import sys
import numpy as np
sys.path.append('../../../script_utils')

from apis import WeatherXAPI, EtlocalAPI, APIError
from config.municipality_coordinates import MUNICIPALITIES
from process_irradiation_data import normalize, export_data_to_csv

YEAR = 1987

# Some constants and globals
FIT_FACTOR = 0.002593461
api = WeatherXAPI(f'{YEAR}-01-01 00:00',f'{YEAR}-12-31 23:59')
etlocal = EtlocalAPI()

flh = {'total_flh': 0.0, 'total_weight': 0.0}

def processed_curve(municipality):
    '''
    Retrieves weather data from the API and fashions a curve from it
    Writes input and outputs files for the municupality
    Returns the processed curve (pd.Series)
    '''
    try:
        dataframe = api.get_dataframe(municipality['lat'], municipality['lon'], ['Q'])
    except APIError as exc:
        print(municipality['name'])
        print(f"\033[93m-   Skipping: {exc}\033[0m")
        return np.zeros(8760)

    solar_pv_installed = etlocal.get_solar_pv(municipality['name'])

    # Schrikkeljaar
    if dataframe.shape[0] == 8784: dataframe.drop(dataframe.tail(24).index, inplace=True)

    my_flh = dataframe['Q'].sum() * FIT_FACTOR
    print(municipality['name'])
    print('-   weight: ', solar_pv_installed)
    print('-   FLH: ', my_flh)

    missing = dataframe['Q'].isna().sum()
    if missing > 180:
        print(f"\033[93m-   Skipping: {missing} datapoints missing\033[0m")
        return np.zeros(8760)

    curve = normalize(dataframe['Q'])

    # Make it pretty
    dataframe.drop(['lat', 'lon'], 'columns', inplace=True)
    dataframe.insert(0, 'municipality', municipality['name'])

    flh['total_flh'] += my_flh * solar_pv_installed
    flh['total_weight'] += solar_pv_installed

    # Write curves and data to csv as well because they may be handy
    # export_data_to_csv(dataframe, f"input/{municipality['name']}_{YEAR}", 'nl', str(YEAR))
    # export_data_to_csv(
    #     curve, f"output/solar_pv_{municipality['name']}", 'nl', str(YEAR), header=False
    # )

    return curve * solar_pv_installed

# Aggregating and normailising the curve
nl_curve = normalize(sum((processed_curve(muni) for muni in MUNICIPALITIES)))
export_data_to_csv(nl_curve, 'output/solar_pv_weighted_nl', 'nl', str(YEAR), header=False)

print('')
print(f"Average FLH was {flh['total_flh']/flh['total_weight']}")
