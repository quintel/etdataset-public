# -*- coding: utf-8 -*-
import numpy as np
import os
import sys
import pylab as plt
from matplotlib.colors import LogNorm
import insulation_classes 
reload(insulation_classes)
import insulation_data
reload(insulation_classes)

# General constants
hours_per_year = 8760
days_per_year = 365
hours_per_day = 24
seconds_per_hour = 3600.0
Watts_per_kW = 1000.0
cm2_to_m2 = 1e-4
J_to_kWh = 2.77778e-7

house_types = insulation_data.house_types
house_types_names = ["terraced_houses", "corner_houses", "semi_detached_houses", "apartments", "detached_houses"]
insulation_types = ["low", "medium", "high"]
data_dump = []
i=-1

# Communicate with the user
if(len(sys.argv) != 3):
    print "Use: python " + str(sys.argv[0]) + " <country> <year> "
    sys.exit(1)

else:
    country = sys.argv[1]
    year = sys.argv[2]
    temperature_file_path = "../data/" + country +"/" + year + "/input" + "/air_temperature.csv"
    irradiation_file_path = "../data/" + country +"/" + year + "/input" + "/irradiation.csv"
    output_file_path = "../data/" + country +"/" + year + "/output/"

#temperature_1987 = np.genfromtxt(os.getcwd() + "/input_data/hourly_temperature_1987_v3.csv", delimiter=",") # degrees C
temperature = np.genfromtxt(temperature_file_path, delimiter=",") # degrees C

# Data for solar irradiation
#irradiation_1987 = np.genfromtxt(os.getcwd() + "/input_data/hourly_irradiation_1987.csv", delimiter=",") # J/cm^2
#irradiation_1987 = irradiation_1987 * J_to_kWh / cm2_to_m2 # kWh/m^2
irradiation = np.genfromtxt(irradiation_file_path, delimiter=",") # J/cm^2
irradiation = irradiation * J_to_kWh / cm2_to_m2 # kWh/m^2


for house_type in house_types:
    i=i+1
    for insulation_type in insulation_types:

        # Define house object
        house = insulation_classes.House(insulation_data.house_data, house_type, insulation_type)

        # Calculating heating demand
        heating_demand = []

        for hour in range(0, hours_per_year):

            # What is the wanted temperature inside?
            hour_of_the_day = hour % hours_per_day # between 0 and 23    

            #Calling the heat demand function of the house object
            needed_heating_demand = house.Calculate_heat_demand(
                                                                            temperature[hour],
                                                                            irradiation[hour],
                                                                            hour_of_the_day)

            # Adding demand to the vector
            heating_demand.append(needed_heating_demand)

        

        hourly_data = heating_demand / sum(heating_demand) / 3600
        
        np.savetxt(output_file_path + "insulation" + "_" + house_types_names[i] + "_" + insulation_type + ".csv", hourly_data, fmt='%.13f', delimiter=',')

print "Succesfully written output files to" + output_file_path + " !"
