"""The explicit-path interface to the weather-year generator."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from .house_types import INSULATION_LEVELS
from .validation import (
    validate_g2a_parameters,
    validate_irradiation,
    validate_temperature,
    validate_thermostat,
    validate_wind_speed,
)

PathLike = str | Path

#: ECN thermostat schedule, shipped so the tool works from any directory.
DEFAULT_THERMOSTAT_PATH = Path(__file__).parent / "data" / "thermostat.csv"


def read_curve(path: PathLike) -> np.ndarray:
    """Read a headerless single-column hourly CSV."""
    return pd.read_csv(path, header=None)[0].to_numpy(dtype=float)


def read_table(path: PathLike) -> pd.DataFrame:
    """Read a CSV with a header row."""
    return pd.read_csv(path)


def default_thermostat() -> pd.DataFrame:
    return read_table(DEFAULT_THERMOSTAT_PATH)


def _as_year(curve: np.ndarray | None) -> np.ndarray | None:
    return None if curve is None else np.asarray(curve, dtype=float)


@dataclass(frozen=True)
class WeatherInputs:
    """One year of weather, validated and ready to generate from.

    Attributes:
        temperature: 8760 hourly outdoor temperatures in °C.
        irradiation: 8760 hourly global irradiation values in J/cm²/h.
        thermostat: 24 rows of setpoints in °C, columns low/medium/high.
        wind_speed: 8760 hourly wind speeds in m/s; buildings and agriculture only.
        g2a_parameters: 1 or 8760 rows of reference/slope/constant; buildings and
            agriculture only.
    """

    temperature: np.ndarray
    irradiation: np.ndarray
    thermostat: pd.DataFrame
    wind_speed: np.ndarray | None = None
    g2a_parameters: pd.DataFrame | None = None

    def __post_init__(self) -> None:
        validate_temperature(self.temperature)
        validate_irradiation(self.irradiation)
        validate_thermostat(self.thermostat)

        if self.wind_speed is not None:
            validate_wind_speed(self.wind_speed)
        if self.g2a_parameters is not None:
            validate_g2a_parameters(self.g2a_parameters)

    @classmethod
    def create(
        cls,
        temperature: np.ndarray,
        irradiation: np.ndarray,
        thermostat: pd.DataFrame | None = None,
        wind_speed: np.ndarray | None = None,
        g2a_parameters: pd.DataFrame | None = None,
    ) -> WeatherInputs:
        """Build from in-memory series."""
        return cls(
            temperature=_as_year(temperature),
            irradiation=_as_year(irradiation),
            thermostat=default_thermostat() if thermostat is None else thermostat,
            wind_speed=_as_year(wind_speed),
            g2a_parameters=g2a_parameters,
        )

    @classmethod
    def from_paths(
        cls,
        temperature: PathLike,
        irradiation: PathLike,
        thermostat: PathLike | None = None,
        wind_speed: PathLike | None = None,
        g2a_parameters: PathLike | None = None,
    ) -> WeatherInputs:
        """Build from CSV paths. Only temperature and irradiation are required."""
        return cls.create(
            temperature=read_curve(temperature),
            irradiation=read_curve(irradiation),
            thermostat=None if thermostat is None else read_table(thermostat),
            wind_speed=None if wind_speed is None else read_curve(wind_speed),
            g2a_parameters=(
                None if g2a_parameters is None else read_table(g2a_parameters)
            ),
        )

    @property
    def has_building_inputs(self) -> bool:
        """Whether buildings and agriculture profiles can be generated."""
        return self.wind_speed is not None and self.g2a_parameters is not None

    def thermostat_setpoints(self, insulation_level: str) -> np.ndarray:
        """The 24 setpoints for one insulation level, in °C."""
        return self.thermostat[insulation_level].to_numpy(dtype=float)

    def setpoints_by_level(self) -> dict[str, np.ndarray]:
        return {level: self.thermostat_setpoints(level) for level in INSULATION_LEVELS}


__all__ = [
    "DEFAULT_THERMOSTAT_PATH",
    "WeatherInputs",
    "default_thermostat",
    "read_curve",
    "read_table",
]
