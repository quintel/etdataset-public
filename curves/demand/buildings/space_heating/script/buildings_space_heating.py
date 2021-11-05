import sys
import pandas as pd
from pathlib import Path
from helpers import (find_text_file,
                     find_csv_file,
                     find_header,
                     check_length,
                     calculate_profile_fraction)

if len(sys.argv) != 3:
    print(f"Use: python {sys.argv[0]} <country> <year>")
    sys.exit(1)

else:
    country = sys.argv[1]
    year = sys.argv[2]

# path to space_heating folder
PARENT_FOLDER = Path(__file__).resolve().parents[1]
BUILDINGS_FOLDER = f'{PARENT_FOLDER}/data/{country}/{year}'
AGRICULTURE_FOLDER = (Path(__file__).resolve().parents[3] / 'agriculture' /
                      'heat' / 'data' / f'{country}/{year}')
WEATHER_DATA_FILE = find_csv_file(f'{BUILDINGS_FOLDER}/input')
PARAMETER_FILE = f'{PARENT_FOLDER}/script/input_data/g2a_parameters.csv'

# Extract header and comments from data file
# headers, skip_lines = find_header(WEATHER_DATA_FILE)

# Read data
weather_data = pd.read_csv(WEATHER_DATA_FILE)

# Add year column
weather_data['YYYYMMDD'] = weather_data['YYYYMMDD'].astype(str)
weather_data['year'] = weather_data['YYYYMMDD'].str[0:4]
# Remove data from other year than specified
weather_data = weather_data[weather_data['year'] == year]
# If year is a leap year, remove last day
weather_data['monthday'] = weather_data['YYYYMMDD'].str[4:]
if pd.Timestamp(year).is_leap_year:
    weather_data = weather_data[~(weather_data['monthday'] == '1231')]
# Check whether data has 8760 data points
check_length(weather_data)

# Compute daily averages
daily_averages = weather_data[['monthday', 'T', 'FH']].groupby(
    weather_data['monthday']).mean().rename(
    columns={'T': 'daily_average_T', 'FH': 'daily_average_FH'})

# Add daily averages to weather_data
weather_data.set_index('monthday', inplace=True)
weather_data = weather_data.join(daily_averages)

# Add effective temperature
# Effective temperature is defined as daily average temperature (in C)
# Minus (daily average wind speed (in ms/s) divided by 1.5)
# Divide by 10 because temp and windspeed unit is decimals in the input data
weather_data['Teff'] = (weather_data['daily_average_T']
                        - (weather_data['daily_average_FH'] / 1.5)) / 10

# Now that we have the effective daily temperature for each hour
# we can calculate the profile fraction using the parameter file
parameters = pd.read_csv(PARAMETER_FILE, usecols=[
                         'G2A_TST', 'G2A_RER', 'G2A_TOP'])

# Add parameters to weather_data
weather_data = pd.concat([weather_data.reset_index(
    drop=True), parameters.reset_index(drop=True)], axis=1)

# Add profile fraction
weather_data['profile_fraction'] = weather_data.apply(
    lambda x: calculate_profile_fraction(
        x['Teff'], x['G2A_TST'], x['G2A_RER'], x['G2A_TOP']), axis=1)

# Normalise to 1/3600
weather_data['normalised_profile'] = weather_data['profile_fraction'] / \
    weather_data['profile_fraction'].sum() / 3600
check_length(weather_data['normalised_profile'])

try:
    weather_data['normalised_profile'].to_csv(
        f'{BUILDINGS_FOLDER}/output/buildings_heating.csv',
        index=False, header=False)

    weather_data['normalised_profile'].to_csv(
        f'{AGRICULTURE_FOLDER}/output/agriculture_heating.csv',
        index=False, header=False)

    print((f'Profile for {year} exported to '
          f'{BUILDINGS_FOLDER}/output/buildings_heating.csv\n'))
    print((f'Profile for {year} exported to '
          f'{AGRICULTURE_FOLDER}/output/agriculture_heating.csv\n'))
except BaseException:
    print('Error')
