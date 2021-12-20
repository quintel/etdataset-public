import sys
import numpy as np
from pathlib import Path

sys.path.append('../../script_utils')

from renewables_ninja import RenewablesNinja

DATA_FOLDER = '../../solar'/Path(__file__).parents[0] / 'data'

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
    # e.g. python3 process_solar_generation_source_data.py nl,be,de 2019
    countries = args[0].upper().split(',')

    year = args[1]

    ninja_api = RenewablesNinja(year, countries=countries)

    for country, solar_curve in ninja_api.get_all_pv():
        print()
        print(f'Downloading curve for {country}')
        solar_curve = validate(solar_curve)

        print(f"-- Full load hours: {solar_curve['national'].sum()}")


        # Do we want this? This ninja curve has concurrency enabled...
        print('   Normalizing curve')
        solar_curve = normalize(solar_curve)

        export_path = DATA_FOLDER / country / year / 'output'
        export_path.mkdir(parents=True, exist_ok=True)
        solar_curve.to_csv(export_path/ 'solar_pv.csv', index=None, header=False)
        print('\033[92m   Curve was exported\033[0m')


if __name__ == "__main__":
    main(sys.argv[1:])
