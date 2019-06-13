import matplotlib.pyplot as plt
import numpy as np
import sys
import csv

#countries = ["be", "nl", "es", "uk", "pl", "br", "de", "fr"]
countries = ["nl"]
#wind_types = ["offshore", "inland", "coastal"]
wind_types = ["offshore"]
required_flhs = {'offshore': 6500, 'inland': 3500, 'coastal': 4500}

# This toggles the (incorrect) ETM behaviour
etm_behaviour = True

# Initialise plot
plt.close()
fig, ax = plt.subplots(figsize=(25,10))
plt.subplot(1,1,1)
plt.title("Peak capacity deviation")
plt.xlabel("Slider setting (FLHs)")
plt.ylabel("%")

for country_code in countries:

    for wind_type in wind_types:

        #file_path = "/Users/kruip/Projects/etsource/datasets/"+country_code+"/load_profiles/wind_"+wind_type+"_baseline.csv"
        file_path = "./output/"+country_code+"_"+wind_type+"_min.csv"
        datafile = open(file_path, 'r')

        # Converting the curves to a numpy array
        min_wind_curve = np.genfromtxt(datafile, delimiter = ',')
        min_wind_curve = min_wind_curve / min_wind_curve.max() 
        min_full_load_hours = np.sum(min_wind_curve)

        file_path = "./output/"+country_code+"_"+wind_type+"_max.csv"
        datafile = open(file_path, 'r')

        # Converting the curves to a numpy array
        max_wind_curve = np.genfromtxt(datafile, delimiter = ',')
        max_wind_curve = max_wind_curve / max_wind_curve.max() 
        max_full_load_hours = np.sum(max_wind_curve)

        if etm_behaviour:

            min_wind_curve /= (min_full_load_hours * 3600.0)
            max_wind_curve /= (max_full_load_hours * 3600.0)

        slider_setting = []
        peak_capacity = []
        flhs_interpolated_curve = []
        delta = max_full_load_hours - min_full_load_hours
        for i in range(int(min_full_load_hours), int(max_full_load_hours), 1):

            interpolation_factor = (float(i) - min_full_load_hours) / delta
            interpolated_curve = (1.0 - interpolation_factor) * min_wind_curve + interpolation_factor * max_wind_curve

            if etm_behaviour:
                interpolated_curve *= 3600.0 * float(i)

            max_interpolated_curve = np.max(interpolated_curve)

            slider_setting.append(i)
            peak_capacity.append(max_interpolated_curve)
            flhs_interpolated_curve.append(np.sum(interpolated_curve))

        plt.plot(np.array(slider_setting), 100*(np.array(peak_capacity)-1.0), label=country_code )
        #plt.plot(np.array(slider_setting), flhs_interpolated_curve, label=country_code )
        # plt.plot(min_wind_curve, label=country_code+"_min: "+str(min_full_load_hours))
        # plt.plot(max_wind_curve, label=country_code+"_max: "+str(max_full_load_hours))
        # plt.plot(0.5 * min_wind_curve + 0.5 * max_wind_curve, label=country_code+"_mix: "+str(np.sum(0.5 * min_wind_curve + 0.5 * max_wind_curve)))        

plt.legend(bbox_to_anchor=[0.8, 0.95])
plt.show()