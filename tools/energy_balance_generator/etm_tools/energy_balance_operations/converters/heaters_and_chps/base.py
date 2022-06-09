from etm_tools.energy_balance_operations.converters.base import Converter

class HeatConverter(Converter):
    PRODUCT_GROUPS = {
        'Coal': ['Anthracite','Coking coal','Other bituminous coal','Sub-bituminous coal',
            'Patent fuel','Coke oven coke','Gas coke','Coal tar','Brown coal briquettes'],
        'Lignite, peat': ['Lignite','Peat and peat products'],
        'Coal gas': ['Coke oven gas','Blast furnace gas','Other recovered gases'],
        'Oil shale': ['Oil shale and oil sands'],
        'Oil': ['Crude oil',
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
        'Gas': ['Natural gas'],
        'Biogas': ['Biogases'],
        'Waste': ['Renewable municipal waste',
            'Industrial waste (non-renewable)','Non-renewable municipal waste'],
        'Hydro': ['Hydro', "Tide, wave, ocean"],
        'Wood pellets': ['Primary solid biofuels'],
        'Solar thermal': ['Solar thermal'],
        'Geothermal': ['Geothermal']
    }

    @staticmethod
    def production_flows(carrier, is_chp=True):
        '''Returns a list of the two Gross Production flows'''
        p_type = 'combined heat and power' if is_chp else 'heat only'

        return [
            f'Gross {carrier} production - main activity producer {p_type}',
            f'Gross {carrier} production - autoproducer {p_type}'
        ]

    @staticmethod
    def transformation_input_flows(is_chp=True):
        '''Returns a list of the two Transformation flows'''
        p_type = 'combined heat and power' if is_chp else 'heat only'
        return [
            f'Transformation input - electricity and heat generation - main activity producer {p_type} - energy use',
            f'Transformation input - electricity and heat generation - autoproducer {p_type} - energy use'
        ]


    # TODO: use .kind instead of keyword is_chp
    def process_producer(self, producer, is_chp=False, shares=None):
        '''
        Processes a single producer and adds it to the energy balance.

        The energy per input product is copied from the amount of energy present in these
        products in the `Transformation` flow.
        The energy for the output product(s) is calculated by summing the energy of all
        input products in the `Gross production` flows.

        Params:
            producer (Producer): The producer that should be processed
            is_chp (Bool):       If True, electricty output will also be added
            shares (CHPLogger):  Holds the input and output shares if multiple
                                 producers use the same fuels
        Returns:
            float: generated Heat by this producer
        '''
        # Calculate energy of input products
        energy_per_product = self.energy_balance.share_to_tj(
            flows=self.transformation_input_flows(is_chp=is_chp),
            products=self.products_for(producer),
            share=shares.get(producer.name, 'electricity', 'input_share') if shares else 1
        )

        # Calculate energy of output product Heat
        energy_per_product['Heat'] = self.energy_balance.share_to_tj(
            flows=self.production_flows('heat', is_chp=is_chp),
            products=self.products_for(producer),
            share=shares.get(producer.name, 'heat', 'output_share') if shares else 1,
            merge_products=True
        )

        # Calculate energy of output product Electricity
        if is_chp:
            energy_per_product['Electricity'] = self.energy_balance.share_to_tj(
                flows=self.production_flows('electricity', is_chp=is_chp),
                products=self.products_for(producer),
                share=shares.get(producer.name, 'electricity', 'output_share') if shares else 1,
                merge_products=True
            )

        self.energy_balance.add_row_with_energy(producer.name, energy_per_product,
            total=False)

        if shares and is_chp:
            shares.add(producer.name, 'electricity', produced=energy_per_product['Electricity'])
            shares.add(producer.name, 'heat', produced=energy_per_product['Heat'])

        return energy_per_product['Heat']


    def products_for(self, producer):
        '''
        Returns a list of all products that make up the producers fuel

        Params:
            producer(Producer): The producer whose fuels should be returned
        '''
        return [fuel for fuel_type in producer.fuel for fuel in self.PRODUCT_GROUPS[fuel_type]]


    def all_products_for(self, producers):
        '''
        Returns a list of all products that make up the producers fuel

        Params:
            producers(list[Producer]): List of producers whose fuels should be included
        '''
        return [p for producer in producers for p in self.products_for(producer)]

    # TODO: one method to update heat network and eb


class CHPConverter(HeatConverter):
    def __init__(self, energy_balance, producers):
        super().__init__(energy_balance)
        self.producers = producers


    @classmethod
    def convert(cls, eb, prod, *args, **kwargs):
        return cls(eb, prod).conversion(*args, **kwargs)
