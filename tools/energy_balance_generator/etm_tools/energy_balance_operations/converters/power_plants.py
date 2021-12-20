'''Powerplant converter. Try to keep the Converters as clear and verbose as possible :)'''

from .base import Converter

class PowerPlantConverter(Converter):
    PRODUCT_GROUPS = {
        'Coal': ['Anthracite','Coking coal','Other bituminous coal','Sub-bituminous coal',
            'Patent fuel','Coke oven coke','Gas coke','Coal tar','Brown coal briquettes'],
        'Lignite, peat': ['Lignite','Peat and peat products'],
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
    def production_labels(carrier):
        return [
            f'Gross {carrier} production - main activity producer {carrier} only',
            f'Gross {carrier} production - autoproducer {carrier} only'
        ]

    @staticmethod
    def transformation_labels(carrier):
        return [
            f'Transformation input - electricity and heat generation - main activity producer {carrier} only - energy use',
            f'Transformation input - electricity and heat generation - autoproducer {carrier} only - energy use'
        ]


    def conversion(self, country, plants=None, flh_calc=None):
        '''
        Parses all plants, and adds them as rows to the EB
        '''
        if plants is None:
            # TODO: add warning, or remove kwarg!
            return

        # We go over each plant
        for plant_name, plant_details in plants.iterrows():
            # Calculate energy of input products based on the given share of the
            # plant in the whole
            energy_per_product = self.energy_balance.share_to_tj(
                flows=self.labels_for(plant_details['output', 'output'], flow_type='transformation'),
                share=plant_details['input_share', country],
                products=self.products_for(plant_details['input', 'input']),
            )

            # Calculate energy of the output product based on the given share of
            # the plant in the whole
            energy_output = self.energy_balance.share_to_tj(
                flows=self.labels_for(plant_details['output', 'output'], flow_type='production'),
                share=plant_details['output_share', country],
                products=self.products_for(plant_details['input', 'input']),
                merge_products=True # We want to sum over all the products
            )

            # Add the output energy to our dictionary under the correct product
            energy_per_product[plant_details['output', 'output']] = energy_output

            # Add the plant to the energy balance with the calculated amout of
            # energy per product (do not fill in the Total column)
            self.energy_balance.add_row_with_energy(plant_name, energy_per_product, total=False)

            if flh_calc:
                flh_calc.add_plant(plant_name, energy_output, plant_details['net_max_generating_capacity_MW', country])


    def labels_for(self, plant_output, flow_type='production'):
        '''
        Returns the labels that should be used for this output product and flow type.
        flow_type can be either 'production' or 'transformation'.
        '''
        if flow_type == 'production':
            return self.production_labels(plant_output.lower())
        if flow_type == 'transformation':
            return self.transformation_labels(plant_output.lower())


    def products_for(self, plant_input):
        '''
        Returns the product or products that go into this plant.
        Check if the plant_input defines a group of products, or is already a singular product
        '''
        if plant_input in self.PRODUCT_GROUPS:
            return self.PRODUCT_GROUPS[plant_input]

        return [plant_input]
