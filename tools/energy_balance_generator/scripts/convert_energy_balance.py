from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from etm_tools.energy_balance_operations import Runner

EU27_COUNTRIES_AND_TOTAL = [
  'AT','BE','BG','CY','CZ','DE','DK','EE','ES','FI','FR','EL','HR','HU',
  'IE','IT','LT','LU','LV','MT','NL','PL','PT','RO','SE','SI','SK','EU27_2020']

HELP = '''\033[94m
Please use this script with the following arguments:
    - year (arg 1): the analysis year for which to run all conversions
    - countries (arg 2): specify one or more countries (separated by commas, no spaces!)

For countries you can also use the special keyword 'EU28' to run conversions for
all EU28 countries at once.\033[0m
'''

# Call the eurostat converters in this order:
EUROSTAT_CONVERSIONS = [
    'industry_ict',
    'industry_metal',
    'industry_chemical',
    'power_plants',
    'chps'
]

# Call the world converters in this order:
WORLD_CONVERSIONS = [
    'split_transformation',
    'turn_positive',
    'append_world_chps',
    'industry_ict'
]

if __name__ == '__main__':
    if not len(sys.argv) == 3:
        raise SystemExit(HELP)

    year = sys.argv[1]
    countries = sys.argv[2].split(',')

    if countries[0] == 'EU27_COUNTRIES_AND_TOTAL':
        countries = EU27_COUNTRIES_AND_TOTAL

    for country in countries:
        print(f'Starting country {country}')

        if country in EU27:
            runner = Runner.load_from_eurostat(country, year)
            runner.process(*EUROSTAT_CONVERSIONS)
        else:
            runner = Runner.load_from_world_csv(country, year)
            runner.process(*WORLD_CONVERSIONS)

        print(f'{country} done!')
