from pathlib import Path
import inspect
from etm_tools.utils.conversion_map import ConversionMap
from .energy_balance.load import Load
from .energy_balance import EnergyBalance
from .converters import *
from .input_files import load_powerplants, load_heaters, load_world_chps
from .chp_capacities import CHPCapacities
from .chp_producers import CHPProducers
from .full_load_hours import FullLoadHoursCalculator

COUNTRY_FOLDER_MAPPING = {
    'AT': 'AT_austria',
    'BE': 'BE_belgium',
    'BG': 'BG_bulgaria',
    'CH': 'CH_switzerland',
    'CY': 'CY_cyprus',
    'CZ': 'CZ_czechia',
    'DE': 'DE_germany',
    'DK': 'DK_denmark',
    'EE': 'EE_estonia',
    'EU27_2020': 'EU27_european_union',
    'ES': 'ES_spain',
    'FI': 'FI_finland',
    'FR': 'FR_france',
    'EL': 'EL_greece',
    'HR': 'HR_croatia',
    'HU': 'HU_hungary',
    'IE': 'IE_ireland',
    'IT': 'IT_italy',
    'LT': 'LT_lithuania',
    'LU': 'LU_luxembourg',
    'LV': 'LV_latvia',
    'MT': 'MT_malta',
    'NL': 'NL_netherlands',
    'NO': 'NO_norway',
    'PL': 'PL_poland',
    'PT': 'PT_portugal',
    'RO': 'RO_romania',
    'RS': 'RS_serbia',
    'SE': 'SE_sweden',
    'SI': 'SI_slovenia',
    'SK': 'SK_slovakia',
    'UK': 'UK_united_kingdom'
}


# Set the path for output data storage
OUTPUT_PATH = Path(__file__).parents[4] / 'data'

class Runner():
    def __init__(self, energy_balance, country, year, mark='eurostat'):
        self.energy_balance = energy_balance
        self.year = year
        self.country = country
        self.mark = mark
        self.cm = ConversionMap(year, mark=mark)
        self.flh_calculator = FullLoadHoursCalculator()

    def process(self, *methods):
        '''Executes the provided methods and writes the output'''
        for method in methods:
            self._call(method)
        self._write()

    def industry_ict(self):
        '''Process industry ICT sector data'''
        self._run_converter(IndustryICTConverter, **self._inputs())

    def industry_metal(self):
        '''Process industry metal sector data'''
        self._run_converter(IndustryMetalConverter, **self._inputs())

    def industry_chemical(self):
        '''Process industry chemical sector data'''
        self._run_converter(IndustryChemicalConverter, **self._inputs())

    def power_plants(self):
        '''Process power plant data, loading powerplants and calculating full load hours'''
        # self._run_converter(
        #     PowerPlantConverter,
        #     self.country,
        #     plants=load_powerplants(self._inputs()['path']),
        #     flh_calc=self.flh_calculator
        # )

    def chps(self):
        '''Process CHP data from Eurostat'''
        # self._run_converter(
        #     HeatersAndCHPsConverter,
        #     CHPCapacities.from_eurostat(self.country, self.year, eb_type='chps',
        #         use_cols={'lev_efcy': 'Efficiencies', 'plants': 'Plants'}
        #     ),
        #     CHPProducers.from_csv(self._inputs()['path']),
        #     load_heaters(),
        #     self.flh_calculator
        # )

    def split_transformation(self):
        '''Split the transformation output and input for processing'''
        self._run_converter(SplitNegativeConverter, 'Transformation output', 'output', 'input')

    def turn_positive(self):
        '''Ensure all data values are positive'''
        self._run_converter(TurnAllPositive)

    def append_world_chps(self):
        '''Append world CHP data to the energy balance'''
        self._run_converter(AppendCHPs, load_world_chps(self._inputs()['path']))

    def _call(self, method_name):
        '''Calls the provided method dynamically'''
        try:
            getattr(self, method_name)()
        except AttributeError as e:
            raise SystemExit(f'Converter {method_name} is unknown. Or error during call: {e}')

    def _inputs(self):
        '''Returns the inputs needed for the method that was called'''
        return self.cm.inputs(inspect.stack()[1][3], self.country)

    def _run_converter(self, converter, *args, **kwargs):
        '''Runs the provided converter on the energy balance data'''
        converter.convert(self.energy_balance, self.mark, *args, **kwargs)

    def _write(self):
        '''Writes the energy balance and full load hours data to CSV files'''
        output_folder = Runner.fetch_EB_output_folder(self.country, self.year)
        # Write energy balance data and full load hours
        if self.mark == 'world':
            self.energy_balance.to_csv(output_folder / f'output_energy_balance_enriched.encrypted.csv')
        else:
            self.energy_balance.to_csv(output_folder / f'output_energy_balance_enriched.csv')
            self.flh_calculator.to_csv(output_folder / 'output_full_load_hours.csv', f'{self.country}_{self.year}')

    @classmethod
    def load_from_eurostat(cls, country, year=2019, flag=None):
        '''Loads energy balance data from Eurostat, with an option to only retrieve raw data'''
        output_folder = Runner.fetch_EB_output_folder(country, year)
        if flag == 'retrieve-only':
            # Retrieve only raw data from Eurostat
            instance = cls(EnergyBalance.from_eurostat(country, year, save_raw=True, output_folder=output_folder), country, year)
        else:
            # Give an error - data should be retreieved separately to avoid overwriting
            raise SystemExit('Data should be retrieved separately using retrieve-only flag.')

        return instance

    @classmethod
    def load_from_csv(cls, country, year=2019, mark='csv', path=None):
        '''Loads energy balance data from a previously saved CSV file'''
        csv_path = path or Runner.fetch_EB_output_folder(country, year) / f'intermediate_energy_balance_raw.csv'
        return cls(EnergyBalance.from_csv(csv_path), country, year, mark=mark)

    @classmethod
    def load_from_raw_csv(cls, country, year=2019):
        '''Loads raw CSV data for the given country and year'''
        input_folder = Runner.fetch_EB_output_folder(country, year)
        instance = cls(EnergyBalance.load_raw_csv(country, year, input_folder=input_folder), country, year)
        return instance

    @classmethod
    def load_from_world_csv(cls, country, year=2019):
        '''Loads energy balance data from a world balance CSV file'''
        return cls(EnergyBalance.from_world_balance_file(country, year), country, year, mark='world')

    def fetch_EB_output_folder(country, year):
        '''Returns the output folder for the energy balance data'''
        country_folder = COUNTRY_FOLDER_MAPPING.get(country, country)
        output_folder = OUTPUT_PATH / country_folder / str(year) / 'energy_balance'
        output_folder.mkdir(exist_ok=True, parents=True)
        return output_folder

    @classmethod
    def load_from_df(cls, df, country, year):
        '''Initiates Runner from a world DataFrame'''
        return cls(EnergyBalance.load_df(df, country, year), country, year, mark='world')
