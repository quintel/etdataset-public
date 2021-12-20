import os
import sys

import csv
import getpass

import matplotlib.pyplot as plt
import numpy as np

os.chdir('./../')


def main(args):
    # Specify the country and year when calling this script in the terminal
    # e.g. python3 generate_solar_slider_caps.py de 2015
    country = args[0]
    year = args[1]

    # Using Spain as the max for all countries
    file_path = "/Users/{}/Projects/etsource/datasets/es/curves/weather/default/solar_pv.csv".format(getpass.getuser())
    # file_path = './data/es/{}/input/solar_pv.csv'.format(country, year)
    datafile = open(file_path, 'r')

    # Converting the curves to a numpy array
    max_solar_curve = np.genfromtxt(datafile, delimiter = ',')
    max_solar_curve = max_solar_curve / max_solar_curve.max()
    max_full_load_hours = np.sum(max_solar_curve)

    file_path = './data/{}/{}/output/solar_pv.csv'.format(country, year)
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
    #print "Ratio FLHs: "+country+" ", performance_ratio

    slider_max = performance_ratio * max_full_load_hours
    
    print "Full load hours from curve "+country+" ",full_load_hours
    print "Full load hours from dataset "+country+" ",flh_from_dataset
    print "Perfmance ratio "+country+" ",performance_ratio
    print "Slider max "+country+" ",slider_max


if __name__ == "__main__":
    main(sys.argv[1:])
