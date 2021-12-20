from .industry_chemical import IndustryChemicalAnalyser
from .fertilizer_demands import FertilizerDemandAnalyser
from .non_ferrous_metals_demands import NonFerrousMetalsDemandAnalyser
from .steel_demands import SteelDemandAnalyser

from etm_tools.utils.conversion_map import ConversionMap


def analyse_country(country, year=2019):
    IndustryChemicalAnalyser.generate_analyses(country, year)

    cm = ConversionMap(source='source_analyses')

    FertilizerDemandAnalyser.generate_analyses(country, **cm.inputs('fertilizer_demand', country))
    NonFerrousMetalsDemandAnalyser.generate_analyses(country, **cm.inputs('non_ferrous_metals_demand', country))
    SteelDemandAnalyser.generate_analyses(country, **cm.inputs('steel_demand', country))
