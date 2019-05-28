# -*- coding: utf-8 -*-
import numpy as np
import sys
import pylab as plt
from numpy import genfromtxt
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import os
from pylab import *

# General constants
T_lower_limit = 14. # cooling starts above this temerature
flh_required = 1500.0  # typical flh for a cooling device in The Netherlands, see Read me
number_of_values_moving_average = 24
constant_cooling_factor = 0.5

# Define start value of upper limit close to lower limmit
T_upper_limit = T_lower_limit + 0.01 # start value of upper limit cooling

# Calculations with constants
annual_sum_constant = (1/3600.) * constant_cooling_factor
annual_sum_temperature = (1/3600.) * (1-constant_cooling_factor)
constant_cooling_value = annual_sum_constant / (365.*24.)

# # Communicate with the user
# if(len(sys.argv) != 3):
#     print "Use: python " + str(sys.argv[0]) + " <country> <year> "
#     sys.exit(1)
# else:
#     country = sys.argv[1]
#     year = sys.argv[2]
#     temperature_file_path = "../data/" + country +"/" + year + "/input" + "/air_temperature.csv"
#     output_file_path = "../data/" + country +"/" + year + "/output/"

country = "nl" 
year = "2015"
temperature_file_path ="air_temperature_2015.csv"

# temperature_file_path = "../data/" + country +"/" + year + "/input" + "/air_temperature.csv"
# output_file_path = "../data/" + country +"/" + year + "/output/"

# Define empty arrays
temperature = np.genfromtxt(temperature_file_path, delimiter=",") # degrees C
T_cooling = np.zeros(len(temperature))
cooling_curve = np.zeros(len(temperature))

# Smooth temperature curve
N = number_of_values_moving_average
cumsum, moving_aves = [0], []

for i, x in enumerate(temperature, 1):
    cumsum.append(cumsum[i-1] + x)
    if i>=N:
        moving_ave = (cumsum[i] - cumsum[i-N])/N
        #can do stuff with moving_ave here
        moving_aves.append(moving_ave)

temperature_smooth = moving_aves

# Generate cooling curve above start temperature
for i in range(0,len(temperature_smooth)):
    if temperature_smooth[i] > T_lower_limit:
        T_cooling[i] = temperature_smooth[i] - T_lower_limit
    else:
        T_cooling[i] = 0.0

# Define function that generates cooling curve between start temperature and upper limit and calculates flh
def find_Tcooling_max(T_upper_limit, T_cooling, cooling_curve ):
    T_upper_limit = T_upper_limit + 0.05

    # Generate cooling curve between start temperature and upper limit
    for i in range(0,len(temperature_smooth)):
        if temperature_smooth[i] > T_upper_limit:
            cooling_curve[i] = T_upper_limit - T_lower_limit
        else:
            cooling_curve[i] = T_cooling[i]

    # Normalize T_cooling
    cooling_curve = cooling_curve / sum(cooling_curve) * (annual_sum_temperature)
    cooling_curve = np.array(cooling_curve)

    # Construct cooling curve by adding constant_cooling_value to normalized T cooling
    cooling_curve = cooling_curve + constant_cooling_value
    cooling_range = np.amax(cooling_curve, axis=0)
    load_technology = np.zeros(len(cooling_curve))
    sum_cooling_curve = sum(cooling_curve)

    # Find flh
    for i in range(0,len(cooling_curve)):
        load_technology[i] = cooling_curve[i] / cooling_range
    flh = sum(load_technology)

    return T_upper_limit,T_cooling,cooling_curve,flh


# Make sure while loop starts
flh = flh_required + 1.

# Iterate, lower upper limit until flh_required is reached
while flh > flh_required:
    T_upper_limit, T_cooling, cooling_curve, flh = find_Tcooling_max(T_upper_limit, T_cooling, cooling_curve)

# Calculate some extra output parameters
hourly_data = cooling_curve
peak_hourly_data = max(hourly_data)
average_hourly_data = average(hourly_data)
average_temperature = average(temperature)

# Print interesting input and output (if required)
print("Full load hours of cooling technology = " + str(round(flh,1)))
print("Running average over = " + str(round(number_of_values_moving_average,1)) + " h")
print("Average temperature = " + str(round(average_temperature,1)) + " degrees C")
print("Cooling starts at " + str(T_lower_limit) + " degrees C")
print("Cooling ends at = " + str(T_upper_limit) + " degrees C")
print("Maximum temperature drop = " + str(T_upper_limit-T_lower_limit) + " degrees C")
print("Peak / average = " + str(round(peak_hourly_data/average_hourly_data,1)))

#Plot (if required)
subplot(2,2,1)
plt.plot(temperature[0:24*365], 'b-')
plt.axhline(y=T_lower_limit, color='r', linestyle='-')
plt.axhline(y=T_upper_limit, color='r', linestyle='-')
plt.xlabel('time (hours)')
plt.ylabel('temperature (degrees C)')
plt.title("Temperature curve raw ")

subplot(2,2,2)
plt.plot(temperature_smooth[0:24*365], 'b-')
plt.axhline(y=T_lower_limit, color='r', linestyle='-')
plt.axhline(y=T_upper_limit, color='r', linestyle='-')
plt.xlabel('time (hours)')
plt.ylabel('temperature (degrees C)')
plt.title("Temperature curve smooth ")

subplot(2,2,3)
plt.plot(hourly_data[0:24*365], 'b-')
plt.title("Normalized cooling curve ")
plt.xlabel('time (hours)')
plt.ylabel('Normalized cooling curve')

subplot(2,2,4)
plt.plot(hourly_data[24*160:24*165], 'b-')
plt.title("Cooling curve, 5 days in summer")
plt.xlabel('time (hours)')
plt.ylabel('Normalized cooling curve')

plt.suptitle("Cooling households " + country + " " + year, fontsize=16)

plt.show()

# # Write data to file
# np.savetxt(output_file_path + "households_cooling" + ".csv", hourly_data, fmt='%.13f', delimiter=',')
# print("Succesfully written output files " + str(country) + " " + str(year) + "!")
