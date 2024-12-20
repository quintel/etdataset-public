from .base import Analyser

class SteelDemandAnalyser(Analyser):
    '''
    Source:
        Steel Statistical Yearbook 202
        https://www.worldsteel.org/steel-by-topic/statistics/steel-statistical-yearbook.html
    Debt:
        - Steel production routes specifications will be updated and these hardcoded values should
          be updated accordingly.
        - Specifications are based on NL specifications from MIDDEN, instead of actual production
          routes per country.
    '''

    # Assumptions
    EAF = {
        'input': {
            'electricity': 0.24448898,
            'network_gas':  0.57915832,
            'coal': 0.17635271
        },
        'output': {
            'not_defined': 0.200400802
        }
    }

    BF = {
        'input': {
            'electricity': 0.06101366,
            'network_gas':  0.06552035,
            'coal': 0.87207932
        },
        'output': {
            'not_defined': 0.1525
        }
    }


    def generate_analysis(self, total_steel_production, percentage_of_BF, output_folder=None):
        '''
        Calculate share of final demand metal steel that goes to EAF and to BF for coal,
        electricity and network gas based on MIDDEN typical production values
        '''

        share_of_BF = percentage_of_BF / 100

        if total_steel_production == 0:
            BF_electricity_share_in_final_electricity_demand_steel = 1
            BF_network_gas_share_in_final_network_gas_demand_steel = 1
            BF_coal_share_in_final_coal_demand_steel = 1
            BF_crude_oil_share_in_final_crude_oil_demand_steel = 1
            BF_cokes_share_in_final_cokes_demand_steel = 1
            BF_steam_hot_water_share_in_final_steam_hot_water_demand_steel = 1
            BF_wood_pellets_share_in_final_wood_pellets_demand_steel = 1
        elif percentage_of_BF == 0:
            BF_electricity_share_in_final_electricity_demand_steel = 0
            BF_network_gas_share_in_final_network_gas_demand_steel = 0
            BF_coal_share_in_final_coal_demand_steel = 0
            BF_crude_oil_share_in_final_crude_oil_demand_steel = 0
            BF_cokes_share_in_final_cokes_demand_steel = 0
            BF_steam_hot_water_share_in_final_steam_hot_water_demand_steel = 0
            BF_wood_pellets_share_in_final_wood_pellets_demand_steel = 0
        elif percentage_of_BF == 100:
            BF_electricity_share_in_final_electricity_demand_steel = 1
            BF_network_gas_share_in_final_network_gas_demand_steel = 1
            BF_coal_share_in_final_coal_demand_steel = 1
            BF_crude_oil_share_in_final_crude_oil_demand_steel = 1
            BF_cokes_share_in_final_cokes_demand_steel = 1
            BF_steam_hot_water_share_in_final_steam_hot_water_demand_steel = 1
            BF_wood_pellets_share_in_final_wood_pellets_demand_steel = 1
        else:
            EAF_energy_demand = total_steel_production * (1 - share_of_BF) / self.EAF['output']['not_defined']
            EAF_electricity_demand = EAF_energy_demand * self.EAF['input']['electricity']
            EAF_network_gas_demand = EAF_energy_demand * self.EAF['input']['network_gas']
            EAF_coal_demand = EAF_energy_demand * self.EAF['input']['coal']

            BF_energy_demand = total_steel_production * share_of_BF / self.BF['output']['not_defined']
            BF_electricity_demand = BF_energy_demand * self.BF['input']['electricity']
            BF_network_gas_demand = BF_energy_demand * self.BF['input']['network_gas']
            BF_coal_demand = BF_energy_demand * self.BF['input']['coal']

            BF_electricity_share_in_final_electricity_demand_steel = BF_electricity_demand / (EAF_electricity_demand + BF_electricity_demand)
            BF_network_gas_share_in_final_network_gas_demand_steel = BF_network_gas_demand / (EAF_network_gas_demand + BF_network_gas_demand)
            BF_coal_share_in_final_coal_demand_steel = BF_coal_demand / (EAF_coal_demand + BF_coal_demand)

            BF_crude_oil_share_in_final_crude_oil_demand_steel = 1
            BF_cokes_share_in_final_cokes_demand_steel = 1
            BF_steam_hot_water_share_in_final_steam_hot_water_demand_steel = 1
            BF_wood_pellets_share_in_final_wood_pellets_demand_steel = 1


        data = {
            'input_industry_metal_steel_production': total_steel_production,
            'input_industry_steel_blastfurnace_bof_share': share_of_BF,
            'industry_final_demand_for_metal_steel_electricity_industry_steel_blastfurnace_bof_parent_share': BF_electricity_share_in_final_electricity_demand_steel,
            'industry_final_demand_for_metal_steel_network_gas_industry_steel_blastfurnace_bof_parent_share': BF_network_gas_share_in_final_network_gas_demand_steel,
            'industry_final_demand_for_metal_steel_coal_industry_steel_blastfurnace_bof_parent_share': BF_coal_share_in_final_coal_demand_steel,
            'industry_final_demand_for_metal_steel_crude_oil_industry_steel_blastfurnace_bof_parent_share': BF_crude_oil_share_in_final_crude_oil_demand_steel,
            'industry_final_demand_for_metal_steel_cokes_industry_steel_blastfurnace_bof_parent_share': BF_cokes_share_in_final_cokes_demand_steel,
            'industry_final_demand_for_metal_steel_steam_hot_water_industry_steel_blastfurnace_bof_parent_share': BF_steam_hot_water_share_in_final_steam_hot_water_demand_steel,
            'industry_final_demand_for_metal_steel_wood_pellets_industry_steel_blastfurnace_bof_parent_share': BF_wood_pellets_share_in_final_wood_pellets_demand_steel
        }

        self.write_to_analysis(data, 'steel_demands_analysis')
