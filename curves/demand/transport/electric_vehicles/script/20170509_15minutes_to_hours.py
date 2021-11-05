import numpy as np
import pylab as plt
import glob
import csv
import os
import sys

os.chdir('./../')

def quarters_to_hours(array):

   hourly_data = []

   for i in range(int(len(array)/4)):
        mean = np.sum(array[i * 4:i * 4 + 4]) / 4
        hourly_data.append(mean)

   return np.array(hourly_data)


def main(args):
    # Specify the country and year when calling this script in the terminal
    # e.g. python 20170509_15minutes_to_hours.py nl 2013
    country = args[0]
    year = args[1]

    # Reading in the patterns
    files = glob.glob(os.getcwd() + '/data/{}/source/profile_*.csv'.format(country, year))

    for current_file in files:

        print(current_file)

        weekdata = []
        weekenddata = []

        with open(current_file, 'rU') as csvfile:
              reader = csv.reader(csvfile, delimiter=',', quotechar='#')
              for row in reader:

                  weekday, weekendday = row

                  weekdata.append(weekday)
                  weekenddata.append(weekendday)


        weekdata = weekdata[1:]
        weekenddata = weekenddata[1:]

        weekdata = [float(x) for x in weekdata]
        weekenddata = [float(x) for x in weekenddata]

        weekdata = quarters_to_hours(weekdata)
        weekenddata = quarters_to_hours(weekenddata)

        #weekdata = weekdata / np.sum(weekdata)
        #weekenddata = weekenddata / np.sum(weekenddata)

        print(weekdata)
        print(weekenddata)

        plt.savetxt(os.getcwd() + '/data/{}/{}/input/hourly_week_'.format(country, year) + current_file.split('/')[-1], weekdata, fmt='%.15f')
        plt.savetxt(os.getcwd() + '/data/{}/{}/input/hourly_weekend_'.format(country, year) + current_file.split('/')[-1], weekenddata, fmt='%.15f')


if __name__ == "__main__":
    main(sys.argv[1:])
