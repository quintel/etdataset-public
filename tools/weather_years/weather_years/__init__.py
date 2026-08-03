"""Weather-year heat demand curve generator.

Turns one year of temperature, irradiation and wind into the hourly space
heating profiles ETM consumes.

    from weather_years import WeatherInputs, generate_weather_year

    inputs = WeatherInputs.from_paths(
        temperature="air_temperature.csv", irradiation="irradiation.csv"
    )
    curves = generate_weather_year(inputs)
"""

from .curves import Curve, write_curves
from .generator import WeatherYearGenerator, generate_weather_year
from .house_types import INSULATION_LEVELS, NL2019_STOCK, HouseType, profile_keys
from .inputs import WeatherInputs
from .smoothing import PerProfileRandomState, SharedRandomState
from .validation import InputError

__all__ = [
    "INSULATION_LEVELS",
    "NL2019_STOCK",
    "Curve",
    "HouseType",
    "InputError",
    "PerProfileRandomState",
    "SharedRandomState",
    "WeatherInputs",
    "WeatherYearGenerator",
    "generate_weather_year",
    "profile_keys",
    "write_curves",
]
