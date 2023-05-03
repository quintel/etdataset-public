import sys
import numpy as np
from pathlib import Path

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

data_e3d = np.genfromtxt(input_file_path + "e3d.csv")

# Define empty matrices
hourly_data = []

# Calculate hourly demand
for i in range(0,8760):

    mean = np.sum(data_e3d[i * 4:i * 4 + 4])
    hourly_data.append(mean)

hourly_data = np.array(hourly_data)

# Normalize curve and divide by 3600
hourly_data = hourly_data / sum(hourly_data) / 3600.0

# Write data to file
output_path = Path(output_file_path)
output_path.mkdir(parents=True, exist_ok=True)
np.savetxt(output_path / "industry_other_electricity.csv", hourly_data, fmt='%.10e', delimiter=',')

print("Succesfully written output files industry_other_electricity.csv " + str(country) + " " + str(year) + "!")
