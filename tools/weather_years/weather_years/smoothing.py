"""Turn a single-household curve into a neighbourhood curve.

A neighbourhood of 300 households does not switch its heating on at the same
minute. The single-house curve is interpolated to 6-minute resolution, copied
300 times with each copy shifted by a normally distributed offset, summed, and
resampled back to hourly values. Background:
https://refman.energytransitionmodel.com/publications/2118

Two sources of randomness are available and they are not interchangeable:

- `SharedRandomState` draws every profile from one stream in generation order.
  This is what produced every weather year ETM currently ships, so it is the
  default and it is frozen: reordering profiles, adding a house type or
  regenerating one profile alone all move the numbers. That order-dependence is
  a defect, and reproducing the shipped curves requires keeping it.
- `PerProfileRandomState` seeds a stream per profile key, so a profile is
  identical whether generated alone or in a set. Switching the default to it
  changes every curve, so it is not switched silently.
"""

from __future__ import annotations

import hashlib
from typing import Protocol

import numpy as np

NUMBER_OF_HOUSES = 300
INTERPOLATION_STEPS = 10  # 6-minute intervals
DEFAULT_SEED = 1337

#: Standard deviation of the shift, in hours, per insulation level.
HOURS_SHIFTED: dict[str, float] = {"low": 2, "medium": 2.5, "high": 3}


class Randomness(Protocol):
    """Supplies the shift offsets used to smooth one profile."""

    def deviations(self, profile_key: str, size: int, scale: float) -> np.ndarray: ...


def _to_shifts(random_numbers: np.ndarray) -> np.ndarray:
    """Round to 0.1 h and express as a whole number of 6-minute intervals."""
    return (np.round(random_numbers, 1) * 10).astype(int)


class SharedRandomState:
    """One random stream for the whole run, consumed in generation order."""

    def __init__(self, seed: int = DEFAULT_SEED) -> None:
        self.seed = seed
        self._random = np.random.RandomState(seed)

    def deviations(self, profile_key: str, size: int, scale: float) -> np.ndarray:
        del profile_key  # order in the stream is what identifies a profile here
        return _to_shifts(self._random.normal(loc=0.0, scale=scale, size=size))


class PerProfileRandomState:
    """An independent random stream per profile, seeded from the profile key."""

    def __init__(self, seed: int = DEFAULT_SEED) -> None:
        self.seed = seed

    def deviations(self, profile_key: str, size: int, scale: float) -> np.ndarray:
        random = np.random.RandomState(self._seed_for(profile_key))
        return _to_shifts(random.normal(loc=0.0, scale=scale, size=size))

    def _seed_for(self, profile_key: str) -> int:
        # Python's hash() is salted per process, so digest the key instead.
        digest = hashlib.blake2b(profile_key.encode(), digest_size=4).digest()
        return (self.seed + int.from_bytes(digest, "big")) % 2**32


def interpolate(curve: np.ndarray, steps: int = INTERPOLATION_STEPS) -> np.ndarray:
    """Linearly upsample an hourly curve, wrapping from the last hour to the first."""
    start = curve
    stop = np.roll(curve, -1)
    step_size = (stop - start) / steps

    return (start[:, None] + np.arange(steps) * step_size[:, None]).ravel()


def resample_to_hourly(
    curve: np.ndarray, steps: int = INTERPOLATION_STEPS
) -> np.ndarray:
    """Average each hour's sub-intervals, centred on the whole hour."""
    blocks = np.roll(curve, steps // 2).reshape(-1, steps)

    # Summed left to right rather than with `blocks.sum(axis=1)`, whose pairwise
    # ordering would perturb the last bits of the shipped curves.
    total = blocks[:, 0].copy()
    for step in range(1, steps):
        total += blocks[:, step]

    return total / steps


def calculate_smoothed_demand(
    heat_demand: np.ndarray,
    insulation_level: str,
    randomness: Randomness,
    profile_key: str,
) -> np.ndarray:
    """Aggregate `NUMBER_OF_HOUSES` time-shifted copies of a single-house curve."""
    shifts = randomness.deviations(
        profile_key, NUMBER_OF_HOUSES, HOURS_SHIFTED[insulation_level]
    )
    interpolated = interpolate(heat_demand)

    cumulative = np.zeros_like(interpolated)
    for shift in shifts:
        cumulative += np.roll(interpolated, shift)

    return resample_to_hourly(cumulative)
