"""
Data processors for emissions transformations.

Provides processors for:
- data_fixer: Dataset-specific fixes (NL mobile machinery, residuals)
- etm_mapper: CRT→ETM mapping, LULUCF splitting, GHG filtering
"""

from .data_fixer import reallocate_nl_mobile_machinery, set_child_residual, ensure_row
from .etm_mapper import ETMMapper

__all__ = [
    "reallocate_nl_mobile_machinery",
    "set_child_residual",
    "ensure_row",
    "ETMMapper",
]
