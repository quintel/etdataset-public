"""
Data writers for emissions output files.

Provides writers for:
- intermediate: Intermediate CSV files with CRT codes
- final: Final emissions.csv files in ETM format (long format with year column)
"""

from .intermediate import IntermediateWriter
from .final import FinalWriter, calculate_gb_long_format

__all__ = [
    "IntermediateWriter",
    "FinalWriter",
    "calculate_gb_long_format",
]
