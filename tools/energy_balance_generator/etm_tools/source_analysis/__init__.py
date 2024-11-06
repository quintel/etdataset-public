from .industry_chemical import IndustryChemicalAnalyser
from .fertilizer_demands import FertilizerDemandAnalyser
from .non_ferrous_metals_demands import NonFerrousMetalsDemandAnalyser
from .steel_demands import SteelDemandAnalyser

from etm_tools.utils.conversion_map import ConversionMap


def analyse_country(country, year=2019, output_folder=None, mark=None):

    cm = ConversionMap(year=year, source='source_analyses')

    IndustryChemicalAnalyser.generate_analyses(country, year, year, mark=mark)
    FertilizerDemandAnalyser.generate_analyses(country, year, **cm.inputs('fertilizer_demand', country))
    NonFerrousMetalsDemandAnalyser.generate_analyses(country, year, **cm.inputs('non_ferrous_metals_demand', country))
    SteelDemandAnalyser.generate_analyses(country, year, **cm.inputs('steel_demand', country))
