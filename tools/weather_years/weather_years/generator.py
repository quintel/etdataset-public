"""Turn a year of weather into the heat-demand profiles ETM consumes.

Two independent methods live here:

- **Households**: the physical house model in `house.py`, smoothed to a
  neighbourhood. One profile per house type per insulation level.
- **Buildings and agriculture**: the Dutch gas-sector G2A formula. Demand rises
  linearly once an effective temperature (temperature corrected for wind chill)
  falls below a reference point. Both sectors get the same profile.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .constants import CM2_TO_M2, J_TO_KWH
from .curves import Curve, normalize
from .house import raw_heat_demand
from .house_types import INSULATION_LEVELS, NL2019_STOCK, HouseType
from .inputs import WeatherInputs
from .smoothing import Randomness, SharedRandomState, calculate_smoothed_demand

#: Wind chill divisor in the Dutch NEDU/KNMI effective-temperature convention.
WIND_CHILL_DIVISOR = 1.5


def to_kwh_m2(irradiation: np.ndarray) -> np.ndarray:
    """Convert irradiation from J/cm²/h to kWh/m²."""
    return irradiation * J_TO_KWH / CM2_TO_M2


class WeatherYearGenerator:
    """Generates a weather year's heat-demand profiles from explicit inputs."""

    def __init__(
        self,
        inputs: WeatherInputs,
        stock: tuple[HouseType, ...] = NL2019_STOCK,
        randomness: Randomness | None = None,
    ) -> None:
        """
        Args:
            stock: the housing stock to generate profiles for. Its order is part
                of the result whenever `randomness` shares one stream.
            randomness: defaults to a fresh `SharedRandomState`, which reproduces
                every weather year ETM ships.
        """
        self.inputs = inputs
        self.stock = stock
        self.randomness = SharedRandomState() if randomness is None else randomness

    def generate(self) -> list[Curve]:
        """All profiles the inputs allow: 12 household, plus 2 if wind and G2A."""
        curves = self.household_profiles()

        if self.inputs.has_building_inputs:
            curves.extend(self.building_profiles())

        return curves

    def household_profiles(self) -> list[Curve]:
        """One profile per house type per insulation level, house-major."""
        irradiation = to_kwh_m2(self.inputs.irradiation)

        return [
            self._household_profile(house, level, irradiation)
            for house in self.stock
            for level in INSULATION_LEVELS
        ]

    def household_profile(self, house_type_name: str, insulation_level: str) -> Curve:
        """A single household profile.

        Under `SharedRandomState` this does *not* reproduce the profile's value
        in a full-set run — the shared stream makes a profile depend on how many
        were generated before it. Use `PerProfileRandomState` for that.
        """
        house = next(h for h in self.stock if h.name == house_type_name)

        return self._household_profile(
            house, insulation_level, to_kwh_m2(self.inputs.irradiation)
        )

    def _household_profile(
        self, house: HouseType, insulation_level: str, irradiation: np.ndarray
    ) -> Curve:
        key = f"insulation_{house.name}_{insulation_level}"
        demand = raw_heat_demand(
            house,
            insulation_level,
            self.inputs.temperature,
            irradiation,
            self.inputs.thermostat_setpoints(insulation_level),
        )
        smoothed = calculate_smoothed_demand(
            demand, insulation_level, self.randomness, key
        )

        return Curve(key, normalize(smoothed))

    def building_profiles(self) -> list[Curve]:
        """Buildings and agriculture, which share one G2A profile."""
        profile = self._g2a_profile()

        return [
            Curve("buildings_heating", profile.copy()),
            Curve("agriculture_heating", profile.copy()),
        ]

    def _g2a_profile(self) -> np.ndarray:
        effective = self.inputs.temperature - (
            self.inputs.wind_speed / WIND_CHILL_DIVISOR
        )
        reference, slope, constant = self._g2a_columns()
        demand = np.where(
            effective < reference, (reference - effective) * slope + constant, constant
        )

        return normalize(demand)

    def _g2a_columns(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Reference, slope and constant broadcast to one value per hour."""
        parameters: pd.DataFrame = self.inputs.g2a_parameters

        return tuple(
            parameters[column].to_numpy(dtype=float)
            for column in ("reference", "slope", "constant")
        )


def generate_weather_year(
    inputs: WeatherInputs,
    stock: tuple[HouseType, ...] = NL2019_STOCK,
    randomness: Randomness | None = None,
) -> list[Curve]:
    """Convenience wrapper over `WeatherYearGenerator.generate`."""
    return WeatherYearGenerator(inputs, stock, randomness).generate()
