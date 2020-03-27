# Class to hold a scenario
class House:
    """Class to describe a house"""

    def __init__(self, initial_values, house_type, insulation_level):

        self.house_type = house_type
        self.insulation_level = insulation_level

        # Behaviour factor
        self.behaviour = initial_values['behaviour'][self.house_type][self.insulation_level]

        # Area
        self.surface_area = initial_values['surface_area'][self.house_type]
        self.window_area = initial_values['window_area'][self.house_type]

        # Temperarture
        self.thermostat_temperature = initial_values['thermostat_vectors'][self.insulation_level]
        self.inside_temperature = self.thermostat_temperature[0]

        # R-value and heat capacity
        self.r_value = initial_values['r_values'][self.house_type][self.insulation_level]
        self.heat_capacity = initial_values['heat_capacity'][self.house_type] + self.behaviour
        self.U = 1.0 / self.r_value
        self.energy_exchange_per_delta_T = self.U * self.surface_area / 1000.0 # factor 1000 to convert from Watt/K to kW/K

    def Calculate_heat_demand(self, outside_temperature, solar_irradiation, hour_of_the_day, debugging = False):

        thermostat_temperature = self.thermostat_temperature[hour_of_the_day]
        if debugging:
            print("thermostat_temperature", thermostat_temperature, "C")

        # How much energy is needed from heating to bridge the temperature gap?
        if self.inside_temperature < thermostat_temperature:

            needed_heating_demand = (thermostat_temperature - self.inside_temperature) * self.heat_capacity
            if debugging:
                print("needed_heating_demand", needed_heating_demand, "kWh")

        else:

            needed_heating_demand = 0.0

        # Updating the inside temperature
        if self.inside_temperature < thermostat_temperature:

            self.inside_temperature = thermostat_temperature

        # How big is the difference between the temperature inside and outside?
        temperature_difference = self.inside_temperature - outside_temperature
        if debugging:
            print("temperature_difference", temperature_difference, "C")

        # How much heat is leaking away in this hour?
        energy_leaking = self.energy_exchange_per_delta_T * temperature_difference
        if debugging:
            print("Leaking", energy_leaking, "kWh")

        # How much energy is added by irradiation?
        energy_added_by_irradiation = solar_irradiation * self.window_area
        if debugging:
            print("energy_added_by_irradiation", energy_added_by_irradiation, "kWh")

        # What is the inside temperature after the leaking?
        self.inside_temperature = self.inside_temperature - (energy_leaking - energy_added_by_irradiation) / self.heat_capacity
        if debugging:
            print("inside_temperature", self.inside_temperature, "C")

        return needed_heating_demand


    def info(self):
        print("========")
        print("R_value: " + str(self.r_value))
        #print("U = 1/R_value = " + str(self.U))
        #print("Leaking kW/K " + str(self.energy_exchange_per_delta_T))
        print("Thermostat ", self.thermostat_temperature)
        print("Heat capacity ", self.heat_capacity)
        print("surface area", self.surface_area)
        print("behaviour factor", self.behaviour)

