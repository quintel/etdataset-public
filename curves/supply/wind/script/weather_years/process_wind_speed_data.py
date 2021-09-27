import os
import sys

import csv
# import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# import pickle
from pathlib import Path

# from knmy import knmy

# Ignore warnings
pd.options.mode.chained_assignment = None  # default='warn'


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
    print('   VARIABLES: [WIND]')

    return knmy.get_hourly_data(stations=stations, start=start, end=end,
                                inseason=False, variables=['WIND'],
                                parse=True)


def preprocess(data):
    """
    Preprocess data
    """
    print('\nPreprocessing the data..')

    # Remove first row, which is a duplicate header
    data = data[1:len(data)]

    # Convert values to floats and replace nan values by zeros for the
    # following columns
    column_names = list(data.head())

    # STN (station), YYYYMMDD (date) and HH (hour) don't have to be converted
    # to numeric values
    for column in ['STN', 'YYYYMMDD', 'HH']:
        column_names.remove(column)

    # FH: uurgemiddelde windsnelheid (in 0.1 m/s)
    relevant_columns = ['FH']

    for column in column_names:
        # For each remaining column, convert values to floats,
        data.loc[:, column] = data[column].astype(float).to_numpy()

        # print the characteristics for the relevant columns,
        if column in relevant_columns:
            print_characteristics(data, column)

        # and replace the nans by alternative values
        data.loc[:, column] = fill_gaps(data, column).to_numpy()

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


def export_to_input_csv(data, name, country, year, header=True):
    """
    Export data to output CSV file
    """
    print('\nExporting the data..')

    filename = Path(__file__).resolve().parents[2] / 'data' / country / year / 'input' / '{}.csv'.format(name)

    # create file/folders if non-existent
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    data.to_csv(filename, index=None, header=header)

    print('Done!')


def main(args):
    """
    Specify the country and year when calling this script in the terminal, e.g.

    python3 process_wind_speed_data.py nl 1997
    """

    try:
        country = args[0]
        year = args[1]
    except:
        print('\nProvide the correct arguments, e.g. python3 process_irradiation_data.py nl 1997')
        sys.exit(1)

    # Specify paramaters
    # stations = [240, 260, 269] # De Bilt (260), Schiphol (240), Lelystad (269)
    stations = [201,203,204,205,206,207,208,211,212,214,239,252,320,321,
                209,210,215,225,235,240,242,248,249,251,257,258,260,265,267,
                269,270,273,275,277,278,279,280,283,285,286,290,308,310,311,
                312,313,315,316,319,323,324,330,331,340,343,344,348,350,356,
                370,375,377,380,391]

    start = int('{}010101'.format(year))
    end = int('{}123124'.format(year))

    # Get hourly data
    disclaimer, output_stations, variables, data = get_hourly_data(stations, start, end)

    # Preprocess data
    data = preprocess(data)

    # Print data
    # print('\nPrinting the data..')
    # print('\n{}\n'.format(data))

    # Get wind speed data for each station
    print('\nGetting wind speed for each weather station..')
    wind_measurements = {}
    for station in stations:
        measurement = list(data.loc[data['STN'] == str(station)]['FH'])
        # If the year is a leap year, take the first 8760 hours of the year
        measurement = measurement[0:8760]
        # Check if the weather station has data available. If so--i.e. the
        # length of the measurement list equals 8760--add the station to the
        # wind measurements dictionary
        if len(measurement) == 8760:
            wind_measurements[station] = measurement

    # Create new dataframe that will be exported to the input data csv
    input_data = pd.DataFrame(wind_measurements, columns=stations)

    # Print data
    print('\nPrinting the data..')
    print('\n{}\n'.format(input_data))

    # Export data to input data CSV
    export_to_input_csv(input_data, 'wind_measurements', country, year)

    # Plot curves (FH: uurgemiddelde windsnelheid (in 0.1 m/s))
    # plot_curves(data, ['FH'])


if __name__ == "__main__":
    main(sys.argv[1:])
