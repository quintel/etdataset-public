"""
Intermediate CSV writer.

Writes intermediate emissions data with CRT codes, used between fetching
and ETM mapping stages.
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
    folder_name,
)


class IntermediateWriter:
    """Write intermediate emissions CSV files."""

    def __init__(self, output_dir: Path):
        """
        Initialize writer.

        Args:
            output_dir: Base output directory (data/)
        """
        self.output_dir = output_dir

    def write_batch(
        self,
        rows: list[dict],
        dataset: str,
        analysis_year: int,
        data_year: int,
    ) -> Path:
        """
        Write batch of emission records to intermediate CSV.

        Args:
            rows: List of emission records (with metadata columns)
            dataset: Dataset identifier
            analysis_year: Analysis year for folder structure
            data_year: Data year (determines file suffix)

        Returns:
            Path to written file
        """
        if not rows:
            raise ValueError(f"No rows to write for {dataset} {data_year}")

        df = pd.DataFrame(rows)
        return self.write_dataframe(df, dataset, analysis_year, data_year)

    def write_dataframe(
        self,
        df: pd.DataFrame,
        dataset: str,
        analysis_year: int,
        data_year: int,
    ) -> Path:
        """
        Write DataFrame to intermediate CSV.

        Args:
            df: Emissions DataFrame with columns:
                dataset, country_name, analysis_year, data_year,
                category_code, category, co2, other_ghg_co2eq
            dataset: Dataset identifier
            analysis_year: Analysis year for folder structure
            data_year: Data year (determines file suffix)

        Returns:
            Path to written file
        """
        folder = folder_name(dataset)
        suffix = str(data_year) if data_year == 1990 else "default"
        output_path = (
            self.output_dir
            / folder
            / str(analysis_year)
            / "15_emissions"
            / f"intermediate_emissions_{suffix}.csv"
        )

        output_path.parent.mkdir(parents=True, exist_ok=True)

        prepared_df = self._prepare_output(df)
        prepared_df.to_csv(output_path, index=False)

        return output_path

    @staticmethod
    def _prepare_output(df: pd.DataFrame) -> pd.DataFrame:
        """Prepare DataFrame for output (select and rename columns)."""
        prepared = df.copy()

        prepared = prepared.rename(
            columns={
                "category_code": COL_OUT_CODE,
                "category": COL_OUT_CATEGORY,
                "co2": COL_OUT_CO2,
                "other_ghg_co2eq": COL_OUT_OTHER,
            }
        )

        prepared[COL_OUT_UNIT] = "kton CO2-eq"

        if COL_OUT_CO2 in prepared.columns and COL_OUT_OTHER in prepared.columns:
            co2 = prepared[COL_OUT_CO2].fillna(0)
            other = prepared[COL_OUT_OTHER].fillna(0)
            both_missing = prepared[COL_OUT_CO2].isna() & prepared[COL_OUT_OTHER].isna()
            prepared[COL_OUT_TOTAL] = co2 + other
            prepared.loc[both_missing, COL_OUT_TOTAL] = float("nan")

        output_cols = [
            COL_OUT_CODE,
            COL_OUT_CATEGORY,
            COL_OUT_CO2,
            COL_OUT_OTHER,
            COL_OUT_TOTAL,
            COL_OUT_UNIT,
        ]

        return prepared[output_cols]
