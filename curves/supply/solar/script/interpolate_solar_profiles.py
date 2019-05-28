import os
import sys

import csv
import getpass

import matplotlib.pyplot as plt
import numpy as np

os.chdir('./../')


def main(args):
    # Specify the country and year when calling this script in the terminal
    # e.g. python interpolate_solar_profiles.py nl 2013
    country = args[0]
    year = args[1]

    # Initialise plot
    plt.close()
    fig, ax = plt.subplots(figsize=(25,10))
    plt.subplot(1,2,1)
    plt.title("Peak capacity deviation")
    plt.xlabel("Slider setting (FLHs)")
    plt.ylabel("%")

    # Using Spain as the max for all countries
    file_path = "/Users/{}/Projects/etsource/datasets/es/load_profiles/solar_pv.csv".format(getpass.getuser())
    # file_path = './data/es/{}/input/solar_pv.csv'.format(country, year)
    datafile = open(file_path, 'r')

    # Converting the curves to a numpy array
    max_solar_curve = np.genfromtxt(datafile, delimiter = ',')
    max_solar_curve = max_solar_curve / max_solar_curve.max()
    max_full_load_hours = np.sum(max_solar_curve)

    file_path = './data/{}/{}/input/solar_pv.csv'.format(country, year)
    datafile = open(file_path, 'r')

    # Converting the curves to a numpy array
    solar_curve = np.genfromtxt(datafile, delimiter = ',')
    solar_curve = solar_curve / solar_curve.max()
    full_load_hours = np.sum(solar_curve)

    # FLHs according to the dataset
    flh_file_path = '/Users/{}/Projects/etsource/datasets/{}/central_producers.csv'.format(getpass.getuser(), country)
    csv_file = csv.reader(open(flh_file_path, "rb"), delimiter=",")

    for row in csv_file:
        if "energy_power_solar_pv_solar_radiation" == row[0]:
            flh_from_dataset = float(row[2])

    performance_ratio = flh_from_dataset / full_load_hours
    print "Ratio FLHs: "+country+" ", performance_ratio

    slider_max = performance_ratio * max_full_load_hours

    print "Slider max "+country+" ",slider_max

    slider_setting = []
    peak_capacity = []
    flhs_interpolated_curve = []
    delta = max_full_load_hours - full_load_hours
    
    for i in range(int(full_load_hours), int(max_full_load_hours), 1):

        interpolation_factor = (float(i) - full_load_hours) / delta
        interpolated_curve = (1.0 - interpolation_factor) * solar_curve + interpolation_factor * max_solar_curve
        max_interpolated_curve = np.max(interpolated_curve)

        slider_setting.append(i)
        peak_capacity.append(max_interpolated_curve)
        flhs_interpolated_curve.append(np.sum(interpolated_curve))

    plt.plot(np.array(slider_setting), 100*(np.array(peak_capacity)-1.0), label=country )

    plt.subplot(1,2,2)
    plt.title("FLHs")
    plt.xlabel("Slider setting (FLHs)")
    plt.ylabel("hours")
    plt.plot(np.array(slider_setting), flhs_interpolated_curve, label=country )

    plt.legend(bbox_to_anchor=[0.8, 0.95])
    plt.show()


if __name__ == "__main__":
    main(sys.argv[1:])
