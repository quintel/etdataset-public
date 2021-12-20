from .base import Converter

class IndustryMetalConverter(Converter):
    # Product groups
    COAL_GAS_PRODUCTS = ['Coke oven gas','Blast furnace gas','Other recovered gases']
    NETWORK_GAS_PRODUCTS = ['Natural gas', 'Biogases']
    ELECTRICITY_PRODUCTS = ['Electricity']

    # Energy use flows
    IND_NON_FER_MET = 'Final consumption - industry sector - non-ferrous metals - energy use'
    IND_MET_ALU = 'Final consumption - industry sector - metal aluminium - energy use'
    IND_MET_OTH = 'Final consumption - industry sector - metal other - energy use'

    # Transformation flows
    TO_CO = 'Transformation output - coke ovens'
    TO_BF = 'Transformation output - blast furnaces'

    def conversion(self,
        demand_aluminium_electricity_energetic,
        demand_aluminium_network_gas_energetic):
        '''
        Splits industry non-ferrous metals demand into 'aluminium' and 'other', based
        on the total demand of aluminium

        Params:
            demand_aluminium_electricity_energetic (float): The total amount of TJ that should
                                                    end up in the aluminium sector for electricity
        '''

        # ENERGETIC
        demand_per_product_group = {
            demand_aluminium_electricity_energetic: self.ELECTRICITY_PRODUCTS,
            demand_aluminium_network_gas_energetic: self.NETWORK_GAS_PRODUCTS
        }

        # Calculate the amount of TJ to be shifted for all individual products based on
        # the given aluminium demands (in short: spread the demand out over the
        # products in the group)
        all_amounts_to_shift = self.energy_balance.all_product_amounts_proportionate(
            self.IND_NON_FER_MET,
            demand_per_product_group
        )

        # Shift these amounts to the aluminium sector
        self.energy_balance.shift_energy(self.IND_NON_FER_MET, self.IND_MET_ALU,
            all_amounts_to_shift, safe_guard='nonnegative'
        )

        # The remaning energy is classified as metal other
        self.energy_balance.rename(self.IND_NON_FER_MET, self.IND_MET_OTH)


        # TRANSFORMATION
        '''

        Checks if there is no transformation output of coal gas in the cokesoven.
        If this is the case and there is coal gas transformation output in the blast furnace,
        then 1 TJ of energy will be moved - otherwise the energy graph will not run.

        '''

        total_output_blastfurnace_coal_gas = self.energy_balance.calculate_sum(self.TO_BF,self.COAL_GAS_PRODUCTS)
        total_output_cokesoven_coal_gas = self.energy_balance.calculate_sum(self.TO_CO,self.COAL_GAS_PRODUCTS)
        
        if total_output_blastfurnace_coal_gas != 0.0:
            if total_output_cokesoven_coal_gas == 0.0:

                all_amounts_to_shift = self.energy_balance.all_product_amounts_proportionate(
                    self.TO_BF,
                    {1: self.COAL_GAS_PRODUCTS}
                )

                self.energy_balance.shift_energy(self.TO_BF, self.TO_CO,
                    all_amounts_to_shift, safe_guard='nonnegative'
                )
                
