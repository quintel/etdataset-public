'''
This script export keys and commit messages to ETLocal, by taking keys from
output_xxx.csv files in data/COUNTRY/YEAR
'''

import shutil
import sys
from pathlib import Path
import os

import pandas as pd
import yaml


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


def get_all_keys(base_folder, drop_na=False):
    df_lst = []
    for subdir, _, files in os.walk(base_folder):
        # Skip files in energy_balance folder
        if os.path.basename(subdir) == "energy_balance":
            continue

        for file in files:
            if file.startswith("output_"):
                df = pd.read_csv(os.path.join(subdir, file))
                df_lst.append(df)

    df = pd.concat(df_lst, ignore_index=True).sort_values('key')

    # Drop keys without value which should be generated based on energy balance
    if drop_na:
        df = df.dropna(subset=['value'])

    return df


def export_commit_yml(df, output_file):
    yaml_lines = ['---']

    # Loop through the dataframe and format each row into YAML structure
    for index, row in df.iterrows():
        yaml_lines.append("- fields:")
        yaml_lines.append(f"  - {row['key']}")
        if row['comment']:  # Only add 'message' if there is a comment
            yaml_lines.append("  message:")
            yaml_lines.append(f"   \"{row['comment']}\"")
        yaml_lines.append("")

    # Join the list into a single string with newlines
    yaml_content = '\n'.join(yaml_lines)

    with open(output_file, 'w') as file:
        file.write(yaml_content)


def export_keys_csv(df, output_file):
    df = df[['key','value']].set_index('key')
    # Transpose dataframe to correct ETLocal format
    df.T.to_csv(output_file, index=False)


if __name__ == '__main__':
    if not len(sys.argv) > 1:
        raise SystemExit(HELP)

    year = sys.argv[1]
    countries = sys.argv[2].split(',') if len(sys.argv) > 2 else 'ALL'

    destination = Path(__file__).parents[3] / 'etlocal' / 'data' / 'datasets' / 'other_keys'
    source_base = Path(__file__).parents[2] / 'data'

    if countries == 'ALL' or countries[0] == 'ALL':
        countries = list(COUNTRY_FOLDER_MAPPING.keys())

    for country in countries:
        folder_name = COUNTRY_FOLDER_MAPPING.get(country)
        if not folder_name:
            print(f'\033[93mNo folder found for {country}\033[0m')
            continue

        destination_country_year = destination / folder_name / year
        source_base_country_year = source_base / folder_name / year

        # Create destination folder if not already exists
        os.makedirs(destination_country_year, exist_ok=True)

        if not source_base_country_year.exists():
            print(f'\033[93mUnable to locate data folder for {country} at {source_base_country_year}\033[0m')
            continue

        df = get_all_keys(source_base_country_year, drop_na=True)
        export_commit_yml(df, destination_country_year / 'commits.yml')
        export_keys_csv(df, destination_country_year / 'data.csv')

        print(f'{country} finished')

    print(f'Commits yml and data csv files exported to {destination}')
    print('Done!')
