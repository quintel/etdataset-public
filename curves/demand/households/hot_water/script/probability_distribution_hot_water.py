# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 11:09:48 2015

@author: jorisberkhout
"""

#==============================================================================
# This script can be used to generate typical domestic hot water (DHW) profiles
# for a period of one year and time steps of 1 hour . The script is based in
# great part on Realistic Domestic Hot-Water Profiles in Different Time Scales,
# Jordan (2001). This study assumes a daily average DHW use of 200 liters and
# distinguishes four types of DHW consumption, each with an associated volume
# and average daily occurence:
#
# type A: short load (1 liter per event, 28 occurences per day)
# type B: medium load (6 liter per event, 12 occurences per day)
# type C: bath (140 liter per event, 0.143 occurences per day (once a week))
# type D: shower (40 liter per event, 2 occurences per day)
#
# According to Jordan (2001), the duration of each of these types is shorter
# than 15 minutes (i.e. the time resolution of our simulation). Hence we
# decided to only model the probability that an event occurs within each 15
# minute time step and assign the entire volume of that event to that 15 minute
# bin. The probability of each type of event varies throughout the year (i.e.
# slightly more DHW consumption in winter), throughout the week (more in the
# weekend) and throughout the day (no DHW consumption during the night).
#
#==============================================================================

import sys
import numpy as np
from matplotlib import pylab as plt
from pathlib import Path

# # Communicate with the user
if(len(sys.argv) != 3):
    print("Use: python " + str(sys.argv[0]) + " <country> <year> ")
    sys.exit(1)

# Import input files
else:
    country = sys.argv[1]
    year = sys.argv[2]
    output_file_path = "../data/" + country +"/" + year + "/output/"

output_file_path = "../data/" + country +"/" + year + "/output/"

# Input for start day first of January: Monday = 1, Tuesday = 2, etc
years = ["2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019","2020", "2021", "2022", "2023"]
start_days_years = [6, 7, 2, 3, 4, 5, 7, 1, 2, 3, 5, 6, 7]
first_of_jan = years.index(year)

# Global variables
# year, days, hours, quarters
days_per_year = 365
hours_per_day = 24
quarters_per_hour = 4
quarters_per_day = quarters_per_hour * hours_per_day
quarters_per_year = quarters_per_day * days_per_year

# volumes per type of event (see table 1: vol/load in l)
volume_A = 1
volume_B = 6
volume_C = 140
volume_D = 40

# daily occurence per type of event (see table 1: vol/day in 1)
occ_A = 28
occ_B = 12
occ_C = 0.143
occ_D = 2

def gauss_function(x, a, x0, sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))

quarters = np.arange(0,quarters_per_year,1.)

# The probability per year follows a cosine function with an amplitude of 10%.
# This probability function is the same for a types of events
# Derived from figure 1.3
top_of_sine_days = 45.
prob_year_ABCD = 0.5 + 0.05 * np.cos((quarters/quarters_per_year + (top_of_sine_days/days_per_year*quarters_per_day))*2*np.pi)

# All types of events have an increasing probability of happening in the weekend
# Type C (bath) follows its own probability
# Numbers from figure 1.5 in Jordan
# Using two subsequent weeks to easily pick one week sequence that fits with 1st of January
prob_week_ABD_jordan = np.array([0.95, 0.95, 0.95, 0.95, 0.98, 1.09, 1.13, 0.95, 0.95, 0.95, 0.95, 0.98, 1.09, 1.13])
prob_week_C_jordan = np.array([0.50, 0.50, 0.50, 0.50, 0.80, 1.90, 2.30, 0.50, 0.50, 0.50, 0.50, 0.80, 1.90, 2.30])

prob_week_ABD = np.zeros(7)
prob_week_C = np.zeros(7)

# Determine sequence of days in the year from 1st of January
for i in range(0,7):
    prob_week_ABD[i] = prob_week_ABD_jordan[(first_of_jan - 1 + i) % 14]
    prob_week_C[i] = prob_week_C_jordan[(first_of_jan - 1 + i) % 14]

# Each type of event follows its own probablity function during the week. I have
# recreated the probability functions shown in Figure 1.6 of Jordan (2001) below.

# Type A and B
prob_day_AB = np.zeros(96)

for i in range(5*4, 23*4):
    prob_day_AB[i] = 1/18.

# Type C
prob_day_C = np.zeros(96)

for j in range(7*4, 23*4):

    prob_day_C[j] = gauss_function(j, 0.06, 15*4., 20.)

for k in range(17*4, 21*4):

    prob_day_C[j] = gauss_function(j, 0.22, 19*4., 5)

# Type D
prob_day_D = np.zeros(96)

for k in range(5*4, 9*4):

    prob_day_D[k] = gauss_function(k, 0.25, 7*4., 4.)

for k in range(9*4, 18*4):

    prob_day_D[k] = 0.02

for k in range(18*4, 21*4):

    prob_day_D[k] = gauss_function(k, 0.085, 19.5*4., 4.)

for k in range(21*4, 23*4):

    prob_day_D[k] = 0.02


# The probability for an event to happen is prob_year * prob_week * prob_day
# The following function can be used to construct the probability function for
# an entire year with time steps of 15 minutes

def annual_probability_curve(prob_day, prob_week, prob_year):

    annual_probability = np.zeros(len(prob_year))

    for i in range(0, len(prob_year)):

        day_of_week = int(( i / 96 ) % 7)
        hour_of_day = int(i % 96)

        annual_probability[i] = prob_year[i] * prob_week[day_of_week] * prob_day[hour_of_day]

    return annual_probability

prob_year_A = annual_probability_curve(prob_day_AB, prob_week_ABD, prob_year_ABCD)
prob_year_B = annual_probability_curve(prob_day_AB, prob_week_ABD, prob_year_ABCD)
prob_year_C = annual_probability_curve(prob_day_C, prob_week_C, prob_year_ABCD)
prob_year_D = annual_probability_curve(prob_day_D, prob_week_ABD, prob_year_ABCD)

pattern = volume_A * prob_year_A * occ_A * 365 + volume_B * prob_year_B * occ_B * 365 + volume_C * prob_year_C * occ_C * 365 + volume_D * prob_year_D * occ_D * 365

# reshape to hours
hourly_data = pattern.reshape(-1, quarters_per_hour).sum(axis=1)

# normalize to a sum of 1/3600
hourly_data = hourly_data / sum(hourly_data) / 3600

# write data to file
output_path = Path(output_file_path)
output_path.mkdir(parents=True, exist_ok=True)
np.savetxt(output_path / "households_hot_water.csv", hourly_data, fmt='%.10e', delimiter=',')

# # Plot if required
# plt.plot(hourly_data[0:24*7], 'k-')
# plt.xlabel('time (hours)')
# plt.ylabel('probability')
# plt.title("Hot water demand " + country + " " + year + ", first week")
# plt.show()

print("Succesfully written output files " + str(country) + " " + str(year) + "!")
