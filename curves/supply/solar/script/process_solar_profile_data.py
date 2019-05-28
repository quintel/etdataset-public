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
    target_path = './data/{}/{}/input/'.format(country, year)
    target_file = "time_series_60min_singleindex_filtered.csv"

    # Specify relevant columns
    column_names = [
        '{}_solar_profile'.format(str.upper(country))
    ]

    # Reading the CSV into a data-frame
    return pd.read_csv(target_path + target_file, usecols=column_names).fillna(0)


def normalize(profile):
    return ( profile / np.sum(profile) ) / 3600


def main(args):
    # Specify the country and year when calling this script in the terminal
    # e.g. python3 process_wind_generation_source_data.py nl 2013
    country = args[0]
    year = args[1]

    # Read wind_profile from file for specified year and country
    data = read_csv(country, year)

    # Select wind profile data
    solar_profile = data['{}_solar_profile'.format(str.upper(country))]

    # Normalize wind profile
    normalized_solar_profile = normalize(solar_profile)

    # Export profile data to csv input file
    normalized_solar_profile.to_csv(r'{}/data/{}/{}/output/solar_pv.csv'.format(os.getcwd(), country, year), index=None, header=False)


if __name__ == "__main__":
    main(sys.argv[1:])
