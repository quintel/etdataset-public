'''Export the energy balances to ETLocal'''

import shutil
import sys
from pathlib import Path

HELP = '''\033[94m
Please use this script with the following arguments:
    - year (arg 1): the analysis year for which to run all conversions
    - countries (arg 2): specify one or more countries (separated by commas, no spaces!)

For countries you can also use the special keyword 'ALL' to export all countries
at once. Omitting the countries argument results in exporting all countries as well.\033[0m
'''

COUNTRY_FOLDER_MAPPING = {
    'AT': 'AT_austria',
    'BE': 'BE_belgium',
    'BG': 'BG_bulgaria',
    'CH': 'CH_switzerland',
    'CY': 'CY_cyprus',
    'CZ': 'CZ_czechia',
    'DE': 'DE_germany',
    'DK': 'DK_denmark',
    'EE': 'EE_estonia',
    'EU27_2020': 'EU27_european_union',
    'ES': 'ES_spain',
    'FI': 'FI_finland',
    'FR': 'FR_france',
    'EL': 'EL_greece',
    'HR': 'HR_croatia',
    'HU': 'HU_hungary',
    'IE': 'IE_ireland',
    'IT': 'IT_italy',
    'LT': 'LT_lithuania',
    'LU': 'LU_luxembourg',
    'LV': 'LV_latvia',
    'MT': 'MT_malta',
    'NL': 'NL_netherlands',
    'NO': 'NO_norway',
    'PL': 'PL_poland',
    'PT': 'PT_portugal',
    'RO': 'RO_romania',
    'RS': 'RS_serbia',
    'SE': 'SE_sweden',
    'SI': 'SI_slovenia',
    'SK': 'SK_slovakia',
    'UK': 'UK_united_kingdom'
}

if __name__ == '__main__':
    if not len(sys.argv) > 1:
        raise SystemExit(HELP)

    year = sys.argv[1]
    countries = sys.argv[2].split(',') if len(sys.argv) > 2 else 'ALL'

    destination = Path(__file__).parents[4] / 'etlocal' / 'data' / 'datasets' / 'energy_balance'
    source_base = Path(__file__).parents[3] / 'data'

    if countries == 'ALL' or countries[0] == 'ALL':
        countries = list(COUNTRY_FOLDER_MAPPING.keys())

    for country in countries:
        folder_name = COUNTRY_FOLDER_MAPPING.get(country)
        if not folder_name:
            print(f'\033[93mNo folder found for {country}\033[0m')
            continue

        source_file = source_base / folder_name / year / 'energy_balance' / 'output_energy_balance_enriched.csv'

        if not source_file.exists():
            source_file = source_base / folder_name / year / 'energy_balance' / 'output_energy_balance_enriched.encrypted.csv'
            if not source_file.exists():
                print(f'\033[93mUnable to locate EB for {country} at {source_file}\033[0m')
                continue

            destination_file = destination / f'{country}_energy_balance_enriched.encrypted.csv'

        else:
            destination_file = destination / f'{country}_energy_balance_enriched.csv'

        shutil.copyfile(source_file, destination_file)
        print(f"Copied {source_file} to {destination_file}")

    print('Done!')
