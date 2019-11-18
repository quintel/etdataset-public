import os
import sys

import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle
from pathlib import Path

from knmy import knmy

# Ignore warnings
pd.options.mode.chained_assignment = None  # default='warn'

FIT_FACTOR = 0.002593461


def get_hourly_data(stations, start, end):
    """
    Return dataframe with hourly wind and temperature data for station 209
    (IJmond) and 235 (De Kooy) for the 1st of January of the year 2018 the 31rd
    of December

    The attribute inseason is set to False since we will always need curves
    for every hour of the year. Furthermore, parse is by default set to True.

    Variables:
    ALL = All variables (Default)
    WIND = DDVEC:FG:FHX:FHX:FX Wind
    TEMP = TG:TN:TX:T10N Temperature
    SUNR = SQ:SP:Q Sunshine
    PRCP = DR:RH:EV24 Precipitation and potential evaporation
    PRES = PG:PGX:PGN Pressure at sea level
    VICL = VVN:VVX:NG Visibility and cloud cover
    MSTR = UG:UX:UN Humidity

    Documentation:
    https://knmy.readthedocs.io/en/latest/
    https://projects.knmi.nl/klimatologie/uurgegevens/selectie.cgi
    """
    print('\nGetting hourly KNMI data..\n')
    print('   STATIONS: {}'.format(stations))
    print('   START: {}'.format(start))
    print('   END: {}'.format(end))
    print('   VARIABLES: [SUNR]')

    return knmy.get_hourly_data(stations=stations, start=start, end=end,
                                inseason=False, variables=['SUNR'],
                                parse=True)


def preprocess(data):
    """
    Preprocess data
    """
    print('\nPreprocessing the data..')

    # Remove first row, which is a duplicate header
    data = data[1:8761]

    # Convert values to floats and replace nan values by zeros for the
    # following columns
    column_names = list(data.head())

    # STN (station), YYYYMMDD (date) and HH (hour) don't have to be converted
    # to numeric values
    for column in ['STN', 'YYYYMMDD', 'HH']:
        column_names.remove(column)

    # Q: globale straling (in J/cm2) per uurvak
    relevant_columns = ['Q']

    for column in column_names:
        # For each remaining column, convert values to floats,
        data.loc[:, column] = data[column].astype(float)

        # print the characteristics for the relevant columns,
        if column in relevant_columns:
            print_characteristics(data, column)

        # and replace the nans by alternative values
        data.loc[:, column] = fill_gaps(data, column)

    return data


def fill_gaps(data, column):
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

    return data[column]


def print_characteristics(data, column):
    """
    Print several characteristics for the hourly data, such as min, max, mean,
    number of nan, data coverage, etc.
    """

    filtered_data = data[column]
    coverage = round(100. - (filtered_data.isna().sum() / 8760.) * 100., 2)

    print('\nCharacteristics for {}:'.format( column))
    print('   COVERAGE: {}%'.format(coverage))
    print('   MIN: {}'.format(min(filtered_data)))
    print('   MAX: {}'.format(max(filtered_data)))
    print('   MEAN: {}'.format(round(np.mean(filtered_data),3)))


def normalize(data):
    """
    Normalize the curve data so that the values sum to 1/3600.
    """

    return ( data / np.sum(data) / 3600. )


def plot_curves(data, columns):
    """
    Plot the data as a curve. The data input should contain a dataframe with
    one column of data.
    """
    print('\nPlotting the data..')

    plt.figure()
    for column in columns:
        data[column].plot()
    plt.legend(loc='best')
    plt.show()

    print('Done!')


def export_data_to_csv(data, name, country, year, header=True):
    """
    Export data to output CSV file
    """
    print('\nExporting the data to {}..'.format(name))

    filename = Path(__file__).resolve().parents[2] / 'data' / country / year / '{}.csv'.format(name)

    # create file/folders if non-existent
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    data.to_csv(filename, index=None, header=header)

    print('Done!')


def determine_flh(data):
    """
    TO DO: EXPLANATION!
    """
    print('\nDetermining FLH..')

    flh = data['Q'].sum() * FIT_FACTOR

    print('FLH: {}'.format(flh))

    return flh


def main(args):
    """
    Specify the country and year when calling this script in the terminal, e.g.

    python3 process_irradiation_data.py nl 1987
    """

    try:
        country = args[0]
        year = args[1]
    except:
        print('\nProvide the correct arguments, e.g. python3 process_irradiation_data.py nl 2015')
        sys.exit(1)

    # Specify paramaters
    station = [260] # De Bilt (260)
    start = int('{}010101'.format(year))
    end = int('{}123124'.format(year))

    # Get hourly data
    disclaimer, stations, variables, data = get_hourly_data(station, start, end)

    print(data)

    # Preprocess data
    data = preprocess(data)

    # Print data
    print('\nPrinting the data..')
    print('\n{}\n'.format(data))

    # Determine flh for this year
    flh_value = determine_flh(data)

    # Export data to input data CSV
    export_data_to_csv(data, 'input/Q_{}_STN{}'.format(round(start/1E6),station[0]), country, year)

    # Process input data to output data (= curve)
    curve = normalize(data['Q'])

    # Export data to output data CSV (curve to be exported to ETSource)
    # By taking the rows [1:8761], the header ('Q') is removed from the data.
    export_data_to_csv(curve, 'output/solar_pv', country, year, header=False)

    # Create a dataframe to export the flh
    flh_key = 'flh_of_energy_power_solar_pv_solar_radiation'
    flh = pd.DataFrame({flh_key: [flh_value]}, columns=[flh_key])

    # Also, export the flh value
    export_data_to_csv(flh, 'output/{}'.format(flh_key), country, year)

    # Plot curves (Q: globale straling (in J/cm2) per uurvak)
    plot_curves(data, ['Q'])


if __name__ == "__main__":
    main(sys.argv[1:])
