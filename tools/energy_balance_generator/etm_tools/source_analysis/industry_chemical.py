from .base import Analyser
from etm_tools.energy_balance_operations import EnergyBalance

class IndustryChemicalAnalyser(Analyser):
    '''
    Source:
        Eurostat
    Debt:
        ETM product wood pellets has no information for non-energetic use on the commodity balance
        of renewables and wastes (NRG_CB_RW). Assumed to be 0.
    '''

    ANALYSES = ['oil', 'gas', 'coal']


    def generate_analysis(self, year, output_folder=None, mark=None):
        '''
        Generate chemical source analysis for all types of chemical analyses.
        '''
        if self.mark == 'world':
            return
        else:
            for analysis in self.ANALYSES:
                self._generate(year, analysis_name=analysis)

    def _generate(self, year, analysis_name='crude_oil', output_folder=None):
        '''
        Generate chemical non energetic demand shares based on a commodity balance downloaded from
        Eurostat. You can change the settings for this comodity balance in the config/eurostat.yml.
        '''
        com_bal = EnergyBalance.from_eurostat(self.country, year, eb_type=analysis_name, output_folder=output_folder)

        # Warning: There were previously issues with the hardcoded flow names. En dashes vs hyphens.
        product_shares = com_bal.calculate_share_in_flow(
            'Final consumption - industry sector - chemical and petrochemical - non-energy use',
            'Final consumption - non-energy use')

        self.write_to_analysis(product_shares, f'commodity_balance_{analysis_name}_raw')
