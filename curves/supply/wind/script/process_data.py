import glob
import os
import sys

import csv
import getpass

import numpy as np
import pandas as pd
import pylab as plt

def read_csv(country, year):
    os.chdir('./../')

    # Specify target path and source
    target_path = './data/{}/{}/source/'.format(country, year)
    target_file = 'time_series_60min_singleindex_filtered.csv'

    # Reading the CSV into a data-frame and fill empty (or NaN) cells with zeros
    return pd.read_csv(target_path + target_file)


def main(args):
    # Specify the country and year when calling this script in the terminal
    # e.g. python3 process_wind_generation_source_data.py nl 2013
    country = args[0]
    year = args[1]

    # Read wind_profile from file for specified year and country
    data = read_csv(country, year)

    # Check what kind of data is available and run relevant script
    columns = data.columns.tolist()

    os.chdir('./script')

    if '{}_wind_profile'.format(str.upper(country)) in columns:
        print('Wind profile (= capacity factor) data available!')
        os.system('python process_wind_profile_data.py {} {}'.format(country, year))
    elif '{}_wind_onshore_generation_actual'.format(str.upper(country)) in columns:
        if '{}_wind_offshore_generation_actual'.format(str.upper(country)) in columns:
            print('Both onshore and offshore wind data available!')
            os.system('python process_wind_onshore_offshore_generation_actual_data.py {} {}'.format(country, year))
        else:
            print('Only onshore wind data available!')
            os.system('python process_wind_onshore_generation_actual_data.py {} {}'.format(country, year))


if __name__ == "__main__":
    main(sys.argv[1:])
