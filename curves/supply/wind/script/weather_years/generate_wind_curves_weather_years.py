#import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import csv
from numpy import genfromtxt
#from pylab import *


## Communicate with the user
if(len(sys.argv) !=2):
    print ("Use: python3 " + str(sys.argv[0]) + " <year> ")
    sys.exit(1)

## Import input files
else:
	year = sys.argv[1]
	input_file_path =  "../../data/" + "nl" +"/" + year + "/input/"
	output_file_path = "../../data/" + "nl" +"/" + year + "/output/"


wind_data = pd.read_csv(input_file_path + "wind_measurements.csv")
wind_data /= 10.0 # Convert to m/s

## Define empty matrices
hourly_data_inland = []
hourly_data_coastal = []
hourly_data_offshore = []


## Define turbine types, turbine parameters and weather stations
types = ["inland","coastal","offshore"]

parameters_wind_turbine = {"cut_in_wind_speed": 3.5, "rated_output_wind_speed": 13, "cut_off_wind_speed": 25}

parameters_conversion_hub_height = {
"inland": {"measurement_height": 10, "hub_height": 80, "roughness_factor": 0.143},
"coastal": {"measurement_height": 10, "hub_height": 80, "roughness_factor": 0.143},
"offshore": {"measurement_height": 10, "hub_height": 80, "roughness_factor": 0.07}
}

weather_stations = {
"inland": ["240"],	
"coastal": ["240"],
#"offshore": ["260"]
"offshore": ["320"]
}


number_of_values_moving_average = 4

## Convert wind speed to speed at hub height
def calculate_wind_at_hub_height(parameters_conversion_hub_height, turbine_type, wind_measured):

	return wind_measured * pow(parameters_conversion_hub_height[turbine_type]["hub_height"] / parameters_conversion_hub_height[turbine_type]["measurement_height"], parameters_conversion_hub_height[turbine_type]["roughness_factor"])

## Convert wind speed at hub height to output power
def calculate_output_power(parameters_wind_turbine, wind_speed_at_hub_height):


	if wind_speed_at_hub_height < parameters_wind_turbine["cut_in_wind_speed"]:

		return 0.0

	elif wind_speed_at_hub_height >= parameters_wind_turbine["cut_in_wind_speed"] and wind_speed_at_hub_height < parameters_wind_turbine["rated_output_wind_speed"]:

				
		return ((pow(wind_speed_at_hub_height, 3.0) - pow(parameters_wind_turbine["cut_in_wind_speed"], 3.0)) / (pow(parameters_wind_turbine["rated_output_wind_speed"], 3.0) - pow(parameters_wind_turbine["cut_in_wind_speed"], 3.0)))

	elif wind_speed_at_hub_height >= parameters_wind_turbine["rated_output_wind_speed"] and wind_speed_at_hub_height < parameters_wind_turbine["cut_off_wind_speed"]:

		return 1

	else:

		return 0.0

#print(calculate_wind_at_hub_height(parameters_conversion_hub_height, "offshore", 6.0))

## Calculate flh
def calculate_flh(parameters_wind_turbine, power_output_array):

	return sum(power_output_array)


power = {}

for turbine_type in types:

	output_power_array = []

	#print(turbine_type)

	for weather_station in weather_stations[turbine_type]:

		#print(weather_station)


		wind_at_hub_height = calculate_wind_at_hub_height(parameters_conversion_hub_height, turbine_type, wind_data[weather_station])

		output_power = [calculate_output_power(parameters_wind_turbine, x) for x in wind_at_hub_height]

		output_power_array.append(output_power)
		output_power_array = np.transpose(output_power_array)


		# Smooth curve with moving average
		N = number_of_values_moving_average
		cumsum, moving_aves = [0], []

		for i, x in enumerate(output_power_array, 1):
			cumsum.append(cumsum[i-1] + x)
			if i>=N:
				moving_ave = (cumsum[i] - cumsum[i-N])/N
				moving_aves.append(moving_ave)
			else:
				moving_aves.append(output_power_array[i])

		output_power_array_smooth = moving_aves

		flh = calculate_flh(parameters_wind_turbine, output_power)
		# print(turbine_type + " " + weather_station + " has " + str(round(flh)) + " flh")
	
	power[turbine_type] = output_power_array_smooth


flhs = [calculate_flh(parameters_wind_turbine, power[turbine_type]) for turbine_type in types]
flhs = np.round(np.array(flhs),1)


# Create normalized curve for all three turbine types
hourly_data_inland = power["inland"] / sum(power["inland"]) / 3600.0
hourly_data_coastal = power["coastal"] / sum(power["coastal"]) / 3600.0
hourly_data_offshore = power["offshore"] / sum(power["offshore"]) / 3600.0


## Write data to file
np.savetxt(output_file_path + "wind_inland_baseline.csv", hourly_data_inland, fmt='%.10e', delimiter=',')
np.savetxt(output_file_path + "wind_coastal_baseline.csv", hourly_data_coastal, fmt='%.10e', delimiter=',')
np.savetxt(output_file_path + "wind_offshore_baseline.csv", hourly_data_offshore, fmt='%.10e', delimiter=',')


# print("Succesfully written output files " + " " + str(year) + "!")

print("flh inland: " + str(flhs[0]))
print("flh coastal: " + str(flhs[1]))
print("flh offshore: " + str(flhs[2]))
print("Finished - wind curves written to output folder of NL " + year)
