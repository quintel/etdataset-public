import sys
import numpy as np
from pathlib import Path

sys.path.append('../../script_utils')

from renewables_ninja import RenewablesNinja

DATA_FOLDER = '../../wind'/Path(__file__).parents[0] / 'data'

def validate(data):
    # Check for leap year
    number_of_hours = data.shape[0]
    if number_of_hours > 8760:
        data = data.drop(np.r_[8760:number_of_hours])

    # Check for % NaN values
    threshold = 0.02
    missing = data['national'].isnull().sum() / 8760.0
    print(f'-- Data coverage: {(1.0 - missing) * 100}%')

    if missing >= threshold:
        raise SystemExit('WARNING: CURVE IS NOT GENERATED!\n(> 2% missing data points)')

    return data


def normalize(profile): ## moet blijven
    return ( profile / np.sum(profile) ) / 3600.0


def main(args):
    # Specify the country and year when calling this script in the terminal
    # e.g. python3 process_wind_renewables_ninja.py cz 2019
    countries = args[0].upper().split(',')

    year = args[1]

    ninja_api = RenewablesNinja(year, countries=countries)

    for country, wind_curves in ninja_api.get_all_wind_curves():
        print()
        print(f'Downloading curve for {country}')
        wind_curve = validate(wind_curves)
        export_path = DATA_FOLDER / country / year / 'output'
        export_path.mkdir(parents=True, exist_ok=True)

        # Not all countries have an onshore and an offshore curve.
        # If a country only has a national curve that curve is used for onshore, offshore and coastal.
        if 'offshore' in wind_curves:
            print('Offshore exists, so different curves for onshore and offshore')
            print(f"-- Full load hours offshore/coastal: {wind_curves['offshore'].sum()}")
            print(f"-- Full load hours onshore: {wind_curves['onshore'].sum()}")

            wind_curves_onshore = normalize(wind_curves['onshore'])
            wind_curves_offshore = normalize(wind_curves['offshore'])

            wind_curves_onshore.to_csv(export_path/ 'wind_inland_baseline.csv', index=None, header=False)
            wind_curves_offshore.to_csv(export_path/ 'wind_offshore_baseline.csv', index=None, header=False)
            wind_curves_offshore.to_csv(export_path/ 'wind_coastal_baseline.csv', index=None, header=False)
            print('\033[92m   Curve wind onshore, coastal and offshore were exported using onshore and offshore curves\033[0m')
        else:
            print('No offshore curve so national curve is used for onshore and offshore')
            print(f"-- Full load hours onshore/offshore/coastal: {wind_curves['national'].sum()}")

            wind_curves_national = normalize(wind_curves['national'])

            wind_curves_national.to_csv(export_path/ 'wind_inland_baseline.csv', index=None, header=False)
            wind_curves_national.to_csv(export_path/ 'wind_offshore_baseline.csv', index=None, header=False)
            wind_curves_national.to_csv(export_path/ 'wind_coastal_baseline.csv', index=None, header=False)
            print('\033[92m   Curve wind onshore, coastal and offshore were exported using curve "national" \033[0m')

if __name__ == "__main__":
    main(sys.argv[1:])

