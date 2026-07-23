"""
Emissions processing library.

A modular, generator-based pipeline for processing greenhouse gas emissions data
from multiple international sources into ETM-compatible datasets.

Main components:
- config: Configuration and constants
- sources: Data source fetchers (UNFCCC API, Excel, UKNI)
- processors: Data transformers (CRT normalization, fixes, ETM mapping)
- validators: Data quality checks (structural and plausibility)
- writers: Output file generators

Example usage:
    from tools.emissions.lib import config, sources, writers

    datasets = config.load_datasets(config_path)
    source = sources.UFCCCAPISource(reader)
    writer = writers.IntermediateWriter(output_dir)

    for row in source.fetch(dataset, years):
        writer.write(row)
"""

__version__ = "2.0.0"

# Re-export main public API
from .config import (
    load_datasets,
    MAX_CATEGORY_DEPTH,
    GWP_AR5_CH4,
    GWP_AR5_N2O,
    COL_OUT_CODE,
    COL_OUT_CATEGORY,
    COL_OUT_UNIT,
    COL_OUT_CO2,
    COL_OUT_OTHER,
    COL_OUT_TOTAL,
)

# Submodules available for import
from . import sources
from . import processors
from . import validators
from . import writers

__all__ = [
    "load_datasets",
    "MAX_CATEGORY_DEPTH",
    "GWP_AR5_CH4",
    "GWP_AR5_N2O",
    "COL_OUT_CODE",
    "COL_OUT_CATEGORY",
    "COL_OUT_UNIT",
    "COL_OUT_CO2",
    "COL_OUT_OTHER",
    "COL_OUT_TOTAL",
    "sources",
    "processors",
    "validators",
    "writers",
]
