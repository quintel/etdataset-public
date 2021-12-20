# -*- coding: utf-8 -*-
import numpy as np
import os
import pylab as plt
from scipy.optimize import minimize
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

house_type = "Vrijstaande woning"

# Data for temperature (hourly)
temperature_1987 = np.genfromtxt(os.getcwd() + "/input_data/hourly_temperature_1987_v3.csv", delimiter=",") # degrees C

# Data for solar irradiation
irradiation_1987 = np.genfromtxt(os.getcwd() + "/input_data/hourly_irradiation_1987.csv", delimiter=",") # J/cm^2
irradiation_1987 = irradiation_1987 * J_to_kWh / cm2_to_m2 # kWh/m^2


def heating_demand(params, house_type, insulation_level):


    house_data = {
        'r_values': {house_type :{"low": params[0], "medium": params[1], "high": params[2]}},
        'heat_capacity': {house_type: insulation_data.heat_capacity_values[house_type]},
        'surface_area': {house_type: insulation_data.surface_area_values[house_type]},
        'window_area': {house_type: params[3]},
        'thermostat_vectors': insulation_data.thermostat_values,
        'behaviour': {
            house_type: {"low": params[4], "medium": params[5], "high": params[6]}            }
        }

    # Define house object
    my_house = insulation_classes.House(house_data,house_type,insulation_level)
    #my_house.info()

    # Calculating heating demand
    heating_demand = []

    for hour in range(0, hours_per_year):

        # What is the wanted temperature inside?
        hour_of_the_day = hour % hours_per_day # between 0 and 23

        #Calling the heat demand function of the house object
        needed_heating_demand = my_house.calculate_heat_demand(
                                                                        temperature_1987[hour],
                                                                        irradiation_1987[hour],
                                                                        hour_of_the_day)
        # Adding demand to the vector
        heating_demand.append(needed_heating_demand)

    return heating_demand


def object_function(params):

    differences = [
                np.sum(np.abs( heating_demand(params,house_type,'low') - insulation_data.heat_demand_profiles_dictionary[house_type]['low'])),
                np.sum(np.abs( heating_demand(params,house_type,'medium') - insulation_data.heat_demand_profiles_dictionary[house_type]['medium'] )),
                np.sum(np.abs( heating_demand(params,house_type,'high') - insulation_data.heat_demand_profiles_dictionary[house_type]['high'] ))]

    err_sum = np.sum(differences)

    return err_sum

initial_guess = [
insulation_data.r_values[house_type]["low"],
insulation_data.r_values[house_type]["medium"],
insulation_data.r_values[house_type]["high"],
 6.0,
 3.0,
 1.0,
 -1.0]

print("Fitting...")

res = minimize(object_function, initial_guess, method = 'Nelder-Mead')

print("result: ", res)

print("Relative errors: ")
print("Low: ", np.sum(np.abs(heating_demand(res.x,house_type,'low') - insulation_data.heat_demand_profiles_dictionary[house_type]['low'])) / np.sum(insulation_data.heat_demand_profiles_dictionary[house_type]['low']))
print("Medium: ", np.sum(np.abs(heating_demand(res.x,house_type,'medium') - insulation_data.heat_demand_profiles_dictionary[house_type]['medium'])) / np.sum(insulation_data.heat_demand_profiles_dictionary[house_type]['medium']))
print("High: ", np.sum(np.abs(heating_demand(res.x,house_type,'high') - insulation_data.heat_demand_profiles_dictionary[house_type]['high'])) / np.sum(insulation_data.heat_demand_profiles_dictionary['Tussenwoning']['high']))

# plotting
plt.close('all')
plt.figure(figsize=(20,10))
# plt.subplot(2, 1, 1)
# plt.semilogy(error_sum_list, label='Tussenwoning low')
# plt.legend()
# plt.xlabel('iteration')
# plt.ylabel('Heat demand error (%)')

# plotting
max_hour = 10*24
plt.close('all')
plt.figure(figsize=(20,10))

plt.subplot(2, 2, 1)
plt.plot(insulation_data.heat_demand_profiles_dictionary[house_type]['low'][0:max_hour], label='ECN ' + house_type + ' low')
plt.plot(heating_demand(res.x,house_type,'low')[0:max_hour], label='Constructed')
plt.legend()
plt.xlabel('time (hour)')
plt.ylabel('Heat demand (kW)')

plt.subplot(2, 2, 2)
plt.plot(insulation_data.heat_demand_profiles_dictionary[house_type]['medium'][0:max_hour], label='ECN ' + house_type + ' medium')
plt.plot(heating_demand(res.x,house_type,'medium')[0:max_hour], label='Constructed')
plt.legend()
plt.xlabel('time (hour)')
plt.ylabel('Heat demand (kW)')

plt.subplot(2, 2, 3)
plt.plot(insulation_data.heat_demand_profiles_dictionary[house_type]['high'][0:max_hour], label='ECN ' + house_type + ' high')
plt.plot(heating_demand(res.x,house_type,'high')[0:max_hour], label='Constructed')
plt.legend()
plt.xlabel('time (hour)')
plt.ylabel('Heat demand (kW)')

plt.subplot(2, 2, 4)
plt.plot(insulation_data.heat_demand_profiles_dictionary[house_type]['high'][0:max_hour]-heating_demand(res.x,house_type,'high')[0:max_hour], label='difference high')
plt.plot(insulation_data.heat_demand_profiles_dictionary[house_type]['medium'][0:max_hour]-heating_demand(res.x,house_type,'medium')[0:max_hour], label='difference medium')
plt.plot(insulation_data.heat_demand_profiles_dictionary[house_type]['low'][0:max_hour]-heating_demand(res.x,house_type,'low')[0:max_hour], label='difference low')
plt.legend()
plt.xlabel('time (hour)')
plt.ylabel('Heat demand (kW)')


plt.show()

#plt.savetxt(os.getcwd() + "/hourly_temperuture_1987.csv", temperature_1987, fmt='%.10e', delimiter=',')
