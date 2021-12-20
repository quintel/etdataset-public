import os
import sys
import numpy as np
from matplotlib import pylab as plt
from matplotlib.colors import LogNorm
from pathlib import Path

sys.path.append('../../script_utils')

from renewables_ninja import RenewablesNinja

DATA_FOLDER = '../../solar_thermal'/Path(__file__).parents[0] / 'data'

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


def validate(data):
    # Check for leap year
    number_of_hours = data.shape[0]
    if number_of_hours > 8760:
        data = data.drop(np.r_[8760:number_of_hours])

    # Check for % NaN values
    threshold = 0.02
    missing = data['irradiance_surface'].isnull().sum() / 8760.0
    print(f'-- Data coverage: {(1.0 - missing) * 100}%')

    if missing >= threshold:
        raise SystemExit('WARNING: CURVE IS NOT GENERATED!\n(> 2% missing data points)')

    return data


def normalize(profile): ## moet blijven
    return ( profile / np.sum(profile) ) / 3600.0


def main(args):
    # Specify the country and year when calling this script in the terminal
    # e.g. python3 solar_thermal_production_curve_generator_renewables_ninja.py cz,nl 2019
    countries = args[0].upper().split(',')

    year = args[1]

    ninja_api = RenewablesNinja(year, countries=countries)

    for country, weather_curves in ninja_api.get_all_weather_curves():
        print()
        print(f'Downloading curve for {country}')
        weather_curves = validate(weather_curves)
        irradiation = weather_curves['irradiance_surface']
        
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
        print("-- Full load hours = " + str(round(flh,1)))

        # normalize curve and divide by 3600
        solar_thermal = production_year / sum(production_year) / 3600.0


        export_path = DATA_FOLDER / country / year / 'output'
        export_path.mkdir(parents=True, exist_ok=True)
        export_name = export_path = DATA_FOLDER / country / year / 'output' / 'solar_thermal.csv'
        np.savetxt(export_name, solar_thermal, fmt='%.10e', delimiter=',')
        # solar_thermal.to_csv(export_path/ 'solar_thermal.csv', index=None, header=False)

        print('\033[92m   Curve solar thermal was exported\033[0m')

if __name__ == "__main__":
    main(sys.argv[1:])

