"""
Final emissions CSV writer.

Writes final emissions.csv files in ETM format with year column (long format).
"""

from __future__ import annotations
from pathlib import Path
import pandas as pd

from ..config import folder_name


class FinalWriter:
    """Write final emissions.csv files in ETM format."""

    def __init__(self, output_dir: Path):
        """
        Initialize writer.

        Args:
            output_dir: Base output directory (data/)
        """
        self.output_dir = output_dir

    def write_long_format(
        self,
        dataset: str,
        analysis_year: int,
        year_data: dict[int, pd.DataFrame],
    ) -> Path:
        """
        Write emissions.csv in long format with year column.

        Args:
            dataset: Dataset identifier
            analysis_year: Analysis year for folder structure
            year_data: Dict mapping year to long-format DataFrame
                       DataFrame columns: etm_sector, etm_subsector, use, ghg, unit, value

        Returns:
            Path to written file
        """
        folder = folder_name(dataset)
        output_path = (
            self.output_dir
            / folder
            / str(analysis_year)
            / "15_emissions"
            / "emissions.csv"
        )

        output_path.parent.mkdir(parents=True, exist_ok=True)

        long_df = self._stack_years_to_long(year_data)
        long_df.to_csv(output_path, index=False)

        return output_path

    @staticmethod
    def _stack_years_to_long(year_data: dict[int, pd.DataFrame]) -> pd.DataFrame:
        """
        Stack multiple years into long format with year column.

        Args:
            year_data: Dict mapping year to long-format DataFrame

        Returns:
            Long-format DataFrame with year column, values rounded to 5 decimals
        """
        if not year_data:
            raise ValueError("No year data provided")

        frames = []
        for year, df in sorted(year_data.items()):
            df_copy = df.copy()
            df_copy["year"] = year
            frames.append(df_copy)

        result = pd.concat(frames, ignore_index=True)

        # Round value column to 5 decimal places
        result["value"] = result["value"].round(5)
        # Normalize -0.0 to 0.0
        result["value"] = result["value"].apply(lambda x: 0.0 if x == 0.0 else x)

        # Column order: etm_sector, etm_subsector, use, ghg, year, unit, value
        result = result[
            ["etm_sector", "etm_subsector", "use", "ghg", "year", "unit", "value"]
        ]

        # Sort by keys and year
        result = result.sort_values(
            ["etm_sector", "etm_subsector", "use", "ghg", "year"]
        )

        return result


def calculate_gb_long_format(
    uk_path: Path,
    ukni_path: Path,
    output_path: Path,
) -> dict:
    """
    Calculate GB emissions by subtracting UKNI from UK (long format).

    Special handling for LULUCF CO2:
    - Reconstructs pre-split values per year
    - Performs subtraction
    - Re-splits result

    Args:
        uk_path: Path to UK emissions.csv
        ukni_path: Path to UKNI emissions.csv
        output_path: Path for GB emissions.csv

    Returns:
        Dict with validation statistics: "per_year" (mapping each year to its
        uk_total/ukni_total/gb_total/gb_uk_ratio), plus overall "negative_count"
        and "negative_rows" (tuples of
        (etm_sector, etm_subsector, use, ghg, year, value)).
    """
    uk_df = pd.read_csv(uk_path)
    ukni_df = pd.read_csv(ukni_path)

    # UKNI's analysis year (e.g. 2018) differs from UK's (e.g. 2019); align it so
    # the per-year subtraction below matches UKNI's analysis year against UK's.
    ukni_df = _align_ukni_years(uk_df, ukni_df)

    # Process each year separately
    years = sorted(uk_df["year"].unique())
    gb_frames = []

    for year in years:
        uk_year = uk_df[uk_df["year"] == year].copy()
        ukni_year = ukni_df[ukni_df["year"] == year].copy()

        # LULUCF special handling
        uk_lulucf_co2 = _reconstruct_lulucf_co2_long(uk_year)
        ukni_lulucf_co2 = _reconstruct_lulucf_co2_long(ukni_year)
        gb_lulucf_co2 = uk_lulucf_co2 - ukni_lulucf_co2

        if gb_lulucf_co2 < 0:
            gb_lulucf_removals = abs(gb_lulucf_co2)
            gb_lulucf_emissions = 0.0
        else:
            gb_lulucf_removals = 0.0
            gb_lulucf_emissions = gb_lulucf_co2

        # Subtract emissions
        gb_year = _subtract_emissions_long(uk_year, ukni_year)
        gb_year = _apply_lulucf_split_long(
            gb_year, gb_lulucf_removals, gb_lulucf_emissions
        )

        gb_frames.append(gb_year)

    gb_df = pd.concat(gb_frames, ignore_index=True)

    # Round values to 5 decimal places
    gb_df["value"] = gb_df["value"].round(5)

    # Sort
    gb_df = gb_df.sort_values(["etm_sector", "etm_subsector", "use", "ghg", "year"])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    gb_df.to_csv(output_path, index=False)

    return _calculate_validation_stats_long(uk_df, ukni_df, gb_df)


# ── Private helpers ───────────────────────────────────────────────────────────


def _align_ukni_years(uk_df: pd.DataFrame, ukni_df: pd.DataFrame) -> pd.DataFrame:
    """
    Remap UKNI's analysis year onto UK's analysis year.

    Maps UKNI's 2018 start year to UK's 2019 start year; returns the
    frame unchanged if either side does not have exactly one analysis year or
    the years already match.

    Returns a modified copy of ukni_df; the original is not mutated.
    """
    uk_analysis = sorted(y for y in uk_df["year"].unique() if y != 1990)
    ukni_analysis = sorted(y for y in ukni_df["year"].unique() if y != 1990)

    if len(uk_analysis) != 1 or len(ukni_analysis) != 1:
        return ukni_df
    if uk_analysis[0] == ukni_analysis[0]:
        return ukni_df

    ukni_df = ukni_df.copy()
    ukni_df["year"] = ukni_df["year"].replace({ukni_analysis[0]: uk_analysis[0]})
    return ukni_df


def _reconstruct_lulucf_co2_long(df: pd.DataFrame) -> float:
    """Reconstruct original signed LULUCF CO2 from split subsectors (long format)."""
    lulucf_co2 = df[(df["etm_sector"] == "LULUCF") & (df["ghg"] == "co2")]

    if lulucf_co2.empty:
        return 0.0

    removals = lulucf_co2[lulucf_co2["etm_subsector"] == "Removals"]["value"]
    emissions = lulucf_co2[lulucf_co2["etm_subsector"] == "Emissions"]["value"]

    removals_val = removals.iloc[0] if not removals.empty else 0.0
    emissions_val = emissions.iloc[0] if not emissions.empty else 0.0

    return emissions_val - removals_val


def _subtract_emissions_long(
    uk_df: pd.DataFrame,
    ukni_df: pd.DataFrame,
) -> pd.DataFrame:
    """Subtract UKNI from UK for all categories (long format)."""
    gb_df = uk_df.merge(
        ukni_df,
        on=["etm_sector", "etm_subsector", "use", "ghg", "unit", "year"],
        how="left",
        suffixes=("_uk", "_ukni"),
    )

    gb_df["value"] = gb_df["value_uk"] - gb_df["value_ukni"].fillna(0)

    key_cols = ["etm_sector", "etm_subsector", "use", "ghg", "year", "unit"]
    gb_df = gb_df[key_cols + ["value"]]

    return gb_df


def _apply_lulucf_split_long(
    df: pd.DataFrame,
    removals_val: float,
    emissions_val: float,
) -> pd.DataFrame:
    """Apply GB LULUCF split values (long format)."""
    lulucf_removals_mask = (
        (df["etm_sector"] == "LULUCF")
        & (df["etm_subsector"] == "Removals")
        & (df["ghg"] == "co2")
    )
    lulucf_emissions_mask = (
        (df["etm_sector"] == "LULUCF")
        & (df["etm_subsector"] == "Emissions")
        & (df["ghg"] == "co2")
    )

    df.loc[lulucf_removals_mask, "value"] = removals_val
    df.loc[lulucf_emissions_mask, "value"] = emissions_val

    return df


def _calculate_validation_stats_long(
    uk_df: pd.DataFrame,
    ukni_df: pd.DataFrame,
    gb_df: pd.DataFrame,
) -> dict:
    """Calculate validation statistics per year (long format)."""
    years = sorted(uk_df["year"].unique())
    if not years:
        return {}

    # Stats per year so both the 1990 base year and the analysis year are shown
    per_year: dict[int, dict] = {}
    for year in years:
        uk_total = uk_df[uk_df["year"] == year]["value"].sum()
        ukni_total = ukni_df[ukni_df["year"] == year]["value"].sum()
        gb_total = gb_df[gb_df["year"] == year]["value"].sum()

        per_year[int(year)] = {
            "uk_total": uk_total,
            "ukni_total": ukni_total,
            "gb_total": gb_total,
            "gb_uk_ratio": gb_total / uk_total if uk_total != 0 else 0,
        }

    negative_mask = gb_df["value"] < -0.01
    negative_count = negative_mask.sum()
    negative_rows = []

    if negative_count > 0:
        for _, row in gb_df[negative_mask].iterrows():
            negative_rows.append(
                (
                    row["etm_sector"],
                    row["etm_subsector"],
                    row["use"],
                    row["ghg"],
                    row["year"],
                    row["value"],
                )
            )

    return {
        "per_year": per_year,
        "negative_count": negative_count,
        "negative_rows": negative_rows,
    }
