from os import sys, path
from pathlib import Path

# Append the parent directory of the current file to sys.path so that the necessary modules can be imported
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from etm_tools.energy_balance_operations import Runner

# List of EU27 countries and the EU27 total. Used to process all countries in one go if required.
EU27_COUNTRIES_AND_TOTAL = [
    'AT', 'BE', 'BG', 'CY', 'CZ', 'DE', 'DK', 'EE', 'ES', 'FI', 'FR', 'EL', 'HR', 'HU',
    'IE', 'IT', 'LT', 'LU', 'LV', 'MT', 'NL', 'PL', 'PT', 'RO', 'SE', 'SI', 'SK', 'EU27_2020'
]

# Help message that explains the script usage, the input parameters, and options available.
HELP = '''\033[94m
Please use this script with the following arguments:
    - year (arg 1): the analysis year for which to run all conversions
    - countries (arg 2): specify one or more countries (separated by commas, no spaces!)
    - (optional) 'retrieve-only' (arg 3): if provided, only retrieves and saves the CSV from the API without processing. This step is required before running the conversions.

For countries you can also use the special keyword 'EU27_COUNTRIES_AND_TOTAL' to run conversions for
all EU27 countries at once.\033[0m
'''

# The converters that will be applied when using the Eurostat data. The order matters.
EUROSTAT_CONVERSIONS = [
    'industry_ict',
    'industry_metal',
    'industry_chemical',
    'power_plants',
    'chps'
]

# Main entry point of the script
if __name__ == '__main__':
    # Ensure that the script has the correct number of arguments
    if not len(sys.argv) == 3 and not len(sys.argv) == 4:
        raise SystemExit(HELP)

    # Extract the year and countries from the command-line arguments
    year = sys.argv[1]
    countries = sys.argv[2].split(',')

    # Check if the optional "retrieve-only" argument is provided
    retrieve_only = len(sys.argv) == 4 and sys.argv[3].lower() == 'retrieve-only'

    # If the user specifies 'EU27_COUNTRIES_AND_TOTAL', it will run for all EU27 countries
    if countries[0] == 'EU27_COUNTRIES_AND_TOTAL':
        countries = EU27_COUNTRIES_AND_TOTAL

    # Iterate through each country specified in the command-line arguments
    for country in countries:
        print(f'Starting country {country}')

        try:
            # Try to load the raw CSV from local storage
            runner = Runner.load_from_raw_csv(country, year)
            print(f"Raw CSV for {country} in {year} exists. Processing...")

            # If 'retrieve-only' flag is set, skip further processing
            if retrieve_only:
                print(f"Raw CSV for {country} in {year} retrieved and saved. No further processing.")
                continue  # Skip to the next country in the loop

            # If not 'retrieve-only', process the data
            runner.process(*EUROSTAT_CONVERSIONS)

        except FileNotFoundError:

            # Handle the retrieve-only flag
            if retrieve_only:
                runner = Runner.load_from_eurostat(country, year, flag='retrieve-only')
                print(f"Raw CSV for {country} in {year} retrieved and saved. No further processing.")
            else:
                # Fetch and process the data using Eurostat conversions
                print(f"CSV for {country} in {year} not found. Please retrieve the data from Eurostat using the 'retrieve-only' flag.")

        print(f'{country} done')
