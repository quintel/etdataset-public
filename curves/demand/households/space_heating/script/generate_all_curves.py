from itertools import count
import sys
import pandas as pd
from pathlib import Path

from heat_demand import generate_profiles

EU_27 = ['AT_austria', 'BE_belgium', 'BG_bulgaria', 'CY_cyprus', 'CZ_czechia', 'DE_germany',
    'DK_denmark', 'EE_estonia', 'ES_spain', 'FI_finland', 'FR_france', 'UK_united_kingdom',
    'EL_greece', 'HR_croatia', 'HU_hungary', 'IE_ireland', 'IT_italy', 'LT_lithuania',
    'LU_luxembourg', 'LV_latvia', 'NL_netherlands', 'PL_poland', 'PT_portugal', 'RO_romania',
    'SE_sweden', 'SI_slovenia', 'SK_slovakia']

# Communicate with the user
if(len(sys.argv) < 3):
    print("Use: python " + str(sys.argv[0]) + "  <year> <country1> <country2> <..>")
    sys.exit(1)

countries = sys.argv[2:]
year = sys.argv[1]
space_heating_folder = Path(__file__).resolve().parents[1]

if countries[0] == 'EU_27':
    countries = EU_27

# Thermostat is the same for everybody
thermostat = pd.read_csv('data/thermostat.csv')

# And go!
for country in countries:
    print(f'Creating curves for {country}')

    country_data = space_heating_folder / 'data' / country / str(year)
    (country_data / 'output').mkdir(parents=True, exist_ok=True)

    irradiation = pd.read_csv(country_data / 'input' / 'irradiation.csv', squeeze=True, header=None)
    temp = pd.read_csv(country_data / 'input' / 'air_temperature.csv', squeeze=True, header=None)

    for curve in generate_profiles(irradiation, temp, thermostat):
        curve.to_csv(country_data / 'output')

    temp.to_csv(country_data / 'output' / 'air_temperature.csv', index=False, header=False)
    print('-- Done!')
