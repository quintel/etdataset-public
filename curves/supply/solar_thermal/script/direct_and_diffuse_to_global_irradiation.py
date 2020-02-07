import glob
import os
import sys

import csv
import getpass
import math
import numpy as np
import pandas as pd
import pvlib
import pylab as plt

import numpy

os.chdir("./../")


SECONDS_PER_HOUR = 3600.0
M2_TO_CM2 = 1E4
WATTS_PER_KW = 1000.

LONGITUDES = {
    "be": 4.4699,
    "de": 10.4515,
    "dk": 9.5018,
    "es": 3.7492,
    "fr": 2.2137,
    "nl": 5.2913,
    "pl": 19.1451,
    "uk": 3.4360
}


def load_source_data(country, year):
    # Specify target path and source
    target_path = "./data/{}/{}/source/".format(country, year)
    target_file = "weather_data_filtered.csv"

    # Specify relevant columns
    column_names = [
        "utc_timestamp",
        "{}_radiation_direct_horizontal".format(str.upper(country)),
        "{}_radiation_diffuse_horizontal".format(str.upper(country))
    ]

    # Reading the CSV into a data-frame
    return pd.read_csv(target_path + target_file, usecols=column_names)


def main(args):
    try:
        country = args[0]
        year = args[1]
    except:
        print('\nProvide the correct arguments, e.g. python3 process_irradiation_data.py nl 2015')
        sys.exit(1)

    source_data = load_source_data(country, year)

    # Preprocessing (fill gaps, etc.)
    # TODO?

    # Select data
    direct_normal_irradiation = source_data["{}_radiation_direct_horizontal".format(str.upper(country))]
    diffuse_horizontal_irradiation = source_data["{}_radiation_diffuse_horizontal".format(str.upper(country))]

    # Get DateTimeIndex list of timestamps for specified year
    timestamps = pd.date_range(start="{}-01-01 00:00:00".format(year), periods=8760, freq="H")

    # Calculate equation of time for each day of the year
    equation_of_time = []
    for day_of_year in range(0,365):
        for hour_of_day in range(0,24):
            equation_of_time.append(pvlib.solarposition.equation_of_time_pvcdrom(day_of_year))

    average_equation_of_time = np.mean(equation_of_time)

    # Get solar hour angle
    solar_hour_angles = pvlib.solarposition.hour_angle(timestamps, LONGITUDES[country], average_equation_of_time)

    # Calculate global horizontal irradiation in J/cm2
    global_horizontal_irradiation = []
    for i in range(0,8760):
        angle_in_rad = solar_hour_angles[i] * math.pi / 180.
        direct_normal_irradiation_in_watt_per_m2 = direct_normal_irradiation[i] * math.cos(angle_in_rad) + diffuse_horizontal_irradiation[i]
        direct_normal_irradiation_in_j_per_cm2 = direct_normal_irradiation_in_watt_per_m2 / M2_TO_CM2 * SECONDS_PER_HOUR
        global_horizontal_irradiation.append(direct_normal_irradiation_in_j_per_cm2)

    # Export global horizontal irradiation profile to csv input file
    pd.DataFrame(global_horizontal_irradiation).to_csv(r'{}/data/{}/{}/input/irradiation.csv'.format(os.getcwd(), country, year), index=None, header=False)


if __name__ == '__main__':
    main(sys.argv[1:])
