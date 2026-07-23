"""
Configuration and constants for emissions processing pipeline.

Centralizes dataset loading, routing, and all pipeline constants.
"""

from __future__ import annotations
from pathlib import Path
import pandas as pd
import re

# ── GWP Constants ─────────────────────────────────────────────────────────────
# IPCC AR5 GWP100 values
GWP_AR5_CH4 = 28
GWP_AR5_N2O = 265

# Conversion factor for Gg to kg
GG_TO_KG = 10**6

# ── Category Depth Filter ─────────────────────────────────────────────────────
# Keep sectors up to and including the 4-dot level (e.g. 1.A.2.g.vii).
# Anything deeper (e.g. 1.B.1.a.i.1 = 5 dots) is dropped.
MAX_CATEGORY_DEPTH = 4

# ── Output Column Names ───────────────────────────────────────────────────────
COL_OUT_CODE = "crt_code"
COL_OUT_CATEGORY = "crt_category"
COL_OUT_UNIT = "unit"
COL_OUT_CO2 = "co2"
COL_OUT_OTHER = "other_ghg"
COL_OUT_TOTAL = "total_ghg"

# ── Verification / Validation Constants ───────────────────────────────────────
REQUIRED_CODES = {
    "1",
    "2",
    "3",
    "4",
    "5",
}  # top-level CRT sectors every file must contain

# ── Mobile Machinery Reallocation ─────────────────────────────────────────────
# NL mobile machinery reallocation codes
# Maps each CRT source code to the ancestor codes
MOBILE_MACHINERY_CRT_CODES = {
    "1.A.2.g.vii": [
        "1.A.2.g",
        "1.A.2",
    ],  # Manufacturing industries — Off-road vehicles and other machinery
    "1.A.4.a.ii": [
        "1.A.4.a",
        "1.A.4",
    ],  # Commercial/institutional — Off-road vehicles and other machinery
    "1.A.4.b.ii": [
        "1.A.4.b",
        "1.A.4",
    ],  # Residential — Off-road vehicles and other machinery
    "1.A.4.c.ii": [
        "1.A.4.c",
        "1.A.4",
    ],  # Agriculture — Off-road vehicles and other machinery
    "1.A.5.b": ["1.A.5"],  # Other — Mobile
}

# CRT codes where mobile machinery should be reallocated to
MOBILE_MACHINERY_REALLOCATION_CODE = "1.A.3.b"
MOBILE_MACHINERY_CHILD_CODE = "1.A.3.b.iii"

# CRT code fishing
FISHING_CRT_CODE = "1.A.4.c.iii"

# ── Validation Constants ──────────────────────────────────────────────────────
# Minimum rows expected per output file
VALIDATION_MIN_ROWS = 10

# Sectors excluded from the negative-value check (LULUCF and Waste)
EXCLUDED_NEGATIVE_SECTORS = ("4", "5")

# Floating-point arithmetic can produce -0.0 values that are semantically zero.
# Threshold used so these are not flagged; values above this threshold are treated as zero/non-negative.
NEGATIVE_THRESHOLD = -0.01  # Gg CO2

# Sub-sector mismatch tolerance;
# Used for validation of sub-sectors sums vs parent sector totals.
SUBSECTOR_MISMATCH_TOLERANCE = 0.001

# Flag if analysis year / 1990 for CRT 1 CO2 ratio exceeds this value
MAX_YEAR_RATIO = 3.0

# ── Regex Patterns ────────────────────────────────────────────────────────────
# Pattern for standard CRT category codes (start with sector digit 1–5)
CRT_CODE_RE = re.compile(r"^[1-5]")

# ── International Bunker Fixes ────────────────────────────────────────────────
# CRT codes for international bunker categories (UNFCCC API returns these without prefixes)
INTERNATIONAL_CRT_CODE_FIXES = {
    "International Bunkers": "1.D.1",
    "International Aviation": "1.D.1.a",
    "International Navigation": "1.D.1.b",
}


# ── Dataset Loading ───────────────────────────────────────────────────────────


def load_datasets(config_path: Path) -> pd.DataFrame:
    """
    Load dataset configuration CSV.

    Args:
        config_path: Path to config_country_datasets.csv

    Returns:
        DataFrame with columns: dataset, name, analysis_year, unfccc_code
    """
    df = pd.read_csv(config_path)
    df.columns = df.columns.str.strip()
    df["analysis_year"] = df["analysis_year"].astype(int)
    return df


def folder_name(dataset: str) -> str:
    """Return the data folder for a dataset (NL variants share the 'nl' folder)."""
    return "nl" if dataset.startswith("nl") else dataset
