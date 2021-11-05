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
    output_file_path = "../data/" + country +"/" + year + "/output/"


# Define matrix with ones
hourly_data = np.ones(8760)

# normalize curve and divide by 3600
hourly_data = hourly_data / sum(hourly_data) / 3600.0

# Write data to file
output_path = Path(output_file_path)
output_path.mkdir(parents=True, exist_ok=True)
np.savetxt(output_path / "river.csv", hourly_data, fmt='%.10e', delimiter=',')

print("Succesfully written output files river.csv " + str(country) + " " + str(year) + "!")
