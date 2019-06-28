import os
import sys

import csv
import getpass

import matplotlib.pyplot as plt
import numpy as np

os.chdir('./../')


def main(args):
    # Specify the country and year when calling this script in the terminal
    # e.g. python process_wind_generation_source_data.py nl 2015
    country = args[0]
    year = args[1]

    wind_types = ["offshore", "inland", "coastal"]
    # limits = ["min", "max"]
    limits = ["min"]
    required_max_flhs = {'offshore': 6500, 'inland': 3500, 'coastal': 4500}
    tolerance = 1.0e-6
    max_iterations = 100

    # Initialise plot
    plt.close()
    fig, ax = plt.subplots(figsize=(25,10))
    plt.subplot(1,1,1)
    plt.title("Wind production")
    plt.xlabel("time (hours)")
    plt.ylabel("MW")

    for wind_type in wind_types:
        try:
            file_path = '{}/data/{}/{}/input/wind_{}.csv'.format(os.getcwd(), country, year, wind_type)
            datafile = open(file_path, 'r')

            # Converting the curves to a numpy array
            wind_curve = np.genfromtxt(datafile, delimiter = ',')
            wind_curve = wind_curve / wind_curve.max()

            full_load_hours = np.sum(wind_curve)

            # FLHs according to the dataset
            flh_file_path = '/Users/{}/Projects/etsource/datasets/{}/central_producers.csv'.format(getpass.getuser(), country)

            csv_file = csv.reader(open(flh_file_path, "rb"), delimiter=",")

            for row in csv_file:

                if "energy_power_wind_turbine_"+wind_type == row[0]:
                    flh_from_dataset = float(row[2])

            #### Plotting curves
            plt.plot(np.array(range(0,8760)), wind_curve, label=wind_type+"_"+country+": {:.0f}".format(full_load_hours)+", from dataset: {:.0f}".format(flh_from_dataset) )

            for limit in limits:

                # Scaling profile to desired FLHs
                if limit == "max":
                    target_flh = required_max_flhs[wind_type]
                else:
                    target_flh = flh_from_dataset

                if full_load_hours < target_flh:
                    approach = "cut_from_top"
                else:
                    approach = "cut_from_bottom"

                rel_error = float('inf')
                chop_size = 0.5
                chop = chop_size
                current_flh = full_load_hours

                i = 0
                while np.abs(rel_error - 1.0) > tolerance and i < max_iterations:

                    if approach == "cut_from_top":
                        # Cut off from top
                        chopped_wind_curve = np.where((wind_curve > chop) , chop, wind_curve)
                    else:
                        # Cut off from bottom
                        chopped_wind_curve = np.where((wind_curve > (1.0 - chop)) , wind_curve - (1.0 - chop), 0.0)

                    current_flh = np.sum(chopped_wind_curve) / chop

                    chop_size /= 2.0
                    if current_flh > target_flh:
                        if approach == "cut_from_top":
                            chop += chop_size
                        else:
                            chop -= chop_size
                    else:
                        if approach == "cut_from_top":
                            chop -= chop_size
                        else:
                            chop += chop_size

                    rel_error = current_flh / target_flh
                    print "iteration : ",i
                    print "full load hours: ", current_flh, "(", rel_error * 100, "%)"

                    i += 1.0

                if i == max_iterations:

                    print "Failed to converge!"
                    print "Country: ", country
                    print "Type: ", wind_type
                    print "Extreme: ", limit
                    print "Approach: ", approach
                    sys.exit(0)
                else:
                    print "Converged with chop: ", chop

                # Scaling chopped wind_curve
                chopped_wind_curve /= chop
                new_full_load_hours = np.sum(chopped_wind_curve)

                #### Plotting curves
                plt.plot(np.array(range(0,8760)), chopped_wind_curve, label=limit+"_"+wind_type+"_"+country+": {:.0f}".format(new_full_load_hours) )

                # Writing profile to file
                normalised_wind_curve = chopped_wind_curve / (3600.0 * new_full_load_hours)

                # out_file = open('{}/data/{}/{}/output/wind_{}_{}.csv'.format(os.getcwd(), country, year, wind_type, limit),'w')
                out_file = open('{}/data/{}/{}/output/wind_{}_baseline.csv'.format(os.getcwd(), country, year, wind_type, limit),'w')
                np.savetxt(out_file, normalised_wind_curve, delimiter=",")
        except:
            pass

    plt.legend(bbox_to_anchor=[0.8, 0.95])
    plt.show()

if __name__ == "__main__":
    main(sys.argv[1:])
