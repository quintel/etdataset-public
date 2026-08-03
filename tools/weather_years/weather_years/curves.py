"""The generator's output: named hourly profiles, and reading them back."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from .constants import SECONDS_PER_HOUR


@dataclass(frozen=True)
class Curve:
    """An hourly profile normalised so its values sum to 1/3600."""

    key: str
    values: np.ndarray

    def write_csv(self, directory: Path) -> Path:
        """Write `<key>.csv`, always overwriting."""
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / f"{self.key}.csv"
        pd.Series(self.values).to_csv(path, index=False, header=False)

        return path

    @classmethod
    def read_csv(cls, path: Path) -> Curve:
        values = pd.read_csv(path, header=None)[0].to_numpy(dtype=float)

        return cls(key=path.stem, values=values)


def normalize(curve: np.ndarray) -> np.ndarray:
    """Scale a curve so it sums to 1/3600, ETM's hourly profile convention."""
    total = np.sum(curve)
    if total == 0:
        raise ValueError("Cannot normalize a curve with zero total demand.")

    return curve / total / SECONDS_PER_HOUR


def write_curves(curves: list[Curve], directory: Path) -> list[Path]:
    return [curve.write_csv(directory) for curve in curves]
