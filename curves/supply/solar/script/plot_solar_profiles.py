import os
import sys

import csv
import getpass

import matplotlib.pyplot as plt
import numpy as np

os.chdir('./../')


def main(args):
    # Specify the country and year when calling this script in the terminal
    # e.g. python3 process_wind_generation_source_data.py nl 2013
    country = args[0]
    year = args[1]

    # Initialise plot
    plt.close()
    fig, ax = plt.subplots(figsize=(25,10))
    plt.subplot(1,1,1)
    plt.title("Solar irradation")
    plt.xlabel("time (hours)")
    plt.ylabel("MW")
    min_hours = 100
    max_hours = 8760
    plt.xlim(min_hours,max_hours)

    # Specify file path and open file
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
        if 'energy_power_solar_pv_solar_radiation' == row[0]:
            flh_from_dataset = float(row[2])

    #### Plotting curves
    plt.plot(np.array(range(min_hours,max_hours)), solar_curve[min_hours:max_hours], label=country+": {:.0f}".format(full_load_hours)+", from dataset: {:.0f}".format(float(flh_from_dataset)) )

    print "Ratio FLHs: "+country+" ", flh_from_dataset / full_load_hours

    plt.legend(bbox_to_anchor=[0.8, 0.95])
    plt.show()


if __name__ == "__main__":
    main(sys.argv[1:])
