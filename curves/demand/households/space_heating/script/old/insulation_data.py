import numpy as np
import os
from pathlib import Path

# Thermostate settings from ECN
thermostat_low = [15.8, 15.8, 15.8, 15.8, 15.8, 15.8, 18.5, 18.5, 18.5, 18.5, 18.5, 18.5, 18.5, 18.5, 18.5, 18.5, 18.5, 19.5, 19.5, 19.5, 19.5, 19.5, 19.5, 15.8]
thermostat_medium = [18, 18, 18, 18, 18, 18, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 20.5, 20.5, 20.5, 20.5, 20.5, 20.5, 18]
thermostat_high = [21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21]
thermostat_values = {'high': thermostat_high, 'medium': thermostat_medium, 'low': thermostat_low}


house_types = ["Tussenwoning", "Hoekwoning", "Twee-onder-een-kapwoning", "Appartement", "Vrijstaande woning"]
insulation_levels = ["low", "medium", "high"]

# All heat demand profiles from ECN
heat_demand_profiles = np.transpose(np.genfromtxt(Path(__file__).parent / "input_data" / "heat_demands.csv", delimiter=","))

heat_demand_profiles_dictionary = {
"Tussenwoning": {"low": heat_demand_profiles[0], "medium": heat_demand_profiles[1], "high": heat_demand_profiles[2]},
"Hoekwoning": {"low": heat_demand_profiles[3], "medium": heat_demand_profiles[4], "high": heat_demand_profiles[5]},
"Twee-onder-een-kapwoning": {"low": heat_demand_profiles[6], "medium": heat_demand_profiles[7], "high": heat_demand_profiles[8]},
"Appartement": {"low": heat_demand_profiles[9], "medium": heat_demand_profiles[10], "high": heat_demand_profiles[11]},
"Vrijstaande woning": {"low": heat_demand_profiles[12], "medium": heat_demand_profiles[13], "high": heat_demand_profiles[14]}
}

# Material constants
density_concrete = 2400.0 # kg / m**3 (https://en.wikipedia.org/wiki/Properties_of_concrete)
specific_heat_capacity_concrete = 880.0 # J / kg K (https://www.designingbuildings.co.uk/wiki/Specific_heat_capacity)

J_to_kWh = 2.77778e-7

# Define tussenwoning_low_data
R_c = 0.76 # [m^2 K / W]
width = 8.0 #m
height = 4.0 #m
wall_thickness = 0.025
roof_area = width * width
wall_area = width * height
window_area = roof_area * 0.1
surface_area = wall_area * 4 + roof_area # m^2 Assuming a square house with a flat roof for now
kg_of_concrete = surface_area * wall_thickness * density_concrete # cubic meter of wall times the specific weight of concrete

# How much energy does it take to heat the house one K?
heat_capacity_house = specific_heat_capacity_concrete * J_to_kWh * kg_of_concrete # kWh / K

heat_capacity_values = {
    "Tussenwoning": heat_capacity_house,
    "Hoekwoning": heat_capacity_house,
    "Twee-onder-een-kapwoning": heat_capacity_house,
    "Appartement": heat_capacity_house,
    "Vrijstaande woning": heat_capacity_house
}

surface_area_values = {
    "Tussenwoning": 183,
    "Hoekwoning": 239,
    "Twee-onder-een-kapwoning": 279,
    "Appartement": 187,
    "Vrijstaande woning": 405
}


fitting_results = { # R-laag, R-midden, R-hoog, window area, behaviour-laag, behaviour-midden, behaviour-hoog
"Tussenwoning": [ 0.72608224,  0.95303516,  2.20833951,  6.08289109,  0.44224575, 2.61042431,  0.59483274],
"Hoekwoning": [ 0.86234292,  1.05413341,  2.73029519,  5.53694918,  1.63456613, 4.84495401,  0.96159576],
"Twee-onder-een-kapwoning": [ 0.92629934,  1.20779267,  2.90413756,  5.80327128,  1.57962902, 4.43499574,  0.45485638],
"Appartement": [ 0.96937942,  1.39716924,  2.95000949,  5.53039382, -0.11691841, 0.80467653,  2.78210071],
"Vrijstaande woning":  [1.02227109,  1.2962618,  3.10765405,  6.12774164,  3.34031291, 7.76537119,  2.74614981]
}

# ECN R-values [m^2 K / W]
# ecn_r_values = {
# "Tussenwoning": {"low": 0.306, "medium": 1.522, "high": 4.236},
# "Hoekwoning": {"low": 0.327, "medium": 1.454, "high": 4.369},
# "Twee-onder-een-kapwoning": {"low": 0.324, "medium": 1.483, "high": 4.346},
# "Appartement": {"low": 0.301, "medium": 1.694, "high": 4.400},
# "Vrijstaande woning": {"low": 0.329, "medium": 1.545, "high": 4.455}
# }

# R-values [m^2 K / W] (from fitting)
r_values = {
"Tussenwoning": {"low": fitting_results["Tussenwoning"][0], "medium": fitting_results["Tussenwoning"][1], "high": fitting_results["Tussenwoning"][2]},
"Hoekwoning": {"low": fitting_results["Hoekwoning"][0], "medium": fitting_results["Hoekwoning"][1], "high": fitting_results["Hoekwoning"][2]},
"Twee-onder-een-kapwoning": {"low": fitting_results["Twee-onder-een-kapwoning"][0], "medium": fitting_results["Twee-onder-een-kapwoning"][1], "high": fitting_results["Twee-onder-een-kapwoning"][2]},
"Appartement": {"low": fitting_results["Appartement"][0], "medium": fitting_results["Appartement"][1], "high": fitting_results["Appartement"][2]},
"Vrijstaande woning": {"low": fitting_results["Vrijstaande woning"][0], "medium": fitting_results["Vrijstaande woning"][1], "high": fitting_results["Vrijstaande woning"][2]}
}

window_area_values = {
    "Tussenwoning": fitting_results["Tussenwoning"][3],
    "Hoekwoning": window_area,
    "Twee-onder-een-kapwoning": window_area,
    "Appartement": window_area,
    "Vrijstaande woning": window_area
}

behaviour = {
"Tussenwoning": {"low": fitting_results["Tussenwoning"][4], "medium": fitting_results["Tussenwoning"][5], "high": fitting_results["Tussenwoning"][6]},
"Hoekwoning": {"low": fitting_results["Hoekwoning"][4], "medium": fitting_results["Hoekwoning"][5], "high": fitting_results["Hoekwoning"][6]},
"Twee-onder-een-kapwoning": {"low": fitting_results["Twee-onder-een-kapwoning"][4], "medium": fitting_results["Twee-onder-een-kapwoning"][5], "high": fitting_results["Twee-onder-een-kapwoning"][6]},
"Appartement": {"low": fitting_results["Appartement"][4], "medium": fitting_results["Appartement"][5], "high": fitting_results["Appartement"][6]},
"Vrijstaande woning": {"low": fitting_results["Vrijstaande woning"][4], "medium": fitting_results["Vrijstaande woning"][5], "high": fitting_results["Vrijstaande woning"][6]}
}


house_data = {
    'r_values': r_values,
    'heat_capacity': heat_capacity_values,
    'surface_area': surface_area_values,
    'window_area': window_area_values,
    'thermostat_vectors': thermostat_values,
    'behaviour': behaviour
    }

