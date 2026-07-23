"""
Structural validation for emissions data.

Verifies hard requirements:
- File completeness
- Required columns
- Required CRT codes
- No duplicate codes
"""

from __future__ import annotations
from pathlib import Path
import pandas as pd

from ..config import (
    COL_OUT_CODE,
    COL_OUT_CATEGORY,
    COL_OUT_UNIT,
    COL_OUT_CO2,
    COL_OUT_OTHER,
    COL_OUT_TOTAL,
    REQUIRED_CODES,
    MOBILE_MACHINERY_CRT_CODES,
    VALIDATION_MIN_ROWS,
)


def verify_outputs(
    saved: list[Path],
    expected: set[tuple[str, int]],
    output_dir: Path,
    nl_folder: str = "nl",
) -> tuple[list[str], list[str]]:
    """
    Structural verification on pipeline output files.

    Checks:
    1. File completeness (all expected files exist)
    2. Correct columns present
    3. Required top-level CRT sector codes (1-5)
    4. NL off-road sub-category codes (for NL datasets)
    5. No duplicate CRT codes
    6. (Soft) Sector-1 CO2 is not null
    7. (Soft) Minimum row count

    Args:
        saved: List of saved file paths
        expected: Set of (dataset_folder, year) tuples expected
        output_dir: Base output directory
        nl_folder: Folder name for NL datasets (default: "nl")

    Returns:
        Tuple of (fails, warns) lists
        - fails: Hard errors that must be fixed
        - warns: Soft warnings for review
    """
    fails: list[str] = []
    warns: list[str] = []

    _check_file_completeness(expected, output_dir, fails)

    expected_cols = {
        COL_OUT_CODE,
        COL_OUT_CATEGORY,
        COL_OUT_UNIT,
        COL_OUT_CO2,
        COL_OUT_OTHER,
        COL_OUT_TOTAL,
    }

    for fpath in sorted(saved):
        df = pd.read_csv(fpath)
        label = fpath.relative_to(output_dir)

        _check_columns(df, expected_cols, label, fails)
        if not expected_cols.issubset(df.columns):
            continue

        codes = set(df[COL_OUT_CODE].dropna().astype(str))

        _check_required_codes(codes, label, fails)
        _check_nl_codes(fpath, output_dir, nl_folder, codes, label, fails)
        _check_duplicates(df, label, fails)
        _check_sector1_co2(df, label, warns)
        _check_min_rows(df, label, warns)

    return fails, warns


# ── Private check functions ───────────────────────────────────────────────────


def _check_file_completeness(
    expected: set[tuple[str, int]],
    output_dir: Path,
    fails: list[str],
) -> None:
    """Check all expected files exist."""
    for fname, yr in sorted(expected):
        suffix = str(yr) if yr in {1990, 2000} else "default"
        pattern = f"intermediate_emissions_{suffix}.csv"
        found = list((output_dir / fname).rglob(f"15_emissions/{pattern}"))
        if not found:
            fails.append(f"MISSING FILE  {fname}/**/15_emissions/{pattern}")


def _check_columns(
    df: pd.DataFrame,
    expected_cols: set[str],
    label: Path,
    fails: list[str],
) -> None:
    """Check required columns present."""
    missing_cols = expected_cols - set(df.columns)
    if missing_cols:
        fails.append(f"MISSING COLS  {label}: {missing_cols}")


def _check_required_codes(
    codes: set[str],
    label: Path,
    fails: list[str],
) -> None:
    """Check required top-level CRT codes present."""
    missing_req = REQUIRED_CODES - codes
    if missing_req:
        fails.append(f"MISSING CODES {label}: {sorted(missing_req)}")


def _check_nl_codes(
    fpath: Path,
    output_dir: Path,
    nl_folder: str,
    codes: set[str],
    label: Path,
    fails: list[str],
) -> None:
    """Check NL off-road codes present for NL datasets."""
    if fpath.relative_to(output_dir).parts[0] == nl_folder:
        missing_nl = set(MOBILE_MACHINERY_CRT_CODES) - codes
        if missing_nl:
            fails.append(f"MISSING NL CODES {label}: {sorted(missing_nl)}")


def _check_duplicates(
    df: pd.DataFrame,
    label: Path,
    fails: list[str],
) -> None:
    """Check no duplicate CRT codes."""
    dupes = df[COL_OUT_CODE][df[COL_OUT_CODE].duplicated()].dropna().tolist()
    if dupes:
        fails.append(f"DUPLICATE CODES {label}: {dupes}")


def _check_sector1_co2(
    df: pd.DataFrame,
    label: Path,
    warns: list[str],
) -> None:
    """Soft check: Sector-1 CO2 should not be null."""
    row1 = df[df[COL_OUT_CODE].astype(str) == "1"]
    if row1.empty or pd.isna(row1.iloc[0][COL_OUT_CO2]):
        warns.append(f"NULL sector-1 CO2  {label}")


def _check_min_rows(
    df: pd.DataFrame,
    label: Path,
    warns: list[str],
) -> None:
    """Soft check: File should have minimum row count."""
    if len(df) < VALIDATION_MIN_ROWS:
        warns.append(f"FEW ROWS ({len(df)})  {label}")
