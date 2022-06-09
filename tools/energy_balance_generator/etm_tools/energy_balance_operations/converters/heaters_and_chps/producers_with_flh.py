class ProducersWithFLH():
    '''Included in gas based CHPs, used for splitting off BIO ICE and Coal Gas CHPs'''

    def split(self, producer, heat_network, flh_calc, chp_capacities, cap_tech='all'):
        '''
        Parse the plant apart from the rest. Assume these have FLH set in their metadata.
        '''
        self.parse_heat(producer, heat_network, flh_calc,
            cap_at=self.max_capacity(chp_capacities, 'heat', cap_tech))
        self.parse_electricity(producer, flh_calc,
            cap_at=self.max_capacity(chp_capacities, 'electricity', cap_tech))

        flh_calc.add_plant_with_flh(producer.name, producer.metadata['flh'])


    def parse_heat(self, producer, heat_network, flh_calc, cap_at=None):
        '''
        Parse the heat part of a CHP that will be split off
        '''
        heat = self.process_producer(producer, is_chp=True)
        heat_network.add_producer(producer, heat)
        self.result.add(producer.name, carrier='heat',
            capacity=self.capacity(heat, producer, flh_calc, cap_at=cap_at)
        )


    def parse_electricity(self, producer, flh_calc, cap_at=None):
        '''
        Parse the electricity part of a CHP that is split off
        '''
        e_produced = self.energy_balance.share_to_tj(
            flows=self.production_flows('electricity'),
            products=self.products_for(producer),
            merge_products=True
        )

        self.result.add(producer.name, carrier='electricity',
            capacity=self.capacity(e_produced, producer, flh_calc, cap_at=cap_at)
        )


    def capacity(self, produced, producer, flh_calc, cap_at=None):
        '''Calculate capacity based on FLH and TJ produced'''
        capacity = (produced * flh_calc.TJ_TO_MWH) / producer.metadata['flh']
        if cap_at is not None and capacity > cap_at:
            ProducersWithFLH.warn_lowering_capacity(producer.name, capacity, cap_at)
            return cap_at

        return capacity


    def max_capacity(self, chp_capacities, carrier, tech='all'):
        '''Returns the max capacity available that can be assigned to the producer'''
        if tech != 'all':
            return chp_capacities.capacity(tech, carrier)

        return chp_capacities.sum(self.GAS_BASED_CHPS, carrier)


    @staticmethod
    def warn_lowering_capacity(plant_name, calculated, cap):
        print(f'\033[93mCapacity Warning: {plant_name}: Based on given full',
            f'load hours, plant capacity should be {calculated}, but only {cap}',
            'MW is available. Limiting capacity, but not correcting FLH.\033[0m')
