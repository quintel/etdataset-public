"""
Northern Ireland (UKNI) data source.

Processes UK Devolved Administration GHGI (DA_GHGI) format data for
Northern Ireland region.
"""

from __future__ import annotations
from typing import Iterator
import pandas as pd
import re

from .base import DataSource


class UKNISource(DataSource):
    """Process Northern Ireland DA_GHGI data."""

    def fetch(
        self,
        dataset: str,
        years: list[int],
        ukni_df: pd.DataFrame,
    ) -> Iterator[dict]:
        """
        Process UKNI data and yield emission records.

        Args:
            dataset: Dataset identifier
            years: Years to fetch
            ukni_df: Pre-loaded UKNI DataFrame (from Excel parsing)

        Yields:
            Standard emission records
        """
        processed_df = self._process_ukni_data(ukni_df, years)

        for _, row in processed_df.iterrows():
            yield self._standardize_row(
                code=row["category_code"],
                category=row["category"],
                year=row["year"],
                co2=row["co2"],
                other_ghg=row["other_ghg_co2eq"],
            )

    def _process_ukni_data(
        self,
        ukni_df: pd.DataFrame,
        years: list[int],
    ) -> pd.DataFrame:
        """
        Convert DA_GHGI format to standard CRT format.

        UKNI format:
        - CRT_Category: codes like "1A1aiii", "1A4ci"
        - Pollutant: "CO2", "CH4", "N2O"
        - Emission: numeric value
        - ConvertTo: "GWP CO2_AR5"
        - EmissionYear: year
        """
        df = ukni_df.copy()
        df = df[df["EmissionYear"].isin(years)]

        df["category_code"] = df["CRT_Category"].apply(self._normalize_crt)
        df = df[df["category_code"].notna()]

        co2_df = self._aggregate_co2(df)
        other_df = self._aggregate_other_ghg(df)

        result = co2_df.merge(other_df, on=["category_code", "year"], how="outer")
        result = self._add_category_names(result, ukni_df)

        return result[["category_code", "category", "year", "co2", "other_ghg_co2eq"]]

    def _aggregate_co2(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Aggregate CO2 emissions."""
        co2_mask = (df["Pollutant"] == "CO2") & (df["ConvertTo"] == "GWP CO2_AR5")
        return (
            df[co2_mask]
            .groupby(["category_code", "EmissionYear"], as_index=False)["Emission"]
            .sum()
            .rename(columns={"Emission": "co2", "EmissionYear": "year"})
        )

    def _aggregate_other_ghg(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Aggregate other GHG emissions (already in CO2eq via AR5)."""
        other_mask = df["Pollutant"].isin(["CH4", "N2O", "HFCs", "NF3", "PFCs", "SF6"]) & (
            df["ConvertTo"] == "GWP CO2_AR5"
        )
        return (
            df[other_mask]
            .groupby(["category_code", "EmissionYear"], as_index=False)["Emission"]
            .sum()
            .rename(columns={"Emission": "other_ghg_co2eq", "EmissionYear": "year"})
        )

    def _add_category_names(
        self,
        result: pd.DataFrame,
        ukni_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Add category names from original data."""
        category_map = (
            ukni_df[["CRT_Category", "CRT_Category_Description"]]
            .dropna()
            .drop_duplicates("CRT_Category")
            .set_index("CRT_Category")["CRT_Category_Description"]
            .to_dict()
        )

        def get_category_name(category_code):
            for orig_code, desc in category_map.items():
                if self._normalize_crt(orig_code) == category_code:
                    return desc
            return ""

        result["category"] = result["category_code"].apply(get_category_name)
        return result

    @staticmethod
    def _normalize_crt(code) -> str | None:
        """
        Normalize UKNI CRT codes to standard format.

        Handles formats:
        - Standard: 1A4ci -> 1.A.4.c.i
        - Single letter: 3H -> 3.H
        - Simple numeric: 2A1 -> 2.A.1
        - With parentheses: 4A(II) -> 4.A(II)
        - Complex: 5C1aii4 -> 5.C.1.a.ii.4
        """
        code = str(code).strip()

        # Pattern 1: Single letter suffix (e.g., 3H, 4A)
        match = re.match(r"^(\d+)([A-Z])$", code)
        if match:
            return f"{match.group(1)}.{match.group(2)}"

        # Pattern 2: Codes with parentheses (e.g., 4A(II), 4B1(IV)b)
        if "(" in code:
            match = re.match(r"^(\d+)([A-Z])(\d*)([a-z]*)(\([^)]+\))([a-z]*)$", code)
            if match:
                major, letter, num, lower1, paren, lower2 = match.groups()
                parts = [major, letter]
                if num:
                    parts.append(num)
                if lower1:
                    parts.append(lower1)
                result = ".".join(parts) + paren
                if lower2:
                    result += "." + lower2
                return result

            # Fallback for parentheses
            match = re.match(r"^(\d+)([A-Z].*)$", code)
            if match:
                return f"{match.group(1)}.{match.group(2)}"

        # Pattern 3: Simple numeric (e.g., 2A1, 3A2)
        match = re.match(r"^(\d+)([A-Z])(\d+)$", code)
        if match:
            return f"{match.group(1)}.{match.group(2)}.{match.group(3)}"

        # Pattern 4: Complex codes with roman numerals
        match = re.match(r"^(\d+)([A-Z])(\d+)([a-z]+?)(i{1,3}|iv|v|vi{1,3}|ix|x)?(\d*)$", code)
        if match:
            major, letter, number, subsection, roman, trailing = match.groups()

            # Check if roman numeral is embedded in subsection
            if not roman and subsection:
                roman_match = re.match(r"^([a-z]+?)(i{1,3}|iv|v|vi{1,3}|ix|x)$", subsection)
                if roman_match:
                    subsection, roman = roman_match.groups()

            parts = [major, letter, number, subsection]
            if roman:
                parts.append(roman)
            if trailing:
                parts.append(trailing)

            return ".".join(parts)

        # No match - return None
        return None
