from etm_tools.energy_balance_operations.heat_network import HeatNetworks
from .base import Converter

class HeatersAndCHPsConverter(Converter):
    PRODUCT_GROUPS = {
        'Coal': ['Anthracite','Coking coal','Other bituminous coal','Sub-bituminous coal',
            'Patent fuel','Coke oven coke','Gas coke','Coal tar','Brown coal briquettes'],
        'Lignite, peat': ['Lignite','Peat and peat products'],
        'Coal gas': ['Coke oven gas','Blast furnace gas','Other recovered gases'],
        'Oil': ['Oil shale and oil sands','Crude oil',
            'Natural gas liquids','Refinery feedstocks',
            'Additives and oxygenates (excluding biofuel portion)','Other hydrocarbons',
            'Refinery gas','Ethane','Liquefied petroleum gases',
            'Motor gasoline (excluding biofuel portion)','Aviation gasoline',
            'Gasoline-type jet fuel','Kerosene-type jet fuel (excluding biofuel portion)',
            'Other kerosene','Naphtha','Gas oil and diesel oil (excluding biofuel portion)',
            'Fuel oil','White spirit and special boiling point industrial spirits','Lubricants',
            'Bitumen','Petroleum coke','Paraffin waxes','Other oil products','Pure biogasoline',
            'Blended biogasoline','Pure biodiesels','Blended biodiesels','Pure bio jet kerosene',
            'Blended bio jet kerosene','Other liquid biofuels'],
        'Network gas': ['Natural gas','Biogases'],
        'Waste': ['Renewable municipal waste',
            'Industrial waste (non-renewable)','Non-renewable municipal waste'],
        'Hydro': ['Hydro', "Tide, wave, ocean"]
    }

    # Flow labels
    @staticmethod
    def production_labels(carrier, chp_carrier=None):
        chp_carrier = carrier.split(' ')[0] if not chp_carrier else chp_carrier
        return [
            f'Gross {chp_carrier} production - main activity producer {carrier}',
            f'Gross {chp_carrier} production - autoproducer {carrier}'
        ]

    @staticmethod
    def transformation_labels(carrier):
        return [
            f'Transformation input - electricity and heat generation - main activity producer {carrier} - energy use',
            f'Transformation input - electricity and heat generation - autoproducer {carrier} - energy use'
        ]

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
    RESIDENTIAL_CONSUMPTION = ['Final consumption - other sectors - energy use', 'Distribution losses']


    def conversion(self, chps_and_heaters):
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
            chps_and_heaters (List[Dict[str,str]]): The list of producers as listed in the
                                                    heaters_and_chps config file.
        '''
        heat_networks = HeatNetworks(self.heat_consumption_for(self.INDUSTRY_CONSUMPTION),
            self.heat_consumption_for(self.RESIDENTIAL_CONSUMPTION))

        # Parse all producers
        for producer in chps_and_heaters:
            heat_output = self.process_producer(producer)
            heat_networks.add_producer(producer, heat_output)

        # Assign flexible producers
        for name, sector, new_share in heat_networks.assign_flexible_producers():
            self.energy_balance.add_row_from_share(name, f'{name} - {sector}', new_share)

        # Remove unassigned versions of producers
        for producer in chps_and_heaters:
            if producer['network'] == 'flexible': self.energy_balance.remove(producer['name'])


    def process_producer(self, producer):
        '''
        Processes a single producer and adds it to the energy balance.

        The energy per input product is copied from the amount of energy present in these
        products in the `Transformation` flow.
        The energy for the output product(s) is calculated by summing the energy of all
        input products in the `Gross production` flows.

        Params:
            producer (Dict[str,str]): The producer that should be processed

        Returns:
            float: generated Heat by this producer
        '''
        p_type = 'heat only' if producer['type'] == 'heater' else 'combined heat and power'

        # Calculate energy of input products
        energy_per_product = self.energy_balance.share_to_tj(
            flows=HeatersAndCHPsConverter.transformation_labels(p_type),
            products=self.products_for(producer['input']),
        )

        # Calculate energy of output product(s)
        self.add_output_product(energy_per_product, p_type, 'Heat', producer['input'])
        if producer['type'] == 'chp':
            self.add_output_product(energy_per_product, p_type, 'Electricity', producer['input'])

        self.energy_balance.add_row_with_energy(producer_name(producer), energy_per_product,
            total=False)

        return energy_per_product['Heat']


    def add_output_product(self, energy_per_product, p_type, output_product, input_product):
        '''
        Adds the total produced energy to the 'energy_per_product' dict at the output product
        '''
        energy_per_product[output_product] = self.energy_balance.share_to_tj(
            flows=HeatersAndCHPsConverter.production_labels(p_type, output_product.lower()),
            products=self.products_for(input_product),
            merge_products=True
        )


    def products_for(self, plant_input):
        '''
        Returns the product or products that go into this plant.
        Check if the plant_input defines a group of products, or is already a singular product
        '''
        if plant_input in self.PRODUCT_GROUPS:
            return self.PRODUCT_GROUPS[plant_input]

        return [plant_input]


    def heat_consumption_for(self, flows):
        return self.energy_balance.eb['Heat'][flows].sum()


def producer_name(producer):
    if producer['network'] == 'flexible':
        return producer['name']

    return f'{producer["name"]} - {producer["network"]}'
