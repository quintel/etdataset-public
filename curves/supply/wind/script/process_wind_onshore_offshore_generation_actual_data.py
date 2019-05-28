import glob
import os
import sys

import csv
import getpass

import numpy as np
import pandas as pd
import pylab as plt

os.chdir('./../')


def read_csv(country, year):
    # Specify target path and source
    target_path = './data/{}/{}/source/'.format(country, year)
    target_file = "time_series_60min_singleindex_filtered.csv"

    # Specify relevant columns
    column_names = [
        '{}_wind_offshore_generation_actual'.format(str.upper(country)),
        '{}_wind_onshore_generation_actual'.format(str.upper(country))
    ]

    # Reading the CSV into a data-frame and fill empty (or NaN) cells with zeros
    df = pd.read_csv(target_path + target_file, usecols=column_names).fillna(0)

    # Check for leap year
    number_of_hours = df.shape[0]
    if number_of_hours > 8760:
        df = df.drop(np.r_[8760:number_of_hours])

    return df


def get_capacity(country):
    capacity = {}

    flh_file_path = '/Users/{}/Projects/etsource/datasets/{}/central_producers.csv'.format(getpass.getuser(), country)
    csv_file = csv.reader(open(flh_file_path, "rb"), delimiter=",")

    for row in csv_file:
        for wind_type in ['inland', 'coastal', 'offshore']:
            if 'energy_power_wind_turbine_{}'.format(wind_type) == row[0]:
                demand = float(row[1])
                flh = float(row[2])
                capacity['wind_{}'.format(wind_type)] = ( demand / flh ) / 3.6 * 1000.0

    return capacity


def normalize(profile):
    return ( profile / np.sum(profile) ) / 3600.0


def main(args):
    # Specify the country and year when calling this script in the terminal
    # e.g. python3 process_wind_generation_source_data.py nl 2013
    country = args[0]
    year = args[1]

    # Read wind_profile from file for specified year and country
    data = read_csv(country, year)

    # Get country specific specifications for onshore/offshore wind turbines
    capacity = get_capacity(country)

    # Select wind generation actual data
    wind_offshore_generation_actual = data['{}_wind_offshore_generation_actual'.format(str.upper(country))]
    wind_onshore_generation_actual = data['{}_wind_onshore_generation_actual'.format(str.upper(country))]

    # Process to wind profile data
    # wind_profile = (wind_offshore_generation_actual + wind_onshore_generation_actual)
    # wind_profile = (wind_offshore_generation_actual + wind_onshore_generation_actual) / (capacity['wind_offshore'] + capacity['wind_coastal'] + capacity['wind_inland'])
    # print('Sum of wind profile (= FLH): {}'.format(np.sum(wind_profile)))
    wind_profile_offshore = wind_offshore_generation_actual / ( capacity['wind_offshore'] + capacity['wind_coastal'] )
    wind_profile_onshore = wind_onshore_generation_actual / capacity['wind_inland']

    # print(wind_profile)


    # Normalize wind profile
    # normalized_wind_profile = normalize(wind_profile)
    normalized_wind_profile_offshore = normalize(wind_profile_offshore)
    normalized_wind_profile_onshore = normalize(wind_profile_onshore)

    # Export profile data to csv input files
    for wind_type in ['offshore', 'coastal']:
        normalized_wind_profile_offshore.to_csv(r'{}/data/{}/{}/input/wind_{}.csv'.format(os.getcwd(), country, year, wind_type), index=None, header=False)

    normalized_wind_profile_onshore.to_csv(r'{}/data/{}/{}/input/wind_inland.csv'.format(os.getcwd(), country, year), index=None, header=False)


if __name__ == "__main__":
    main(sys.argv[1:])
