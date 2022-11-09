# We could setup a Heat network in here??
from etm_tools.energy_balance_operations.heat_network import HeatNetworks

from .base import HeatConverter

from .gas_chps import GasCHPsConverter
from .steam_turbine_chps import SteamTurbineCHPConverter
from .heaters import HeatersConverter

class HeatersAndCHPsConverter(HeatConverter):
    '''
    Note about not taking 'Other' CHPs into account.
    '''
    MARK = 'eurostat'

    # Heat networks consumption
    INDUSTRY_CONSUMPTION = ['Final consumption - industry sector - energy use',
        'Energy sector - coal mines - energy use',
        'Energy sector - oil and natural gas extraction plants - energy use',
        'Energy sector - patent fuel plants - energy use',
        'Energy sector - brown coal briquettes and peat briquettes plants - energy use',
        'Energy sector - gas works - energy use',
        'Energy sector - petroleum refineries (oil refineries) - energy use',
        'Energy sector - nuclear industry - energy use',
        'Energy sector - coal liquefaction plants - energy use',
        'Energy sector - liquefaction and regasification plants (LNG) - energy use',
        'Energy sector - gasification plants for biogas - energy use',
        'Energy sector - gas-to-liquids plants - energy use',
        'Energy sector - charcoal production plants - energy use',
        'Energy sector - not elsewhere specified - energy use'
    ]
    RESIDENTIAL_CONSUMPTION = ['Final consumption - other sectors - energy use',
        'Distribution losses']

    GAS_BACKUP = 'Gas Turbine CHP'


    def conversion(self, chp_capacities, chp_producers, heaters, flh_calc):
        '''
        Parses all producers of types chp and heaters. The input products are calculated from
        the `Transformation` flows, and the output products (Heat for heaters and Heat and
        Electricity for CHPs) are calculated by adding the the energy from the used products for
        the producer from the correct `Gross production` flows.
        Then all producers are assigned a heat network (either industrial or residential). Flexible
        producers will be split up in a residential and industrial version based on the heat deficit
        remaining in the `Final consumption` flows once all the 'inflexible' producers have been
        assigned.
        All producers will be added as rows to the energy balance.

        Params:
            heaters (List[Producer]):           The list of producers as listed in the
                                                heaters_and_chps config file.
            chp_capacities (CHPCapacities):     The CHPCapacities from eurostat
            chp_producers (CHPProducers):       The CHPProducers from the CHP input file
            flh_calc (FullLoadHoursCalculator):  Logs all full load hours of the CHPs
        '''

        heat_networks = HeatNetworks(
            self.heat_consumption_for(self.INDUSTRY_CONSUMPTION),
            self.heat_consumption_for(self.RESIDENTIAL_CONSUMPTION)
        )

        # Convert all the types of heaters and CHP's
        GasCHPsConverter.convert(self.energy_balance, chp_producers, chp_capacities,
            heat_network=heat_networks, flh_calc=flh_calc)
        SteamTurbineCHPConverter.convert(self.energy_balance, chp_producers, chp_capacities,
            heat_network=heat_networks, flh_calc=flh_calc)
        HeatersConverter.convert(self.energy_balance, heaters, heat_networks=heat_networks)

        self.solve_heat_networks(heat_networks, flh_calc)

        # TODO: combine the oil shale plant with the CHP ICE and recalculate FLH


    def solve_heat_networks(self, heat_networks, flh_calc):
        '''
        Gets the result from the HeatNetwork of how flexible producers should be split up into
        Residential and Industrial plants. Assigns these producers the correct amount of heat and
        other products.

        The resulting producers are added to the Energy Balance
        '''
        # Assign flexible producers
        for producer, sector, new_share in heat_networks.assign_flexible_producers():
            self.energy_balance.add_row_from_share(producer.name, producer.name_for(sector), new_share)
            # Check for backup FLH set to ON by incalculable Gas based CHPs
            if producer.subplant(sector) and producer.subplant(sector).use_backup:
                flh_calc.add_plant_with_flh(producer.name_for(sector), producer.subplant(sector).backup_flh)
            else:
                flh_calc.add_copy(producer.name_for(sector), producer.name)

        # Remove unassigned versions of producers and swap energy between Industrial plants that
        # sometimes blend in Oil with NG, and Residential plants that only use NG, that are based
        # on the same producer
        for producer in heat_networks.unassigned_producers:
            self.energy_balance.remove(producer.name)
            flh_calc.remove(producer.name)

            if producer.has_subplants_with_different_fuels():
                # NOTE: don't hardcode this Nora!
                backup = self.GAS_BACKUP if producer.subplants_shared_fuel() == 'Gas' else ''

                # NOTE: we assume the plant that used extra fuels is the Industrial variant
                self.energy_balance.swap_energy(
                    producer.residential_plant.name,
                    producer.industrial_plant.name,
                    self.PRODUCT_GROUPS[producer.subplants_fuel_diff()],
                    self.PRODUCT_GROUPS[producer.subplants_shared_fuel()],
                    backup_flow=backup
                )


    def heat_consumption_for(self, flows):
        return self.energy_balance.eb['Heat'][flows].sum()
