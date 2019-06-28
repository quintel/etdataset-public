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
        '{}_wind_onshore_generation_actual'.format(str.upper(country))
    ]

    # Reading the CSV into a data-frame and fill empty (or NaN) cells with zeros
    df = pd.read_csv(target_path + target_file, usecols=column_names).fillna(0)

    # Check for leap year
    number_of_hours = df.shape[0]
    if number_of_hours > 8760:
        df = df.drop(np.r_[8760:number_of_hours])

    return df


def perform_checks(data, country, year):
    # Check for leap year
    number_of_hours = data.shape[0]
    if number_of_hours > 8760:
     data = data.drop(np.r_[8760:number_of_hours])

    # Check for % NaN values
    threshold = 0.02
    missing = float(data['{}_wind_onshore_generation_actual'.format(str.upper(country))].isnull().sum()) / 8760.0
    print('\nData coverage: {}%'.format((1.0 - missing) * 100))
    if missing >= threshold:
     print('\nWARNING: CURVE IS NOT GENERATED!\n(> 2% missing data points in {})'.format(country, year, '{}_wind_onshore_generation_actual'.format(str.upper(country))))
     return data, False

    return data, True


def fill_gaps(data, country):
    column = '{}_wind_onshore_generation_actual'.format(str.upper(country))
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
                data.at[index, column]

    return data


def normalize(profile):
    return ( profile / np.sum(profile) ) / 3600.0


def main(args):
    # Specify the country and year when calling this script in the terminal
    # e.g. python3 process_wind_generation_source_data.py nl 2013
    country = args[0]
    year = args[1]

    # Read wind_profile from file for specified year and country
    data = read_csv(country, year)

    # Perform checks (< 2% NaN values, etc.)
    data, check = perform_checks(data, country, year)

    if check:
        # Fill gaps
        data = fill_gaps(data, country)

        # Select wind profile data
        wind_profile = data['{}_wind_onshore_generation_actual'.format(str.upper(country))]

        # Normalize wind profile
        normalized_wind_profile = normalize(wind_profile)

        # Export profile data to csv input files
        for wind_type in ['inland', 'coastal', 'offshore']:
            normalized_wind_profile.to_csv(r'{}/data/{}/{}/input/wind_{}.csv'.format(os.getcwd(), country, year, wind_type), index=None, header=False)


if __name__ == "__main__":
    main(sys.argv[1:])
