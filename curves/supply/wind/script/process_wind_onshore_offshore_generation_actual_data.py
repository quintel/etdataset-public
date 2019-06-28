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

    # Reading the CSV into a data-frame
    return pd.read_csv(target_path + target_file, usecols=column_names)


def perform_checks(data, country, year):
    # Check for leap year
    number_of_hours = data.shape[0]
    if number_of_hours > 8760:
        data = data.drop(np.r_[8760:number_of_hours])

    # Check for % NaN values
    threshold = 0.02
    is_valid = {}

    for type in ['offshore', 'onshore']:
        wind_type_data = data['{}_wind_{}_generation_actual'.format(str.upper(country), type)]
        missing = float(wind_type_data.isnull().sum()) / 8760.0
        print('\nData coverage ({}): {}%'.format(type, (1.0 - missing) * 100))
        if missing >= threshold:
            is_valid[type] = False
            print('\nWARNING: CURVE IS NOT GENERATED!\n(> 2% missing data points in {})'.format('{}_wind_{}_generation_actual'.format(str.upper(country), type)))
        else:
            is_valid[type] = True
            data['{}_wind_{}_generation_actual'.format(str.upper(country), type)] = wind_type_data

    return data, is_valid


def fill_gaps(data, country, wind_type):
    column = '{}_wind_{}_generation_actual'.format(str.upper(country), wind_type)
    for index, row in data.iterrows():
        current_value = row[column]

        # Check if the current value is NaN
        if pd.isna(current_value):
            # If the current value is NaN, replace it by the first valid value
            # that is found for this hour at the day in previous days
            if index >= 24:
                replace_value = data.at[index-24, column]

                if pd.isna(replace_value):
                    # If the first day of the year still returns NaN for this hour,
                    # replace the value by 0
                    data.at[index, column] = 0.0
                else:
                    data.at[index, column] = replace_value
            else:
                data.at[index, column] = 0.0

    return data


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


def process_data(data, capacity):
    # Process generation actual data to wind profile data
    wind_profile = data / capacity
    # Return the normalized data
    return normalize(wind_profile)


def main(args):
    # Specify the country and year when calling this script in the terminal
    # e.g. python3 process_wind_onshore_offshore_generation_actual_data.py nl 2013
    country = args[0]
    year = args[1]

    # Read wind_profile from file for specified year and country
    data = read_csv(country, year)

    # Perform checks (< 2% NaN values, etc.)
    data, is_valid = perform_checks(data, country, year)

    # Get country specific specifications for onshore/offshore wind turbines
    capacity = get_capacity(country)

    if is_valid['onshore']:
        # Fill gaps
        data = fill_gaps(data, country, 'onshore')
        # Process wind onshore generation actual data
        onshore_wind_curve = process_data(data['{}_wind_onshore_generation_actual'.format(str.upper(country))], capacity['wind_inland'])
        # Export profile data to csv input files
        onshore_wind_curve.to_csv(r'{}/data/{}/{}/input/wind_inland.csv'.format(os.getcwd(), country, year), index=None, header=False)

    if is_valid['offshore']:
        # Fill gaps
        data = fill_gaps(data, country, 'offshore')
        # Process wind offshore generation actual data
        offshore_wind_curve = process_data(data['{}_wind_offshore_generation_actual'.format(str.upper(country))], capacity['wind_offshore'] + capacity['wind_coastal'])
        # Export profile data to csv input files
        for wind_type in ['offshore', 'coastal']:
            offshore_wind_curve.to_csv(r'{}/data/{}/{}/input/wind_{}.csv'.format(os.getcwd(), country, year, wind_type), index=None, header=False)


if __name__ == "__main__":
    main(sys.argv[1:])
