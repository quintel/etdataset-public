from pathlib import Path

from etm_tools.utils.conversion_map import ConversionMap
from .energy_balance import EnergyBalance
from .converters import (IndustryChemicalConverter, IndustryICTConverter, PowerPlantConverter,
    IndustryMetalConverter, HeatersAndCHPsConverter)
from .input_files import load_powerplants, load_heaters_and_chps
from .full_load_hours import FullLoadHoursCalculator

OUTPUT_PATH = Path(__file__).parents[2] / 'data' / 'energy_balances'

def convert_country(country_name, path_to_energy_balance=None, download_from_eurostat=False,
    year=2019):
    '''
    Applies all conversions to the specified country. Outputs an energy balance file.

    Params:
        path_to_energy_balance (str|Path):   optional, the path to the energy balance csv file
        download_from_eurostat (True|False): If set to True, downloads the energy balance from
                                             eurostat, instead of reading it directy from a csv
        year (int):                          optional, what year to download the EB from eurostat
                                             from

    Ouput is a new energy balance csv
    '''
    if download_from_eurostat:
        nrg_bal = EnergyBalance.from_eurostat(country_name, year)
    elif path_to_energy_balance:
        nrg_bal = EnergyBalance.from_csv(path_to_energy_balance)
    else:
        SystemExit('You need to specify either a path to an energy balance, or allow downloading.')

    cm = ConversionMap()

    ## ORDINARY CONVERTERS ##
    IndustryICTConverter.convert(nrg_bal, **cm.inputs('industry_ict', country_name))
    IndustryMetalConverter.convert(nrg_bal, **cm.inputs('industry_metal', country_name))
    IndustryChemicalConverter.convert(nrg_bal, **cm.inputs('industry_chemical', country_name))

    HeatersAndCHPsConverter.convert(nrg_bal, load_heaters_and_chps())

    ## POWERPLANTS ##
    flh_calculator = FullLoadHoursCalculator()
    powerplant_path = cm.inputs('power_plants', country_name)['path']
    PowerPlantConverter.convert(nrg_bal, country_name, plants=load_powerplants(powerplant_path),
        flh_calc=flh_calculator)


    ## FINISH ##
    year_folder = OUTPUT_PATH / str(year)
    year_folder.mkdir(exist_ok=True, parents=True)

    flh_calculator.to_csv(year_folder / 'full_load_hours.csv', country_name)
    nrg_bal.to_csv(year_folder / f'{country_name}.csv')

