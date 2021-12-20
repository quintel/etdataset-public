from .base import Converter

class IndustryICTConverter(Converter):
    # Products groups
    ELECTRICITY_PRODUCTS = ['Electricity']

    # Energy use flows
    IND = 'Final consumption - industry sector - energy use'
    IND_ICT = 'Final consumption - industry sector - information and communication - energy use'
    OTH = 'Final consumption - other sectors - energy use'
    OTH_SERV = 'Final consumption - other sectors - commercial and public services - energy use'

    def conversion(self, demand_ict_electricity_energetic):
        '''
        Create an ICT Industry flow, based on an input ICT demand and the existing
        commercial and public services flow from the Other sector
        '''

        # ENERGETIC

        # Shift electricity from services sector to new ict sector.
        all_amounts_to_shift = self.energy_balance.all_product_amounts_proportionate(
            self.OTH_SERV,
            {demand_ict_electricity_energetic: self.ELECTRICITY_PRODUCTS}
        )

        self.energy_balance.shift_energy(self.OTH_SERV, self.IND_ICT,
            all_amounts_to_shift, safe_guard='nonnegative'
        )

        # Update other and industry according to shifted electricity.
        all_amounts_to_shift = self.energy_balance.all_product_amounts_proportionate(
            self.OTH,
            {demand_ict_electricity_energetic: self.ELECTRICITY_PRODUCTS}
        )

        self.energy_balance.shift_energy(self.OTH, self.IND,
            all_amounts_to_shift, safe_guard='nonnegative'
        )
