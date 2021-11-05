import sys
import numpy as np

# Communicate with the user
if(len(sys.argv) != 3):
    print("Use: python " + str(sys.argv[0]) + " <country> <year> ")
    sys.exit(1)

# Import input files
else:
    country = sys.argv[1]
    year = sys.argv[2]
    input_file_path =  "../data/" + country +"/" + year + "/input/"
    output_file_path = "../data/" + country +"/" + year + "/output/"

data_e1A = np.genfromtxt(input_file_path + "EDSN_E1A.csv")

# Define empty matrices
hourly_data = []

# Calculate hourly demand from 15-min data
for i in range(0,8760):

    mean = np.sum(data_e1A[i * 4:i * 4 + 4])
    hourly_data.append(mean)

hourly_data = np.array(hourly_data)

# Normalize curve and divide by 3600
hourly_data = hourly_data / sum(hourly_data) / 3600.0

# Write data to file
np.savetxt(output_file_path + "households_cooling.csv", hourly_data, fmt='%.10e', delimiter=',')

print("Succesfully written output files " + str(country) + " " + str(year) + "!")
