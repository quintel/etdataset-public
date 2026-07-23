"""
Data models for emissions validation.

Provides type-safe data structures for validation results and intermediate data.
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class DatasetInfo:
    """Information about a dataset extracted from file path."""

    dataset: str  # Dataset folder name (e.g., "nl", "FI_finland")
    year: int  # Analysis year
    dataset_for_unfccc: str  # Dataset name for UNFCCC filename (handles NL mapping)


@dataclass
class EmissionTotals:
    """Emission totals for CO2, other GHG, and total GHG."""

    co2: float  # CO2 emissions in kton CO2-eq
    other_ghg: float  # Other GHG emissions in kton CO2-eq
    total_ghg: float  # Total GHG emissions in kton CO2-eq


@dataclass
class ValidationResult:
    """Result of comparing calculated vs reported emissions."""

    dataset: str  # Dataset name
    calculated: EmissionTotals  # Calculated totals from emissions.csv
    reported: EmissionTotals  # Reported totals from UNFCCC API
    relative_diffs: dict[str, float | None]  # Relative differences by gas type
    passed: bool  # Whether validation passed threshold
    warnings: list[str]  # Warning messages if validation failed


@dataclass
class ExcelSheetTotals:
    """Emission totals extracted from Excel Summary2 sheet."""

    co2: float  # CO2 emissions in kton CO2-eq
    other_ghg: float  # Other GHG emissions in kton CO2-eq
    total_ghg: float  # Total GHG emissions in kton CO2-eq
    sheet_name: str  # Name of sheet totals were extracted from


@dataclass
class ExcelValidationResult:
    """Result of Excel source internal consistency validation."""

    dataset: str  # Dataset name
    year: int  # Analysis year
    summary_totals: ExcelSheetTotals | None  # Totals from Summary2 sheet
    detailed_totals: EmissionTotals  # Totals from detailed sheets (emissions.csv)
    relative_diffs: dict[str, float | None]  # Relative differences by gas type
    passed: bool  # Whether validation passed threshold
    warnings: list[str]  # Warning messages if validation failed
    missing_summary: bool  # True if Summary2 sheet was not found/parsed
