'''Refactored code from Dorine (etdataset/curves/demand/households/space_heating/script)'''
from .config import insulation_config

class House:
    """Class to describe a house"""

    def __init__(self, house_type, insulation_level, thermostat):
        self.house_type = house_type
        self.insulation_level = insulation_level

        self.set_heat_capacity()
        self.set_energy_exchange()

        self.window_area = insulation_config.get_window_area(house_type)
        self.thermostat_temperature = thermostat[insulation_level]
        self.inside_temperature = self.thermostat_temperature[0]


    def calculate_heat_demand(self, outside_temperature, solar_irradiation, hour_of_the_day):
        thermostat_temperature = self.thermostat_temperature[hour_of_the_day]
        needed_heating_demand = self.heating_demand_for(thermostat_temperature)

        # Update inside temperature if we are heating up
        if self.inside_temperature < thermostat_temperature:
            self.inside_temperature = thermostat_temperature

        # How big is the difference between the temperature inside and outside?
        temperature_difference = self.inside_temperature - outside_temperature

        # How much heat is leaking away in this hour?
        energy_leaking = self.energy_exchange_per_delta_T * temperature_difference

        # How much energy is added by irradiation?
        energy_added_by_irradiation = solar_irradiation * self.window_area

        # What is the inside temperature after the leaking? Update again
        self.inside_temperature = self.inside_temperature - (energy_leaking - energy_added_by_irradiation) / self.heat_capacity

        return needed_heating_demand


    def heating_demand_for(self, thermostat_temperature):
        '''
        Returns the currently needed heating demand for the thermostat temperature
        compared to the inside temperature
        '''
        if self.inside_temperature >= thermostat_temperature:
            return 0.0

        return (thermostat_temperature - self.inside_temperature) * self.heat_capacity


    def set_heat_capacity(self):
        '''Initialise heat capacity'''
        self.heat_capacity = (
            insulation_config.get_heat_capacity(self.house_type) +
            insulation_config.get_behaviour(self.house_type, self.insulation_level)
        )


    def set_energy_exchange(self):
        '''Initialise energy exchage per delta T'''
        U = 1.0 / insulation_config.get_r_values(self.house_type, self.insulation_level)
        # factor 1000 to convert from Watt/K to kW/K
        self.energy_exchange_per_delta_T = (
            U *
            insulation_config.get_surface_area(self.house_type) /
            1000.0
        )
