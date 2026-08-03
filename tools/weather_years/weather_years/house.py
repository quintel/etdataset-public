"""Single-house thermal model.

Each hour the house compares its indoor temperature to the thermostat setpoint
and demands heat if it is too cold, then loses heat through the envelope and
gains heat from sunlight through the windows. Indoor temperature carries over
between hours, so the house has thermal inertia.

Known limitation: indoor temperature has no ceiling, so a well-insulated house
accumulates solar gain it would in reality vent through an open window.
"""

from __future__ import annotations

import numpy as np

from .constants import HEAT_CAPACITY_HOUSE, HOURS_PER_DAY
from .house_types import HouseType


class House:
    """A house of one type at one insulation level, stepped hour by hour."""

    def __init__(
        self,
        house_type: HouseType,
        insulation_level: str,
        thermostat: np.ndarray,
    ) -> None:
        """
        Args:
            thermostat: 24 setpoints in °C, one per hour of the day.
        """
        self.house_type = house_type
        self.insulation_level = insulation_level
        self.thermostat_temperature = thermostat
        self.inside_temperature = float(thermostat[0])

        self.heat_capacity = HEAT_CAPACITY_HOUSE + house_type.behaviour(
            insulation_level
        )
        self.energy_exchange_per_delta_T = self._energy_exchange_per_delta_T()

    def _energy_exchange_per_delta_T(self) -> float:
        """Envelope heat loss in kW/K."""
        u_value = 1.0 / self.house_type.r_value(self.insulation_level)
        # Factor 1000 converts W/K to kW/K.
        return u_value * self.house_type.surface_area / 1000.0

    def calculate_heat_demand(
        self,
        outside_temperature: float,
        solar_irradiation: float,
        hour_of_the_day: int,
    ) -> float:
        """Heat demand in kWh for one hour, advancing the indoor temperature.

        Args:
            outside_temperature: °C
            solar_irradiation: kWh/m² over the hour
        """
        setpoint = self.thermostat_temperature[hour_of_the_day]
        needed_heating_demand = self.heating_demand_for(setpoint)

        if self.inside_temperature < setpoint:
            self.inside_temperature = setpoint

        energy_leaking = self.energy_exchange_per_delta_T * (
            self.inside_temperature - outside_temperature
        )
        energy_added_by_irradiation = solar_irradiation * self.house_type.window_area

        self.inside_temperature -= (
            energy_leaking - energy_added_by_irradiation
        ) / self.heat_capacity

        return needed_heating_demand

    def heating_demand_for(self, setpoint: float) -> float:
        """kWh needed to lift the indoor temperature to the setpoint."""
        if self.inside_temperature >= setpoint:
            return 0.0

        return (setpoint - self.inside_temperature) * self.heat_capacity


def raw_heat_demand(
    house_type: HouseType,
    insulation_level: str,
    temperature: np.ndarray,
    irradiation: np.ndarray,
    thermostat: np.ndarray,
) -> np.ndarray:
    """Unsmoothed hourly heat demand of a single house over the year, in kWh.

    Args:
        temperature: hourly outdoor temperature in °C.
        irradiation: hourly solar irradiation in kWh/m².
        thermostat: 24 setpoints in °C.
    """
    house = House(house_type, insulation_level, thermostat)

    return np.array(
        [
            house.calculate_heat_demand(
                temperature[hour], irradiation[hour], hour % HOURS_PER_DAY
            )
            for hour in range(len(temperature))
        ]
    )
