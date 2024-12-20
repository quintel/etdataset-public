from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from etm_tools.source_analysis import analyse_country

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

if __name__ == '__main__':
    if not len(sys.argv) == 3:
        raise SystemExit(HELP)

    year = sys.argv[1]
    countries = sys.argv[2].split(',')

    if countries[0] == 'EU27_COUNTRIES_AND_TOTAL':
        countries = EU27_COUNTRIES_AND_TOTAL

    for country in countries:
        print(f'Starting country {country}')
        if country not in EU27_COUNTRIES_AND_TOTAL:
            analyse_country(country, year=year, mark='world')
        else:
            analyse_country(country, year=year)
        print(f'{country} done!')
