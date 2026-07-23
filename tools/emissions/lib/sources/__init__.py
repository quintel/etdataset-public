"""
Data sources for emissions processing.

Provides fetcher classes for different data sources:
- UFCCCAPISource: UNFCCC Detailed Inventory API
- UFCCCExcelSource: UNFCCC CRT Excel submissions
- UKNISource: Northern Ireland DA_GHGI data
"""

from .base import DataSource
from .unfccc_api import UFCCCAPISource
from .unfccc_excel import UFCCCExcelSource
from .ukni import UKNISource

__all__ = [
    "DataSource",
    "UFCCCAPISource",
    "UFCCCExcelSource",
    "UKNISource",
]
