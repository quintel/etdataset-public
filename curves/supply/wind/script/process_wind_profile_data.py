import glob
import os
import sys

import csv
import numpy as np
import pandas as pd
import pylab as plt

os.chdir('./../')


def read_csv(country, year):
    # Specify target path and source
    target_path = './data/{}/{}/source/'.format(country, year)
    target_file = 'time_series_60min_singleindex_filtered.csv'

    # Specify relevant columns
    column_names = [
        '{}_wind_profile'.format(str.upper(country))
    ]

    # Reading the CSV into a data-frame and fill empty (or NaN) cells with zeros
    df = pd.read_csv(target_path + target_file, usecols=column_names).fillna(0)

    # Check for leap year
    number_of_hours = df.shape[0]
    if number_of_hours > 8760:
        df = df.drop(np.r_[8760:number_of_hours])

    return df


def normalize(profile):
    return ( profile / np.sum(profile) ) / 3600.0


def main(args):
    # Specify the country and year when calling this script in the terminal
    # e.g. python3 process_wind_generation_source_data.py nl 2013
    country = args[0]
    year = args[1]

    # Read wind_profile from file for specified year and country
    data = read_csv(country, year)

    # Select wind profile data
    wind_profile = data['{}_wind_profile'.format(str.upper(country))]

    # Normalize wind profile
    normalized_wind_profile = normalize(wind_profile)

    # Export profile data to csv input files
    for wind_type in ['inland', 'coastal', 'offshore']:
        normalized_wind_profile.to_csv(r'{}/data/{}/{}/input/wind_{}.csv'.format(os.getcwd(), country, year, wind_type), index=None, header=False)


if __name__ == "__main__":
    main(sys.argv[1:])
