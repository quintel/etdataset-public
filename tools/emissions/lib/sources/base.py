"""
Base class for emissions data sources.

Defines common interface for fetching and processing emissions data from
different sources (UNFCCC API, Excel files, regional datasets).
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Iterator
import pandas as pd


class DataSource(ABC):
    """
    Abstract base class for emissions data sources.

    Subclasses must implement fetch() to yield processed emission records
    in standard format.
    """

    @abstractmethod
    def fetch(
        self,
        dataset: str,
        years: list[int],
        **kwargs,
    ) -> Iterator[dict]:
        """
        Fetch and process emissions data for a dataset.

        Args:
            dataset: Dataset identifier (e.g., 'nl2020', 'de2021')
            years: List of years to fetch (e.g., [1990, 2020])
            **kwargs: Source-specific parameters

        Yields:
            Dict with keys: category_code, category, year, co2, other_ghg_co2eq
        """
        pass

    def _standardize_row(
        self,
        code: str,
        category: str,
        year: int,
        co2: float,
        other_ghg: float,
    ) -> dict:
        """
        Create standard row format.

        Args:
            code: CRT category code (e.g., '1.A.1.a')
            category: Category label
            year: Year
            co2: CO2 emissions in Gg
            other_ghg: Other GHG emissions in Gg CO2eq

        Returns:
            Standardized dict
        """
        return {
            "category_code": code,
            "category": category,
            "year": year,
            "co2": co2,
            "other_ghg_co2eq": other_ghg,
        }
