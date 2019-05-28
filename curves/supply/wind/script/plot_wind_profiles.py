import matplotlib.pyplot as plt
import numpy as np
import sys
import csv

countries = ["be", "nl", "es", "uk", "pl", "br", "de", "fr"]
#countries = ["nl"]
#wind_types = ["offshore", "inland", "coastal"]
wind_types = ["inland"]
required_flhs = {'offshore': 6500, 'inland': 3500, 'coastal': 4500}

# Initialise plot
plt.close()
fig, ax = plt.subplots(figsize=(25,10))
plt.subplot(1,1,1)
plt.title("Wind production")
plt.xlabel("time (hours)")
plt.ylabel("MW")

for country_code in countries:

    for wind_type in wind_types:

        file_path = "/Users/kruip/Projects/etsource/datasets/"+country_code+"/load_profiles/wind_"+wind_type+".csv"
        datafile = open(file_path, 'r')

        # Converting the curves to a numpy array
        wind_curve = np.genfromtxt(datafile, delimiter = ',')
        wind_curve = wind_curve / wind_curve.max() 

        full_load_hours = np.sum(wind_curve)

        # FLHs according to the dataset
        flh_file_path = "/Users/kruip/Projects/etsource/datasets/"+country_code+"/central_producers.csv"

        csv_file = csv.reader(open(flh_file_path, "rb"), delimiter=",")

        for row in csv_file:

            if "energy_power_wind_turbine_"+wind_type == row[0]:
                flh_from_dataset = row[2]

        #### Plotting curves
        plt.plot(np.array(range(0,8760)), wind_curve, label=wind_type+"_"+country_code+": {:.0f}".format(full_load_hours)+", from dataset: {:.0f}".format(float(flh_from_dataset)) )

plt.legend(bbox_to_anchor=[0.8, 0.95])
plt.show()