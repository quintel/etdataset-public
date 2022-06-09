from .producers_with_flh import ProducersWithFLH
from .base import CHPConverter

class GasCHPsConverter(CHPConverter, ProducersWithFLH):
    ''''''
    # TODO: remove these in favor of getting the full producers from self.producers
    GAS_BASED_CHPS = ['Internal Combustion CHP', 'Gas Turbine CHP', 'Combined Cycle CHP']
    BIO_ICE = 'Biogas CHP'

    def conversion(self, chp_capacities, flh_calc=None, heat_network=None):
        '''
        First the Biogas based Internal Combustion Engine will be split off from
        the other gas based CHP's that run on a mix of Oil and Natural Gas.
        Capacities and output shares for the four CHP types (gen_tech in
        Eurostat language) are added to the result.
        Secondly the input file of typical efficiences is used to determine the
        share in total fuel input for each type of CHP.
        Then ...

        Params:
            chp_capacities(CHPCapacities):  The CHP capacities as retrieved from
                                            Eurostat
        '''
        self.result = CHPLogger()
        # TODO: add flh and hn to self - in .base!! and capacities too? would love that! ;)

        # Treat Coal Gas Plant and Biogas Internal Combustion Engine separately
        self.split(self.producers.coal_gas_chp, heat_network, flh_calc, chp_capacities)

        # If the fixed FLH of 8500 for Biogas leads to calculated capacity that exceeds the ICE CHP
        # no correction is made. The resulting capacity will therefore be higher than the ICE CHP
        # capacity, but this has no effect on the energy flows. The only implication is that
        # some biogas is actually burned in other CHPs, such as the CCGT or GT. The resulting
        # redistribution of capacity for CCGT and GT will therefore be slightly off.
        self.split(self.producers.biogas_chp, heat_network, flh_calc, chp_capacities,
            cap_tech='Internal Combustion CHP')

        # Calculate the output shares based on the Eurostat CHP capacities and save them to result
        self.calculate_output_shares(chp_capacities, carrier='electricity')
        self.calculate_output_shares(chp_capacities, carrier='heat')

        # Calculate input shares based on efficiencies from the CHP input file
        self.calculate_input_shares()

        # Add the other gas based producers to the Energy Balance and Heat Networks
        for producer in self.producers.gas_based_chps:
            heat = self.process_producer(producer, is_chp=True, shares=self.result)
            heat_network.add_producer(producer, heat)

            # Check if CHPs were incalcuable and backup was turned ON, else add to FLH calc normally
            if not producer.has_subplants() and producer.has_subplant_with_backup_on():
                flh_calc.add_plant_with_flh(producer.name, producer.first_subplant().backup_flh)
            else:
                flh_calc.add_plant(
                    producer.name,
                    self.result.get(producer.name, 'electricity', 'produced'),
                    self.result.get(producer.name, 'electricity', 'capacity')
                )



    def calculate_output_shares(self, chp_capacities, carrier='electricity'):
        '''Adds the shares and capacities to the intermediate result'''
        try:
            total_capacity = self.total_capacity_gas_and_oil(chp_capacities, carrier)

            # Calculate and add shares to result
            for tech in self.GAS_BASED_CHPS:
                capacity = chp_capacities.capacity(tech, carrier)

                if tech == 'Internal Combustion CHP':
                    capacity -= self.result.get(self.BIO_ICE, carrier, 'capacity')

                output_share = capacity / total_capacity if total_capacity else .0

                self.result.add(
                    tech, capacity=capacity,
                    output_share=output_share, carrier=carrier
                )
        except CHPCapacityError:
            # TODO: Warning to user that Coal gas is possibly messed up?
            self.set_backup_full_load_hours(chp_capacities, carrier)


    def set_backup_full_load_hours(self, chp_capacities, carrier):
        '''
        Alarm plants to use their backup FLH in further calculations.
        This method is called when CHP FLH are deemed incalculable due to Coal
        gas CHP not behaving. (Possibly the coal gas should have gone somewhere else)
        '''
        for producer in self.producers.gas_based_chps:
            # If there was originally a capacity, switch on backup FLHs
            if chp_capacities.capacity(producer.name, carrier):
                producer.turn_on_backup_flh()


    def total_capacity_gas_and_oil(self, chp_capacities, carrier):
        '''
        Returns the total capacity left in all gas based CHPs after splitting off
        Coal gas and Biogas plants.

        If no capacity is left after subtracting Coal gas or Biogas plants, backup
        full load hours are switched on, as the gas based CHPs are assumed to be
        incalculable. We do this so that any bits of oil and gas that are in the
        Energy Balance for CHPs will be accounted for regardless of any misplaced
        capacity for Coal gas/Biogas.

        Params:
            chp_capacities (CHPCapacities): The capacities of all (gas based) CHPs
            coal_gas(str):                  The coal gas plants name
            carrier(str):                   'heat' | 'electricity'

        Returns float (capcity in MW)
        '''
        total_capacity_gas_and_oil = (
            chp_capacities.sum(self.GAS_BASED_CHPS, carrier) -
            self.result.get(self.BIO_ICE, carrier, 'capacity') -
            self.result.get(self.producers.coal_gas_chp.name, carrier, 'capacity')
        )

        # If there was no capacity in the first place, or when we have a positive capacity left,
        # we go on normally
        if total_capacity_gas_and_oil > 0 or not chp_capacities.sum(self.GAS_BASED_CHPS, carrier):
            return total_capacity_gas_and_oil

        # Otherwise we have a problem
        raise CHPCapacityError()


    def calculate_input_shares(self):
        '''
        Calculate input shares based on the relative input shares, combining
        typical effiencies and output shares

        This is not done for the BIO_ICE or coal gas CHP.
        '''
        producers = self.producers.gas_based_chps
        total = sum((self.relative_input_eff(producer) for producer in producers))

        for producer in producers:
            input_share = self.relative_input_eff(producer) / total if total else .0

            self.result.add(
                producer.name, 'electricity',
                input_share=input_share
            )


    def relative_input_eff(self, producer):
        '''
        Uses the mean of residential and industrial efficiency to calculate
        relative efficiency.
        '''
        return (self.result.get(producer.name, 'electricity', 'output_share') /
            producer.metadata['efficiency'])


# ------------------------------------------------------------------------------

# TODO: Make these properties on Producer instead of as a silly class at the bottom here
class CHPLogger:
    '''Keeps track of our result'''
    def __init__(self):
        self.logger = {}


    def add(self, gen_tech, carrier='electricity', **kwargs):
        if not gen_tech in self.logger:
            self.logger[gen_tech] = {carrier: kwargs}
        elif not carrier in self.logger[gen_tech]:
            self.logger[gen_tech][carrier] = kwargs
        else:
            for key in kwargs:
                self.logger[gen_tech][carrier][key] = kwargs[key]


    def get(self, gen_tech, carrier='electricity', item='output_share'):
        return self.logger.get(gen_tech, {}).get(carrier, {}).get(item, 0.0)


    def show(self):
        return self.logger


class CHPCapacityError(BaseException):
    '''
    Raised when there is something wrong with splitting off capacity from Biogas and
    Coal gas from the rest. The Coal gas should probably have gone somewhere else than
    in a Gas based CHP
    '''
    pass
