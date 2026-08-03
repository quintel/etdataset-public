"""Resolving an area code to the folders etdataset keeps its weather curves in.

An area and year read from `source_analyses/<area>/<year>/13_curves/weather_years/`
and write to `data/<area>/<year>/13_curves/output/`.

An optional input that is not there is left unset rather than guessed at, so a
folder with no wind series yields household curves and no error. A year is only
offered if its input folder exists, so discovery never proposes a year that
would then fail to read.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .curves import Curve
from .inputs import PathLike, WeatherInputs
from .validation import InputError

#: Name a weather-year folder gives the temperature it was generated from.
TEMPERATURE_FILE = "air_temperature.csv"

#: Where the 13_curves pipeline keeps a year's weather inputs, under its area.
SOURCE_ANALYSES_INPUTS = Path("13_curves") / "weather_years"


def _optional(path: Path) -> Path | None:
    return path if path.exists() else None


def find_etdataset_root(start: PathLike | None = None) -> Path:
    """The nearest ancestor holding both `source_analyses/` and `data/`.

    Searched from this package rather than the working directory, so an area
    code resolves the same way wherever the tool is run from.
    """
    origin = Path(start).resolve() if start else Path(__file__).resolve()

    for candidate in (origin, *origin.parents):
        if (candidate / "source_analyses").is_dir() and (candidate / "data").is_dir():
            return candidate

    raise InputError(
        f"No etdataset checkout found above {origin} — looked for a folder "
        "holding both source_analyses/ and data/. Pass --etdataset-root, or give "
        "the input paths explicitly."
    )


@dataclass(frozen=True)
class AreaYear:
    """One area and year, resolved to the folders it reads from and writes to."""

    area: str
    year: str
    input_folder: Path
    output_folder: Path

    def __str__(self) -> str:
        return f"{self.area} {self.year}"

    def inputs(self, thermostat: PathLike | None = None) -> WeatherInputs:
        """Read and validate every input the folder holds."""
        return WeatherInputs.from_paths(
            temperature=self.input_folder / TEMPERATURE_FILE,
            irradiation=self.input_folder / "irradiation.csv",
            thermostat=thermostat or _optional(self.input_folder / "thermostat.csv"),
            wind_speed=_optional(self.input_folder / "wind_speed.csv"),
            g2a_parameters=_optional(self.input_folder / "G2A_parameters.csv"),
        )


def _years_with_inputs(
    area_folder: Path, inputs_within_year: PathLike, year: str | None
) -> list[str]:
    """Year folders under an area that actually hold weather inputs."""
    if not area_folder.is_dir():
        return []

    return sorted(
        path.name
        for path in area_folder.iterdir()
        if (path / inputs_within_year).is_dir()
        and (year is None or path.name == str(year))
    )


def source_analyses_area_years(
    etdataset_root: PathLike, area: str, year: str | None = None
) -> list[AreaYear]:
    """Every year of `source_analyses/<area>/` that has weather inputs."""
    root = Path(etdataset_root)
    area_folder = root / "source_analyses" / area

    return [
        AreaYear(
            area=area,
            year=found,
            input_folder=area_folder / found / SOURCE_ANALYSES_INPUTS,
            output_folder=root / "data" / area / found / "13_curves" / "output",
        )
        for found in _years_with_inputs(area_folder, SOURCE_ANALYSES_INPUTS, year)
    ]


def write_weather_year(
    curves: list[Curve], inputs: WeatherInputs, directory: PathLike
) -> list[Path]:
    """Write the curves plus the pass-through temperature, as etsource expects.

    Existing files are overwritten. A weather-year folder that half-matches its
    inputs is worse than one that is simply rewritten.
    """
    folder = Path(directory)
    written = [curve.write_csv(folder) for curve in curves]
    written.append(
        Curve(Path(TEMPERATURE_FILE).stem, inputs.temperature).write_csv(folder)
    )

    return written


__all__ = [
    "SOURCE_ANALYSES_INPUTS",
    "TEMPERATURE_FILE",
    "AreaYear",
    "find_etdataset_root",
    "source_analyses_area_years",
    "write_weather_year",
]
