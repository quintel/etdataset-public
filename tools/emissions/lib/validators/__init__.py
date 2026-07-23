"""
Data validators for emissions quality checks.

Provides validators for:
- structural: Hard requirements (files, columns, codes, duplicates)
- plausibility: Value plausibility (non-negative, sums, ratios)
"""

from .structural import verify_outputs
from .plausibility import (
    validate_outputs,
    validate_1990_unfccc_totals,
    validate_excel_final_emissions,
)

__all__ = [
    "verify_outputs",
    "validate_outputs",
    "validate_1990_unfccc_totals",
    "validate_excel_final_emissions",
]
