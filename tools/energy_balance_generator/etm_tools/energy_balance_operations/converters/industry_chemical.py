from .base import Converter

class IndustryChemicalConverter(Converter):
    # Product groups
    COAL_PRODUCTS = ['Anthracite','Coking coal','Other bituminous coal','Sub-bituminous coal',
        'Peat and peat products','Lignite','Patent fuel','Gas coke','Coal tar',
        'Brown coal briquettes']
    NETWORK_GAS_PRODUCTS = ['Natural gas', 'Biogases']
    CRUDE_OIL_PRODUCTS = ['Oil shale and oil sands', 'Crude oil', 'Natural gas liquids', 'Refinery feedstocks',
        'Additives and oxygenates (excluding biofuel portion)', 'Other hydrocarbons',
        'Refinery gas', 'Ethane', 'Liquefied petroleum gases',
        'Motor gasoline (excluding biofuel portion)', 'Aviation gasoline', 'Gasoline-type jet fuel',
        'Kerosene-type jet fuel (excluding biofuel portion)', 'Other kerosene',
        'Gas oil and diesel oil (excluding biofuel portion)', 'Fuel oil', 'Naphtha',
        'White spirit and special boiling point industrial spirits', 'Lubricants', 'Bitumen',
        'Paraffin waxes', 'Petroleum coke', 'Other oil products']
    WOOD_PELLETS_PRODUCTS = ['Primary solid biofuels']
    HEAT_PRODUCTS = ['Heat']
    ELECTRICITY_PRODUCTS = ['Electricity']

    # Energy use flows
    CHEM_AND_PETROCHEM_E = 'Final consumption - industry sector - chemical and petrochemical - energy use'
    CHEM_FERTILIZERS_E = 'Final consumption - industry sector - chemical fertilizers - energy use'
    CHEM_OTHER_E = 'Final consumption - industry sector - chemical other - energy use'

    # Non energy use flows
    FINAL_NE = 'Final consumption - non-energy use'
    CHEM_AND_PETROCHEM_NE = 'Final consumption - industry sector - chemical and petrochemical - non-energy use'
    CHEM_FERTILIZERS_NE = 'Final consumption - industry sector - chemical fertilizers - non-energy use'
    CHEM_OTHER_NE = 'Final consumption - industry sector - chemical other - non-energy use'
    IND_NE = 'Final consumption - industry sector - non-energy use'
    OTHER_NE = 'Final consumption - industry sector - other - non-energy use'


    def conversion(self,
        demand_fertilizers_coal_energetic,
        demand_fertilizers_network_gas_energetic,
        demand_fertilizers_crude_oil_energetic,
        demand_fertilizers_wood_pellets_energetic,
        demand_fertilizers_heat_energetic,
        demand_fertilizers_electricity_energetic,
        demand_fertilizers_coal_non_energetic,
        demand_fertilizers_network_gas_non_energetic,
        demand_fertilizers_crude_oil_non_energetic,
        # shares_chemical_wood_pellets_non_energetic,
        shares_chemical_network_gas_non_energetic=None,
        shares_chemical_crude_oil_non_energetic=None,
        shares_chemical_coal_non_energetic=None
        ):
        '''
        Splits chemical and petrochemical industry into 'other' and 'fertilizers', based
        on the total demand of fertilizers

        Params:
            demand_fertilizers_coal_energetic (float): The total amount of TJ that should
                                                    end up in the fertilizers sector for coal
            ...
            shares_chemical_crude_oil_non_energetic (Dict[str,float]): Product shares to create a
                                                                       non-energy Chemical and
                                                                       Petroleum sector
        '''

        # ENERGETIC ------------------------------------------------------------

        demand_fertilizers_energetic = {
            # Coal fertilizer demand should be spread out over coal product group, etc
            demand_fertilizers_coal_energetic: self.COAL_PRODUCTS,
            demand_fertilizers_network_gas_energetic: self.NETWORK_GAS_PRODUCTS,
            demand_fertilizers_crude_oil_energetic: self.CRUDE_OIL_PRODUCTS,
            demand_fertilizers_wood_pellets_energetic: self.WOOD_PELLETS_PRODUCTS,
            demand_fertilizers_heat_energetic: self.HEAT_PRODUCTS,
            demand_fertilizers_electricity_energetic: self.ELECTRICITY_PRODUCTS
        }

        self.split_up_flow(self.CHEM_AND_PETROCHEM_E, self.CHEM_FERTILIZERS_E,
            self.CHEM_OTHER_E, demand_fertilizers_energetic)

        # NON ENERGETIC --------------------------------------------------------

        # First create a chemical industry subgroup of the final non energy use
        if not self.energy_balance.has_values(self.CHEM_AND_PETROCHEM_NE):
            self.create_chemical_and_petroleum_non_energy_row(shares_chemical_network_gas_non_energetic,
                shares_chemical_crude_oil_non_energetic, shares_chemical_coal_non_energetic)

        # Second subtract chemical industry non-energetic from industry non-energetic to obtain other industry non-energetic

        self.energy_balance.add_row_from_diff(self.IND_NE,self.CHEM_AND_PETROCHEM_NE,self.OTHER_NE)

        # Third divide the chemical industry into fertilizers and other
        demand_fertilizers_non_energetic = {
            # Coal fertilizer demand should be spread out over coal product group, etc
            demand_fertilizers_coal_non_energetic: self.COAL_PRODUCTS,
            demand_fertilizers_network_gas_non_energetic: self.NETWORK_GAS_PRODUCTS,
            demand_fertilizers_crude_oil_non_energetic: self.CRUDE_OIL_PRODUCTS,
        }

        self.split_up_flow(self.CHEM_AND_PETROCHEM_NE, self.CHEM_FERTILIZERS_NE,
            self.CHEM_OTHER_NE, demand_fertilizers_non_energetic)


    def split_up_flow(self, chem_and_petro, fertilizers, chem_other, demand_per_product_group):
        '''
        Splits up a flow into two other flows based on the demand per product group

        Params:
            chem_and_petro (str): Energy or non energy use chemical and petroleum sector

        '''

        # Calculate the amount of TJ to be shifted for all individual products based on
        # the given fertilizer demands (in short: spread the demand out over the
        # products in the group)
        amounts_to_shift = self.energy_balance.all_product_amounts_proportionate(
            chem_and_petro,
            demand_per_product_group
        )

        # Shift these amounts to the fertilizers
        self.energy_balance.shift_energy(chem_and_petro, fertilizers,
            amounts_to_shift, safe_guard='nonnegative'
        )

        # The remaning energy is classified as chemical other
        self.energy_balance.rename(chem_and_petro, chem_other)


    def create_chemical_and_petroleum_non_energy_row(self,
        shares_chemical_network_gas_non_energetic, shares_chemical_crude_oil_non_energetic,
        shares_chemical_coal_non_energetic):
        '''Based on the shares per product, creates or skips creating a row for non-energy use chem and petrol'''

        merged_product_shares = (shares_chemical_network_gas_non_energetic |
                                shares_chemical_crude_oil_non_energetic |
                                shares_chemical_coal_non_energetic)

        self.energy_balance.add_row_with_energy(
            self.CHEM_AND_PETROCHEM_NE,
            self.energy_balance.product_shares_to_tj(self.FINAL_NE, merged_product_shares)
        )
