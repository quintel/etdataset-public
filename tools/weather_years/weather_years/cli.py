"""
Name one or more area codes and both folders are resolved for you:

    python -m weather_years nl

reads `source_analyses/nl/<year>/13_curves/weather_years/` and writes
`data/nl/<year>/13_curves/output/`, for every year that has inputs. `--year`
narrows that to one. Explicit `--temperature`/`--irradiation`/`--output` paths
work as an alternative.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

from .generator import generate_weather_year
from .inputs import WeatherInputs
from .layouts import (
    AreaYear,
    find_etdataset_root,
    source_analyses_area_years,
    write_weather_year,
)
from .smoothing import PerProfileRandomState, SharedRandomState
from .validation import InputError

RANDOMNESS = {"shared": SharedRandomState, "per-profile": PerProfileRandomState}


@dataclass(frozen=True)
class Job:
    """One weather year to generate, and where to put it."""

    label: str
    inputs: WeatherInputs
    output: Path


def _add_area_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "areas",
        nargs="*",
        metavar="AREA",
        help="area codes as they appear in source_analyses/, e.g. nl BE_belgium",
    )
    parser.add_argument(
        "--year",
        help="restrict to one year; without it, every year with inputs is generated",
    )
    parser.add_argument(
        "--etdataset-root",
        type=Path,
        help="etdataset checkout to resolve area codes against (default: detected)",
    )


def _add_explicit_input_arguments(parser: argparse.ArgumentParser) -> None:
    group = parser.add_argument_group(
        "explicit inputs", "Paths to the input curves, instead of an area code."
    )
    group.add_argument("--temperature", type=Path, help="hourly °C, headerless CSV")
    group.add_argument(
        "--irradiation", type=Path, help="hourly J/cm²/h, headerless CSV"
    )
    group.add_argument("--wind-speed", type=Path, help="hourly m/s, headerless CSV")
    group.add_argument(
        "--g2a-parameters", type=Path, help="reference/slope/constant CSV"
    )
    group.add_argument(
        "--thermostat",
        type=Path,
        help="24-row low/medium/high CSV; defaults to the packaged ECN schedule",
    )


def _area_years(args: argparse.Namespace) -> list[AreaYear]:
    """Resolve every area code, failing on one that has nothing to generate."""
    root = args.etdataset_root or find_etdataset_root()
    resolved = []

    for area in args.areas:
        found = source_analyses_area_years(root, area, args.year)

        if not found:
            looked_in = Path(root) / "source_analyses" / area
            for_year = f" for year {args.year}" if args.year else ""
            raise SystemExit(f"No weather inputs{for_year} under {looked_in}.")
        resolved.extend(found)

    return resolved


def _area_jobs(args: argparse.Namespace) -> list[Job]:
    area_years = _area_years(args)

    if args.output and len(area_years) > 1:
        listed = ", ".join(str(area_year) for area_year in area_years)
        raise SystemExit(
            f"--output takes one destination but {len(area_years)} weather years "
            f"were resolved ({listed}). Add --year, or name one area at a time."
        )

    return [
        Job(
            label=str(area_year),
            inputs=area_year.inputs(args.thermostat),
            output=args.output or area_year.output_folder,
        )
        for area_year in area_years
    ]


def _explicit_job(args: argparse.Namespace) -> Job:
    if not (args.temperature and args.irradiation and args.output):
        raise SystemExit(
            "Name an area code, or give --temperature, --irradiation and --output."
        )

    return Job(
        label=str(args.temperature),
        inputs=WeatherInputs.from_paths(
            temperature=args.temperature,
            irradiation=args.irradiation,
            thermostat=args.thermostat,
            wind_speed=args.wind_speed,
            g2a_parameters=args.g2a_parameters,
        ),
        output=args.output,
    )


def build_jobs(args: argparse.Namespace) -> list[Job]:
    """Resolve every weather year to generate, reading and validating its inputs.

    All inputs are read before anything is written, so a bad area code cannot
    leave half the run's output folders rewritten.
    """
    if args.areas:
        return _area_jobs(args)
    if args.year:
        raise SystemExit("--year needs at least one area code.")

    return [_explicit_job(args)]


def run(job: Job, smoothing: str) -> None:
    curves = generate_weather_year(job.inputs, randomness=RANDOMNESS[smoothing]())
    written = write_weather_year(curves, job.inputs, job.output)

    print(f"{job.label}: wrote {len(written)} files to {job.output}")
    if not job.inputs.has_building_inputs:
        missing = ", ".join(
            name
            for name, value in (
                ("wind speed", job.inputs.wind_speed),
                ("G2A parameters", job.inputs.g2a_parameters),
            )
            if value is None
        )
        print(
            f"  no {missing}, so buildings_heating and agriculture_heating were "
            "not generated"
        )


def generate(args: argparse.Namespace) -> int:
    for job in build_jobs(args):
        run(job, args.smoothing)

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="weather_years", description=__doc__.splitlines()[0]
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="destination folder; derived from the area code when one is given",
    )
    parser.add_argument(
        "--smoothing",
        choices=sorted(RANDOMNESS),
        default="shared",
        help=(
            "'shared' (default) reproduces the weather years ETM ships and is "
            "order-dependent; 'per-profile' is reproducible per curve and moves "
            "every value"
        ),
    )
    _add_area_arguments(parser)
    _add_explicit_input_arguments(parser)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        return generate(args)
    except FileNotFoundError as error:
        print(f"error: no such file: {error.filename}", file=sys.stderr)
    except InputError as error:
        print(f"error: {error}", file=sys.stderr)

    return 2


if __name__ == "__main__":
    sys.exit(main())
