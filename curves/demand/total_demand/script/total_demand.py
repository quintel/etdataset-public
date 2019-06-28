import numpy as np
from pylab import *
from numpy import genfromtxt


country_filename = ""

# Communicate with the user
if(len(sys.argv) != 3):
    print "Use: python " + str(sys.argv[0]) + " <country> <year> "
    sys.exit(1)

	
# Import input files
else:
    country = sys.argv[1]
    year = sys.argv[2]
    input_file_path =  "../data/" + country +"/" + year + "/input/"
    output_file_path = "../data/" + country +"/" + year + "/output/"
    print(country)


if(country == "uk"):
	country_filename = "GB"

else:
	country_filename = str(country)
	country_filename = country_filename.upper()


ENTSOE = genfromtxt(input_file_path + country_filename + "_demand_curve.csv")

# Define empty matrices
hourly_data = []

hourly_data = ENTSOE

# normalize curve and divide by 3600
hourly_data = hourly_data / sum(hourly_data) / 3600.0

# Write data to file
np.savetxt(output_file_path + "total_demand" + ".csv", hourly_data, fmt='%.10e', delimiter=',')

print("Succesfully written total_demand output files " + str(country) + " " + str(year) + "!")
