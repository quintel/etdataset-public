"""Synthetic weather carrying the features the generator reacts to.

Nothing here is 'actual' weather. The fixtures are sine waves: a cold winter and
a warm summer, a daily cycle, daylight-shaped irradiation, windy spells and G2A
parameters in the magnitudes expected. Tests can then assert how a curve
responds to the weather rather than what it came out as, which keeps them true
when the input year changes.

Wind is deliberately given a period that divides neither the day nor the year,
so a test claiming wind moves a curve cannot be passing on the temperature
signal instead.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from weather_years import WeatherInputs
from weather_years.constants import HOURS_PER_DAY, HOURS_PER_YEAR

#: A period aligning with neither the daily nor the annual cycle.
WIND_PERIOD = 97


def sine_year(mean: float, amplitude: float, phase: float = 0.0) -> np.ndarray:
    """A smooth year-long curve."""
    hours = np.arange(HOURS_PER_YEAR)

    return mean + amplitude * np.sin(2 * np.pi * (hours / HOURS_PER_YEAR) + phase)


@pytest.fixture(scope="session")
def synthetic_temperature() -> np.ndarray:
    """A year swinging between roughly -5 °C and 25 °C, coldest in January."""
    daily = 3 * np.sin(2 * np.pi * np.arange(HOURS_PER_YEAR) / HOURS_PER_DAY)

    return sine_year(mean=10.0, amplitude=12.0, phase=-np.pi / 2) + daily


@pytest.fixture(scope="session")
def synthetic_irradiation() -> np.ndarray:
    """A year of daylight-shaped irradiation peaking near 300 J/cm²/h."""
    hour_of_day = np.arange(HOURS_PER_YEAR) % HOURS_PER_DAY
    daylight = np.clip(np.sin(np.pi * (hour_of_day - 6) / 12), 0, None)

    return daylight * sine_year(mean=200.0, amplitude=100.0, phase=-np.pi / 2)


@pytest.fixture(scope="session")
def synthetic_wind_speed() -> np.ndarray:
    """Windy spells between 0 and 10 m/s, uncorrelated with anything."""
    hours = np.arange(HOURS_PER_YEAR)

    return 5.0 + 5.0 * np.sin(2 * np.pi * hours / WIND_PERIOD)


@pytest.fixture(scope="session")
def synthetic_g2a_parameters() -> pd.DataFrame:
    """Hourly G2A parameters in the magnitudes expected."""
    hour_of_day = np.arange(HOURS_PER_YEAR) % HOURS_PER_DAY
    daily = np.sin(2 * np.pi * (hour_of_day - 6) / HOURS_PER_DAY)

    return pd.DataFrame(
        {
            "reference": 11.0 + 4.0 * daily,
            "slope": np.full(HOURS_PER_YEAR, 1.4e-5),
            "constant": 3.0e-5 + 1.0e-5 * daily,
        }
    )


@pytest.fixture(scope="session")
def synthetic_inputs(synthetic_temperature, synthetic_irradiation) -> WeatherInputs:
    """Households only: no wind speed and no G2A parameters."""
    return WeatherInputs.create(
        temperature=synthetic_temperature, irradiation=synthetic_irradiation
    )


@pytest.fixture(scope="session")
def synthetic_full_inputs(
    synthetic_temperature,
    synthetic_irradiation,
    synthetic_wind_speed,
    synthetic_g2a_parameters,
) -> WeatherInputs:
    """Everything the generator expects."""
    return WeatherInputs.create(
        temperature=synthetic_temperature,
        irradiation=synthetic_irradiation,
        wind_speed=synthetic_wind_speed,
        g2a_parameters=synthetic_g2a_parameters,
    )


def _write_input_folder(folder: Path, inputs: WeatherInputs) -> Path:
    """Lay a `WeatherInputs` out on disk as an area's input folder.

    Only the series the inputs actually carry are written, so a households-only
    fixture produces a households-only folder.
    """
    folder.mkdir(parents=True, exist_ok=True)
    pd.Series(inputs.temperature).to_csv(
        folder / "air_temperature.csv", index=False, header=False
    )
    pd.Series(inputs.irradiation).to_csv(
        folder / "irradiation.csv", index=False, header=False
    )

    if inputs.wind_speed is not None:
        pd.Series(inputs.wind_speed).to_csv(
            folder / "wind_speed.csv", index=False, header=False
        )
    if inputs.g2a_parameters is not None:
        inputs.g2a_parameters.to_csv(folder / "G2A_parameters.csv", index=False)

    return folder


@pytest.fixture(scope="session")
def household_input_folder(tmp_path_factory, synthetic_inputs) -> Path:
    """A folder of temperature and irradiation CSVs, shared across tests."""
    return _write_input_folder(tmp_path_factory.mktemp("households"), synthetic_inputs)


@pytest.fixture(scope="session")
def full_input_folder(tmp_path_factory, synthetic_full_inputs) -> Path:
    """A folder carrying every input, shared across tests."""
    return _write_input_folder(tmp_path_factory.mktemp("full"), synthetic_full_inputs)
