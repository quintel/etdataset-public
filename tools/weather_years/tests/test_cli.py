"""The command line: area codes, explicit paths, and where the files land."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

from weather_years import Curve, profile_keys
from weather_years.cli import build_jobs, build_parser, main
from weather_years.layouts import (
    SOURCE_ANALYSES_INPUTS,
    TEMPERATURE_FILE,
    find_etdataset_root,
)

PACKAGE_ROOT = Path(__file__).resolve().parents[1]

#: What a households-only run writes: the 12 profiles and the temperature it used.
HOUSEHOLD_FILES = set(profile_keys()) | {"air_temperature"}
NON_RESIDENTIAL_FILES = {"buildings_heating", "agriculture_heating"}


def parse(argv):
    return build_parser().parse_args(argv)


def explicit_paths(input_folder):
    """The `--temperature`-style flags for every input the folder holds."""
    flags = {
        TEMPERATURE_FILE: "--temperature",
        "irradiation.csv": "--irradiation",
        "wind_speed.csv": "--wind-speed",
        "G2A_parameters.csv": "--g2a-parameters",
    }
    argv = []

    for name, flag in flags.items():
        if (input_folder / name).exists():
            argv += [flag, str(input_folder / name)]

    return argv


def checkout(root, input_folder, area="nl", year="2023"):
    """A minimal etdataset checkout holding one area-year of weather inputs."""
    inputs = root / "source_analyses" / area / year / SOURCE_ANALYSES_INPUTS
    inputs.mkdir(parents=True, exist_ok=True)
    for source in input_folder.glob("*.csv"):
        (inputs / source.name).write_bytes(source.read_bytes())
    (root / "data").mkdir(exist_ok=True)

    return root


def output_folder(root, area="nl", year="2023"):
    return root / "data" / area / year / "13_curves" / "output"


def written(folder):
    return {path.stem for path in folder.glob("*.csv")}


def test_an_area_code_reads_and_writes_the_etdataset_folders(
    full_input_folder, tmp_path
):
    """The one-argument path: `python -m weather_years nl`."""
    root = checkout(tmp_path, full_input_folder)

    assert main(["nl", "--etdataset-root", str(root)]) == 0
    assert written(output_folder(root)) == HOUSEHOLD_FILES | NON_RESIDENTIAL_FILES


def test_explicit_paths_write_the_curves_and_the_temperature(
    household_input_folder, tmp_path
):
    argv = [*explicit_paths(household_input_folder), "--output", str(tmp_path)]

    assert main(argv) == 0
    assert written(tmp_path) == HOUSEHOLD_FILES

    passed_through = Curve.read_csv(tmp_path / TEMPERATURE_FILE).values
    source = Curve.read_csv(household_input_folder / TEMPERATURE_FILE).values
    assert np.allclose(passed_through, source, rtol=1e-12)


def test_a_households_only_run_says_what_it_could_not_generate(
    household_input_folder, tmp_path, capsys
):
    """Missing wind and G2A parameters are reported, not silently skipped."""
    main([*explicit_paths(household_input_folder), "--output", str(tmp_path)])

    assert "wind speed, G2A parameters" in capsys.readouterr().out


def test_every_year_with_inputs_is_generated_unless_a_year_is_named(
    household_input_folder, tmp_path
):
    root = checkout(tmp_path, household_input_folder, year="2023")
    checkout(root, household_input_folder, year="2019")
    argv = ["nl", "--etdataset-root", str(root)]

    assert [job.label for job in build_jobs(parse(argv))] == ["nl 2019", "nl 2023"]
    assert [job.label for job in build_jobs(parse([*argv, "--year", "2019"]))] == [
        "nl 2019"
    ]


def test_output_is_refused_for_more_than_one_weather_year(
    household_input_folder, tmp_path
):
    """One folder cannot hold two weather years without silently clobbering."""
    root = checkout(tmp_path / "repo", household_input_folder, year="2023")
    checkout(root, household_input_folder, year="2019")
    argv = ["nl", "--etdataset-root", str(root), "--output", str(tmp_path)]

    with pytest.raises(SystemExit, match="nl 2019, nl 2023"):
        build_jobs(parse(argv))


def test_the_checkout_is_found_by_searching_upwards(household_input_folder, tmp_path):
    """An area code resolves the same wherever the tool is run from, and a
    checkout nested inside another resolves to the inner one."""
    inner = checkout(tmp_path / "outer" / "etdataset", household_input_folder)
    checkout(tmp_path / "outer", household_input_folder)

    assert find_etdataset_root(inner / "tools" / "weather_years") == inner


BAD_ARGUMENTS = {
    "no inputs at all": (["--output", "."], "area code"),
    "a year without an area": (["--year", "2023"], "area code"),
    "an unknown area": (["xx"], "source_analyses/xx"),
    "an unknown year": (["nl", "--year", "1066"], "year 1066"),
}


@pytest.mark.parametrize(
    ("argv", "expected"), BAD_ARGUMENTS.values(), ids=BAD_ARGUMENTS
)
def test_bad_arguments_exit_saying_what_is_wrong(
    household_input_folder, tmp_path, argv, expected
):
    root = checkout(tmp_path, household_input_folder)

    with pytest.raises(SystemExit, match=expected):
        build_jobs(parse([*argv, "--etdataset-root", str(root)]))


def test_a_missing_input_file_exits_2_naming_the_file(
    household_input_folder, tmp_path, capsys
):
    argv = [
        "--temperature",
        str(tmp_path / "nope.csv"),
        "--irradiation",
        str(household_input_folder / "irradiation.csv"),
        "--output",
        str(tmp_path),
    ]

    assert main(argv) == 2
    assert "nope.csv" in capsys.readouterr().err


def test_two_runs_write_identical_files(full_input_folder, tmp_path):
    """A diff between two output folders means a real change, never run noise."""
    folders = [tmp_path / "first", tmp_path / "second"]

    for folder in folders:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "weather_years",
                *explicit_paths(full_input_folder),
                "--output",
                str(folder),
            ],
            cwd=PACKAGE_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )

    first, second = (sorted(folder.glob("*.csv")) for folder in folders)
    assert [path.name for path in first] == [path.name for path in second]

    for left, right in zip(first, second):
        assert left.read_bytes() == right.read_bytes(), f"{left.name} differs"
