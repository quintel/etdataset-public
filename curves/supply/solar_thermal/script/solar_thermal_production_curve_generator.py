# -*- coding: utf-8 -*-
import os
import sys
import numpy as np
from matplotlib import pylab as plt
from matplotlib.colors import LogNorm


# General constants
hours_per_year = 8760
seconds_per_hour = 3600.0
cm2_to_m2 = 1e-4
standard_irradiance = 1000

# Technology constants
n0 = 0.838                      #
a1 = 2.46                       #[W/m2k]
a2 = 0.0197                     #[W/m2k2]
aperture_area = 12.56           #[m2]
glass_thickness = 0.0023        #[m]
fluid_volume = 0.0114          #[m3]
efficiency_literature = 0.6     #

glass_density = 2500            # [kg/m3]
glass_specific_heat = 840       # [J/(kg.K)]
fluid_density = 1000            # [kg/m3]
fluid_specific_heat = 4200      # [J/(kg.K)]
glass_volume =  glass_thickness * aperture_area

glass_thermal_capacity = glass_volume * glass_density * glass_specific_heat
fluid_thermal_capacity = fluid_volume * fluid_density * fluid_specific_heat
panel_thermal_capacity = glass_thermal_capacity + fluid_thermal_capacity

Tdiff_set = 48                      #oC (Choosen so that FLH NL2015 = 684)


# Communicate with the user
if(len(sys.argv) != 3):
    print("Use: python " + str(sys.argv[0]) + " <country> <year> ")
    sys.exit(1)

else:
    country = sys.argv[1]
    year = sys.argv[2]
    irradiation_file_path = "../data/" + country +"/" + year + "/input" + "/irradiation.csv"
    output_file_path = "../data/" + country +"/" + year + "/output/"

# Data for solar irradiation
irradiation = np.genfromtxt(irradiation_file_path, delimiter=",") # J/cm^2
irradiation = irradiation / cm2_to_m2 / seconds_per_hour # kW/m^2

# Set parameters
Tdiff = 0
efficiency = 0
efficiency_raw = 0
delta_Tdiff = 0
production = 0
hourly_data = []
production_year = []
power_per_m2 = 0
power_per_m2_year = []

for i in range(0,hours_per_year):

    if ((i+1)/24).is_integer():
        Tdiff = 0
    else:
        if Tdiff + delta_Tdiff > Tdiff_set:
            Tdiff = Tdiff_set
        else:
            Tdiff = Tdiff + delta_Tdiff

    if irradiation[i] == 0:
        efficiency = 0
    else:
        efficiency_raw = n0 - (a1*Tdiff/irradiation[i]) - ((a2*Tdiff*Tdiff)/irradiation[i])
        if efficiency_raw < 0:
            efficiency = 0
        else:
            efficiency = efficiency_raw

    heat_from_sun = irradiation[i] * efficiency * aperture_area * seconds_per_hour

    if Tdiff < Tdiff_set:
        production = 0
        delta_Tdiff = heat_from_sun / panel_thermal_capacity
    else:
        production = heat_from_sun
        power_per_m2 = heat_from_sun / aperture_area / 3600
        delta_Tdiff = 0

    production_year.append(production)
    power_per_m2_year.append(power_per_m2)

production_year = np.array(production_year)
total_production = sum(production_year)
power_per_m2_year = np.array(power_per_m2_year)
total_production_per_m2 = sum(power_per_m2_year)


flh = total_production_per_m2 / (standard_irradiance * efficiency_literature)
print("FLH = " + str(round(flh,1)))

#plt.plot(power_per_m2_year)
#plt.show()

# normalize curve and divide by 3600
hourly_data = production_year / sum(production_year) / 3600.0

np.savetxt(output_file_path + "solar_thermal.csv", hourly_data, fmt='%.10e', delimiter=',')

print("Succesfully written output files to " + output_file_path + " !")
