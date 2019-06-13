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


# Define matrix with ones
hourly_data = np.ones(8760)

# normalize curve and divide by 3600
hourly_data = hourly_data / sum(hourly_data) / 3600.0

# Write data to file
np.savetxt(output_file_path + "industry_heat" + ".csv", hourly_data, fmt='%.13f', delimiter=',')

print("Succesfully written output files agriculutre_chp.csv " + str(country) + " " + str(year) + "!")
