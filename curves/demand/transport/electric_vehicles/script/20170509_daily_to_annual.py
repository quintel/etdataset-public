from datetime import date, timedelta, datetime
import numpy as np
import pylab as plt
import glob
import csv
import os
import sys

os.chdir('./../')

def main(args):
    # Specify the country and year when calling this script in the terminal
    # e.g. python 20170509_daily_to_annual.py nl 2013
    country = args[0]
    year = args[1]

    # 2013: Tuesday (1) 2014: Wednesday (2) 2015: Thursday (3),
    # 2016: Friday (4), 2017: Sunday (6), 2018: Monday (0)
    first_of_jan = date(int(year), 1, 1).weekday()

    scaling_factor = 1/3600.

    # Profiles 1, 2, and 3 are Movares based; 4 en 5 are ELaad/Jedlix based.
    for profile_number in [1,2,3,4,5]:

        week = list(plt.loadtxt(os.getcwd() + '/data/{}/{}/input/hourly_week_profile_'.format(country, year) + str(profile_number) + '.csv'))
        weekend = list(plt.loadtxt(os.getcwd() + '/data/{}/{}/input/hourly_weekend_profile_'.format(country, year) + str(profile_number) + '.csv'))

        annual_profile = []

        for i in range(0,365):

          # the first_of_jan is to account for the fact that January 1 could be
          # any weekday dependent on the year
          if (i + first_of_jan) % 7 < 5:

            annual_profile.extend(week)

            print("week")

          else:

            annual_profile.extend(weekend)

            print("weekend")

        annual_profile = annual_profile / sum(annual_profile) * scaling_factor

        plt.plot(annual_profile)
        plt.show()

        plt.savetxt(os.getcwd() + '/data/{}/{}/output/electric_vehicle_profile_'.format(country,year) + str(profile_number) + '.csv', annual_profile)


if __name__ == "__main__":
    main(sys.argv[1:])
