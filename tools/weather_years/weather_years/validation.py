"""Input checks that fail loudly rather than producing plausible wrong curves."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .constants import HOURS_PER_DAY, HOURS_PER_YEAR
from .house_types import INSULATION_LEVELS

#: Surface air temperature records leave a wide margin around [-90, 60] °C.
MIN_PLAUSIBLE_TEMPERATURE = -90.0
MAX_PLAUSIBLE_TEMPERATURE = 60.0
#: 0 °C in kelvin is 273.15; nothing in °C reaches 150.
KELVIN_THRESHOLD = 150.0

#: 1000 W/m² of full sunshine is 360 J/cm²/h. Observed maxima run 275-365.
MAX_PLAUSIBLE_IRRADIATION = 400.0

MAX_PLAUSIBLE_WIND_SPEED = 120.0  # m/s; the record gust is 113


class InputError(ValueError):
    """An input cannot be used as given."""


def validate_length(curve: np.ndarray, name: str) -> None:
    if len(curve) != HOURS_PER_YEAR:
        raise InputError(
            f"{name} must have {HOURS_PER_YEAR} hourly values, got {len(curve)}."
        )


def validate_temperature(temperature: np.ndarray) -> None:
    """Reject kelvin and physically impossible temperatures."""
    validate_length(temperature, "Temperature")

    if temperature.min() >= KELVIN_THRESHOLD:
        raise InputError(
            f"Temperature is expected in °C, but the minimum is "
            f"{temperature.min():.1f}, which looks like kelvin. Subtract 273.15."
        )
    if (
        temperature.min() < MIN_PLAUSIBLE_TEMPERATURE
        or temperature.max() > MAX_PLAUSIBLE_TEMPERATURE
    ):
        raise InputError(
            f"Temperature in °C is expected within "
            f"[{MIN_PLAUSIBLE_TEMPERATURE}, {MAX_PLAUSIBLE_TEMPERATURE}], got "
            f"[{temperature.min():.1f}, {temperature.max():.1f}]."
        )


def validate_irradiation(irradiation: np.ndarray) -> None:
    """Reject W/m² and negative irradiation."""
    validate_length(irradiation, "Irradiation")

    if irradiation.min() < 0:
        raise InputError(
            f"Irradiation cannot be negative, got a minimum of {irradiation.min():.1f}."
        )
    if irradiation.max() > MAX_PLAUSIBLE_IRRADIATION:
        raise InputError(
            f"Irradiation is expected in J/cm²/h (the KNMI convention), where full "
            f"sunshine is about 360. The maximum here is {irradiation.max():.1f}, "
            "which suggests W/m² (the ERA5/PVGIS convention). Convert with "
            "`j_cm2 = w_m2 * 3600 / 1e4`."
        )


def validate_thermostat(thermostat: pd.DataFrame) -> None:
    missing = [level for level in INSULATION_LEVELS if level not in thermostat.columns]
    if missing:
        raise InputError(f"Thermostat settings are missing columns: {missing}.")
    if len(thermostat) != HOURS_PER_DAY:
        raise InputError(
            f"Thermostat settings must have {HOURS_PER_DAY} rows, one per hour of the "
            f"day, got {len(thermostat)}."
        )


def validate_wind_speed(wind_speed: np.ndarray) -> None:
    validate_length(wind_speed, "Wind speed")

    if wind_speed.min() < 0 or wind_speed.max() > MAX_PLAUSIBLE_WIND_SPEED:
        raise InputError(
            f"Wind speed is expected in m/s within [0, {MAX_PLAUSIBLE_WIND_SPEED}], got "
            f"[{wind_speed.min():.1f}, {wind_speed.max():.1f}]. Values above this "
            "suggest km/h."
        )


def validate_g2a_parameters(g2a_parameters: pd.DataFrame) -> None:
    required = ("reference", "slope", "constant")
    missing = [column for column in required if column not in g2a_parameters.columns]
    if missing:
        raise InputError(f"G2A parameters are missing columns: {missing}.")
    if len(g2a_parameters) not in (1, HOURS_PER_YEAR):
        raise InputError(
            f"G2A parameters must have 1 row (constant) or {HOURS_PER_YEAR} rows "
            f"(hourly), got {len(g2a_parameters)}."
        )
