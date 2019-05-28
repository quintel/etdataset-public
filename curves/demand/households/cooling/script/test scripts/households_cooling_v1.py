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
T_lower_limit = 19.5 # cooling starts above this temerature
flh_required = 400.0  # typical flh for a cooling device in The Netherlands, see Read me
T_upper_limit = 40.0 # start value of upper limit cooling

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

temperature = np.genfromtxt(temperature_file_path, delimiter=",") # degrees C
T_cooling = np.zeros(len(temperature))

# temperature_file_path = "../data/" + country +"/" + year + "/input" + "/air_temperature.csv"
# output_file_path = "../data/" + country +"/" + year + "/output/"

# Generate cooling curve above start temperature
for i in range(0,len(temperature)):
    if temperature[i] > T_lower_limit:
        T_cooling[i] = temperature[i] - T_lower_limit
    else:
        T_cooling[i] = 0.0

# Define function that generates cooling curve between start temperature and upper limit and calculates flh
def find_Tcooling_max(T_upper_limit, T_cooling, ):
    T_upper_limit = T_upper_limit - 0.1

    # Generate cooling curve between start temperature and upper limit
    for i in range(0,len(temperature)):
        if temperature[i] > T_upper_limit:
            T_cooling[i] = T_upper_limit - T_lower_limit
        else:
            T_cooling[i] = T_cooling[i]
    
    cooling_range = np.amax(T_cooling, axis=0)
    load_technology = np.zeros(len(T_cooling))

    # find flh
    for i in range(0,len(T_cooling)):
        load_technology[i] = T_cooling[i] / cooling_range
    flh = sum(load_technology)
    return T_upper_limit,T_cooling,flh

# Make sure while loop starts
flh = flh_required - 1.

# Iterate, lower upper limit until flh_required is reached
while flh < flh_required:
    T_upper_limit, T_cooling, flh = find_Tcooling_max(T_upper_limit, T_cooling)

# Normalize to a sum of 1/3600
hourly_data = T_cooling
hourly_data = hourly_data / sum(hourly_data) / 3600


# Communicate with user
print("Full load hours of cooling technology = " + str(round(flh,1)))
print("Cooling starts at " + str(T_lower_limit))
print("Cooling ends at = " + str(T_upper_limit))
print("Maximum temperature drop = " + str(T_upper_limit-T_lower_limit))

# #Plot if required
subplot(1,2,1)
plt.plot(temperature[0:24*365], 'b-')
plt.axhline(y=T_lower_limit, color='r', linestyle='-')
plt.axhline(y=T_upper_limit, color='r', linestyle='-')
plt.xlabel('time (hours)')
plt.ylabel('temperature (degrees C)')
plt.title("Temperature curve " + country + " " + year)

subplot(1,2,2)
plt.plot(T_cooling[0:24*365], 'b-')
plt.title("Cooling curve " + country + " " + year)
plt.xlabel('time (hours)')
plt.xlim(0,8760)
plt.ylabel('Cooling temperature (degrees C)')
plt.show()


