from .base import Analyser

class FertilizerDemandAnalyser(Analyser):
    '''
    Source:
        Clean Hydrogen Monitor 2020
        https://www.hydrogeneurope.eu/wp-content/uploads/2021/04/Clean-Hydrogen-Monitor-2020.pdf
    Debts:
        - Assumptions are made to estimate inputs, instead of using actual product flows.
        - Specifications for nl2019 used for all countries.
        - No product inputs to produce useable heat in the burner, other than network gas.
        - No electricity usage for carbon capture, all final electricity demand is useful
          electricity demand.

    '''

    # Assumptions
    OUTPUT = {
        'hydrogen': 0.77,
        'useable_heat': 0.9
    }

    INPUT = {
        'network_gas': 7.12057053710720E-01,
        'useable_heat': 2.87942946289280E-01
    }

    INPUT_OF_ELECTRICITY = 3.0E09
    OUTPUT_OF_HYDROGEN = 69.0998E09


    def generate_analysis(self, hydrogen_non_energetic_demand, output_folder=None):
        '''
        Generates an input file for fertilizer demand.

        Convert hydrogen demand to energy products input by using the specifications of nl2019
        industry_chemicals_fertilizers_steam_methane_reformer_hydrogen and
        industry_chemicals_fertilizers_burner_network_gas.

        Params:
            hydrogen_non_energetic_demand (float): Fertilizer demand in TJ for hydrogen non energy
                                                   use
        '''
        network_gas_ne = hydrogen_non_energetic_demand / self.OUTPUT['hydrogen'] * self.INPUT['network_gas']
        useable_heat_e = hydrogen_non_energetic_demand / self.OUTPUT['hydrogen'] * self.INPUT['useable_heat']
        network_gas_e = useable_heat_e / self.OUTPUT['useable_heat']
        electricity_e = hydrogen_non_energetic_demand * (self.INPUT_OF_ELECTRICITY / self.OUTPUT_OF_HYDROGEN)

        data = {
            'demand_fertilizers_coal_energetic': 0.0,
            'demand_fertilizers_network_gas_energetic': network_gas_e ,
            'demand_fertilizers_crude_oil_energetic': 0.0,
            'demand_fertilizers_wood_pellets_energetic': 0.0,
            'demand_fertilizers_heat_energetic': 0.0,
            'demand_fertilizers_electricity_energetic': electricity_e,
            'demand_fertilizers_coal_non_energetic': 0.0,
            'demand_fertilizers_network_gas_non_energetic': network_gas_ne,
            'demand_fertilizers_crude_oil_non_energetic': 0.0,
        }

        self.write_to_analysis(data, 'fertilizer_demand_analysis')
