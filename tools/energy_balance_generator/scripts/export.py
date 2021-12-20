'''Export the energy balances to ETLocal'''

import shutil
import sys
from pathlib import Path

HELP = '''\033[94m
Please use this script with the following arguments:
    - year (arg 1): the analysis year for which to run all conversions
    - countries (arg 2): specify one or more countries (separated by commas, no spaces!)

For countries you can also use the special keyword 'ALL' to export all countries
at once. Omiting the countries agrument results in exporting all countries as well.\033[0m
'''

if __name__ == '__main__':
    if not len(sys.argv) > 1:
        raise SystemExit(HELP)

    year = sys.argv[1]
    countries = sys.argv[2].split(',') if len(sys.argv) > 2 else 'ALL'

    destination = Path(__file__).parents[4] / 'etlocal' / 'data' / 'datasets'
    source = Path(__file__).parents[1] / 'data' / 'energy_balances' / str(year)

    if countries == 'ALL' or countries[0] == 'ALL':
        for file in source.glob('*.csv'):
            if file.stem == 'full_load_hours': continue

            shutil.copyfile(file, destination / file.name)
    else:
        for country in countries:
            file = source / f'{country}.csv'

            if not file.exists():
                print(f'\033[93mUnable to locate EB for {country}\033[0m')
                continue

            shutil.copyfile(file, destination / f'{country}.csv')

    print('Done!')
