"""
UNFCCC API data source.

Fetches emissions data from the UNFCCC Detailed Inventory API via unfccc_di_api.
"""

from __future__ import annotations
from typing import Iterator, Any
import pandas as pd

from .base import DataSource
from ..config import (
    MAX_CATEGORY_DEPTH,
    INTERNATIONAL_CRT_CODE_FIXES,
)


class UFCCCAPISource(DataSource):
    """Fetch emissions data from UNFCCC API."""

    def __init__(self, reader: Any):
        """
        Initialize with UNFCCC API reader.

        Args:
            reader: unfccc_di_api.ZenodoReader instance
        """
        self.reader = reader

    def fetch(
        self,
        dataset: str,
        years: list[int],
        party_code: str,
        max_depth: int = MAX_CATEGORY_DEPTH,
    ) -> Iterator[dict]:
        """
        Fetch UNFCCC API data for a country.

        Args:
            dataset: Dataset identifier (unused, for interface consistency)
            years: Years to fetch
            party_code: UNFCCC party code (e.g., 'NLD', 'DEU')
            max_depth: Maximum CRT code depth (default: 4)

        Yields:
            Standard emission records
        """
        raw_df = self._fetch_raw_data(party_code, years)
        processed_df = self._process_api_data(raw_df, party_code, max_depth)

        for _, row in processed_df.iterrows():
            yield self._standardize_row(
                code=row["category_code"],
                category=row["category"],
                year=row["year"],
                co2=row["co2"],
                other_ghg=row["other_ghg_co2eq"],
            )

    def _fetch_raw_data(
        self,
        party_code: str,
        years: list[int],
    ) -> pd.DataFrame:
        """Fetch raw data from API."""
        raw = self.reader.query(party_code=party_code)
        years_str = [str(y) for y in years]
        data = raw[raw["year"].isin(years_str)].copy()
        data["year"] = data["year"].astype(int)
        return data

    def _process_api_data(
        self,
        df: pd.DataFrame,
        party_code: str,
        max_depth: int,
    ) -> pd.DataFrame:
        """Process API data to standard format."""
        data = df.copy()
        data["numberValue"] = pd.to_numeric(data["numberValue"], errors="coerce")

        data = self._filter_api_data(data)

        if data.empty:
            print(f"  Warning: no 'Net emissions/removals' data for {party_code}")
            return pd.DataFrame(
                columns=["category_code", "category", "year", "co2", "other_ghg_co2eq"]
            )

        data = self._extract_codes(data)
        data = self._fix_bunker_codes(data)
        data = self._filter_by_depth(data, max_depth)

        pivot = self._pivot_by_gas(data)
        pivot = self._calculate_other_ghg(pivot)
        pivot = self._add_indirect_co2(pivot, df, party_code)

        return pivot[["category_code", "category", "year", "co2", "other_ghg_co2eq"]]

    def _filter_api_data(
        self,
        data: pd.DataFrame,
    ) -> pd.DataFrame:
        """Filter to relevant gas and measure types."""
        data = data[data["gas"].isin(["CO2", "Aggregate GHGs"])]
        data = data[data["measure"] == "Net emissions/removals"]
        data = data[data["classification"] == "Total for category"]
        return data

    def _extract_codes(
        self,
        data: pd.DataFrame,
    ) -> pd.DataFrame:
        """Extract CRT code and category name."""
        parsed = data["category"].str.extract(r"^(\S+)\s*-?\s*(.*)")

        potential_code = parsed[0].str.rstrip(".")
        potential_name = parsed[1].str.strip()

        has_numeric_prefix = potential_code.str.match(r"^[0-9]", na=False)

        data["category_code"] = potential_code.where(has_numeric_prefix, "")
        data["category"] = potential_name.where(has_numeric_prefix, data["category"])

        return data

    def _fix_bunker_codes(
        self,
        data: pd.DataFrame,
    ) -> pd.DataFrame:
        """Fix international bunker CRT codes."""
        bunker_mask = data["category"].isin(INTERNATIONAL_CRT_CODE_FIXES.keys())

        if bunker_mask.any():
            data.loc[bunker_mask, "category_code"] = data.loc[
                bunker_mask, "category"
            ].map(INTERNATIONAL_CRT_CODE_FIXES)

        return data

    def _filter_by_depth(
        self,
        data: pd.DataFrame,
        max_depth: int,
    ) -> pd.DataFrame:
        """Filter categories by maximum depth."""
        return data[data["category_code"].fillna("").str.count(r"\.") <= max_depth]

    def _pivot_by_gas(
        self,
        data: pd.DataFrame,
    ) -> pd.DataFrame:
        """Pivot to separate CO2 and Aggregate GHG columns."""
        pivot = data.pivot_table(
            index=["category_code", "category", "year"],
            columns="gas",
            values="numberValue",
            aggfunc="sum",
        ).reset_index()

        pivot.columns.name = None

        if "CO2" not in pivot.columns:
            pivot["CO2"] = pd.NA
        if "Aggregate GHGs" not in pivot.columns:
            pivot["Aggregate GHGs"] = pd.NA

        return pivot

    def _calculate_other_ghg(
        self,
        pivot: pd.DataFrame,
    ) -> pd.DataFrame:
        """Calculate other_ghg as Aggregate GHGs - CO2."""
        co2 = pivot["CO2"].fillna(0)
        agg = pivot["Aggregate GHGs"].fillna(0)

        pivot["co2"] = co2
        pivot["other_ghg_co2eq"] = agg - co2

        both_missing = pivot["CO2"].isna() & pivot["Aggregate GHGs"].isna()
        pivot.loc[both_missing, "co2"] = pd.NA
        pivot.loc[both_missing, "other_ghg_co2eq"] = pd.NA

        return pivot

    def _add_indirect_co2(
        self,
        pivot: pd.DataFrame,
        df: pd.DataFrame,
        party_code: str,
    ) -> pd.DataFrame:
        """Add indirect CO2 emissions rows."""
        indirect_co2 = df[
            (df["category"] == "Total GHG emissions with LULUCF")
            & (df["measure"] == "Indirect emissions")
            & (df["gas"] == "CO2")
        ][["year", "numberValue"]].copy()

        indirect_co2["numberValue"] = pd.to_numeric(
            indirect_co2["numberValue"], errors="coerce"
        )

        if indirect_co2.empty:
            print(f"  Warning: no indirect CO2 data found for {party_code}")
        else:
            indirect_rows = pd.DataFrame(
                {
                    "category_code": "ind_CO2",
                    "category": "Indirect CO2",
                    "year": indirect_co2["year"],
                    "co2": indirect_co2["numberValue"].fillna(0),
                    "other_ghg_co2eq": 0,
                }
            )
            pivot = pd.concat([pivot, indirect_rows], ignore_index=True)

        return pivot
