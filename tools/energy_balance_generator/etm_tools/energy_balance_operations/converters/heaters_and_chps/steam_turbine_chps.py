from etm_tools.energy_balance_operations.plant import Plant, Producer
from .base import CHPConverter

class SteamTurbineCHPConverter(CHPConverter):

    EXCLUDE = 'Co-firing coal plant for district heat (CHP)'

    def conversion(self, chp_capacities, flh_calc=None, heat_network=None):
        '''
        Parses all Steam Turbine CHP's. They are added to the EB, HeatNetwork and FullLoadHours
        calculation.

        Params:
            chp_capacities(CHPCapacities):      The CHP capacities as retrieved from
                                                Eurostat
            flh_calc(FullLoadHoursCalculator):  All parsed producers will be added to
                                                the full load hours calculation and
                                                output file
            heat_network(HeatNetwork):          The heat network instance the plants
                                                should be added to
        '''
        # Exclude the Co-firing plant from the Steam Turbines that we will parse
        steam_turbines = [
            producer for producer in self.producers.steam_turbine_chps
            if producer.name != self.EXCLUDE
        ]

        # Calculate total capacity and production
        total_e_capacity = chp_capacities.capacity('Steam Turbine CHP')
        total_e_produced = self.produced('electricity', steam_turbines)

        for producer in steam_turbines:
            # Add to EB and Heat network
            heat = self.process_producer(producer, is_chp=True)
            heat_network.add_producer(producer, heat)

            # Calculate the producers capacity based on its share in the e-prodcution
            # and add the plant to the to FLH Logger
            e_produced = self.produced('electricity', producer)
            production_share = e_produced / total_e_produced if total_e_produced else .0
            e_capacity = production_share * total_e_capacity
            flh_calc.add_plant(producer.name, e_produced, e_capacity)


    def produced(self, carrier, producer):
        '''
        Returns the amount produced in TJ by the producers based on their fuels

        Params:
            carrier(str):                       One of 'electricity' or 'heat'
            producer(Producer|list[Producer]):  A single, or Iterable of producers

        Returns:
            float: production in TJ
        '''
        if isinstance(producer, list):
            product_list = self.all_products_for(producer)
        else:
            product_list = self.products_for(producer)

        return self.energy_balance.share_to_tj(
            flows=self.production_flows(carrier),
            products=product_list,
            merge_products=True
        )
