from pathlib import Path
import inspect

from etm_tools.utils.conversion_map import ConversionMap
from .energy_balance import EnergyBalance
from .converters import *
from .input_files import load_powerplants, load_heaters, load_world_chps
from .chp_capacities import CHPCapacities
from .chp_producers import CHPProducers
from .full_load_hours import FullLoadHoursCalculator

OUTPUT_PATH = Path(__file__).parents[2] / 'data' / 'conversions_output'

class Runner():
    def __init__(self, energy_balance, country, year, mark='eurostat'):
        self.energy_balance = energy_balance
        self.year = year
        self.country = country
        self.mark = mark
        self.cm = ConversionMap(year)
        self.flh_calculator = FullLoadHoursCalculator()

    def process(self, *methods):
        '''Call all methods - and then write'''
        for method in methods:
            self._call(method)

        self._write()

    def industry_ict(self):
        self._run_converter(IndustryICTConverter, **self._inputs())

    def industry_metal(self):
        self._run_converter(IndustryMetalConverter, **self._inputs())

    def industry_chemical(self):
        self._run_converter(IndustryChemicalConverter, **self._inputs())

    def power_plants(self):
        self._run_converter(
            PowerPlantConverter,
            self.country,
            plants=load_powerplants(self._inputs()['path']),
            flh_calc=self.flh_calculator
        )

    def chps(self):
        '''NOTE: Runs the full CHP module including downloads, Eurostat only'''
        self._run_converter(
            HeatersAndCHPsConverter,
            CHPCapacities.from_eurostat(self.country, self.year, eb_type='chps',
                use_cols={'lev_efcy': 'Efficiencies', 'plants': 'Plants'}
            ),
            CHPProducers.from_csv(self._inputs()['path']),
            load_heaters(),
            self.flh_calculator
        )

    def split_transformation(self):
        self._run_converter(SplitNegativeConverter, 'Transformation output', 'output', 'input')

    def turn_positive(self):
        self._run_converter(TurnAllPositive)

    def append_world_chps(self):
        self._run_converter(AppendCHPs, load_world_chps(self._inputs()['path']))

    def _call(self, method_name):
        try:
            getattr(self, method_name)()
        except AttributeError:
            raise SystemExit(f'\033[93mConverter {method_name} is unknown.\033[0m')

    def _inputs(self):
        '''Returns the inputs for the method that called this method'''
        return self.cm.inputs(inspect.stack()[1][3], self.country)

    def _run_converter(self, converter, *args, **kwargs):
        converter.convert(self.energy_balance, self.mark, *args, **kwargs)

    def _write(self):
        year_folder = OUTPUT_PATH / str(self.year)
        year_folder.mkdir(exist_ok=True, parents=True)

        self.flh_calculator.to_csv(year_folder / 'full_load_hours.csv', self.country)
        self.energy_balance.to_csv(year_folder / f'{self.country}.csv')

    @classmethod
    def load_from_eurostat(cls, country, year=2019):
        return cls(EnergyBalance.from_eurostat(country, year), country, year)

    @classmethod
    def load_from_csv(cls, country, year=2019, mark='eurostat', path=None):
        return cls(EnergyBalance.from_csv(path), country, year, mark=mark)

    @classmethod
    def load_from_world_csv(cls, country, year=2019):
       return cls(EnergyBalance.from_world_balance_file(country, year), country, year, mark='world')
