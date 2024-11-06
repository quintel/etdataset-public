from .base import Analyser

class NonFerrousMetalsDemandAnalyser(Analyser):
    '''
    Source:
        Mineral Yearbook – XLSX Format – 2020 tables-only release – T13:
        https://www.usgs.gov/centers/nmic/aluminum-statistics-and-information
    Debts:
        Assumption 100% current technology due to lack of better sources
    '''

    # Assumptions
    OUTPUT = {
        'not_defined': 0.0162972620599739,   # Mton per PJ
        'useable_heat': 0.9
    }

    INPUT = {
        'electricity': 0.940352020860495,
        'useable_heat': 0.0596479791395046
    }


    def generate_analysis(self, total_aluminium_production, output_folder=None):
        '''
        Calculate final aluminum demand for electricity and network gas by using the total aluminum
        production, specifications of nl2019 industry_aluminium_electrolysis_current_electricity
        and industry_aluminium_burner_network_gas.
        '''
        data = {
            'aluminium production': total_aluminium_production,
            'demand_aluminium_electricity_energetic': (
                total_aluminium_production / self.OUTPUT['not_defined'] *
                self.INPUT['electricity'] * 1000   # Convert to TJ
            ),
            'demand_aluminium_network_gas_energetic': (
                total_aluminium_production / self.OUTPUT['not_defined'] *
                self.INPUT['useable_heat'] / self.OUTPUT['useable_heat'] * 1000   # Convert to TJ
            )
        }

        self.write_to_analysis(data, 'non_ferrous_metal_demands_analysis')
