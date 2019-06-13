import numpy as np
from pylab import *
from numpy import genfromtxt

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

data_G2A = genfromtxt(input_file_path + "G2A.csv")

# Define empty matrices
hourly_data = []
hourly_data = data_G2A

# normalize curve and divide by 3600
hourly_data = hourly_data / sum(hourly_data) / 3600.0

# Write data to file
np.savetxt(output_file_path + "buildings_heating" + ".csv", hourly_data, fmt='%.13f', delimiter=',')
np.savetxt(output_file_path + "buildings_chp" + ".csv", hourly_data, fmt='%.13f', delimiter=',')


print("Succesfully written output files buildings_heating.csv and buildings_chp.csv " + str(country) + " " + str(year) + "!")
