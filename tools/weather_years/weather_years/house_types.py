"""The housing stock.

The number of household profiles produced follows from
the table: `len(stock) * len(INSULATION_LEVELS)`.

Provenance of the Dutch values: the R-values and behaviour-fitting numbers below
are the set used to generate the nl2019 dataset. Window areas and surface areas
come from the same calibration.

Profile *order* is load-bearing while `SharedRandomState` smoothing is in use:
profiles draw from one random stream in the order this table lists them, each
consuming 300 draws. Inserting, removing or reordering an entry changes the
draws every profile after it receives, and so changes those curves. See
`smoothing.py`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

#: Ordered least- to best-insulated. Also the thermostat column names.
INSULATION_LEVELS: tuple[str, ...] = ("low", "medium", "high")


@dataclass(frozen=True)
class HouseType:
    """One house type and its per-insulation-level calibration."""

    name: str
    surface_area: float  # m² of heat-losing envelope
    window_area: float  # m² of glazing admitting solar gain
    r_values: Mapping[str, float]  # m²K/W, per insulation level
    behaviour_fitting: Mapping[str, float]  # kWh/K, added to the base heat capacity

    def r_value(self, insulation_level: str) -> float:
        return self.r_values[insulation_level]

    def behaviour(self, insulation_level: str) -> float:
        return self.behaviour_fitting[insulation_level]


NL2019_STOCK: tuple[HouseType, ...] = (
    HouseType(
        name="terraced_houses",
        surface_area=183,
        window_area=6.08289109,
        r_values={"low": 0.72608224, "medium": 0.95303516, "high": 2.20833951},
        behaviour_fitting={"low": 0.44224575, "medium": 2.61042431, "high": 0.59483274},
    ),
    HouseType(
        name="semi_detached_houses",
        surface_area=279,
        window_area=5.80327128,
        r_values={"low": 0.92629934, "medium": 1.20779267, "high": 2.90413756},
        behaviour_fitting={"low": 1.57962902, "medium": 4.43499574, "high": 0.45485638},
    ),
    HouseType(
        name="apartments",
        surface_area=187,
        window_area=5.53039382,
        r_values={"low": 0.96937942, "medium": 1.39716924, "high": 2.95000949},
        behaviour_fitting={
            "low": -0.11691841,
            "medium": 0.80467653,
            "high": 2.78210071,
        },
    ),
    HouseType(
        name="detached_houses",
        surface_area=405,
        window_area=6.12774164,
        r_values={"low": 1.02227109, "medium": 1.2962618, "high": 3.10765405},
        behaviour_fitting={"low": 3.34031291, "medium": 7.76537119, "high": 2.74614981},
    ),
)

# Retired from the Dutch stock, but still used in tests to check that the generator
# produces the same curves for the same inputs as it did when they were in the stock.
LEGACY_CORNER_HOUSES = HouseType(
    name="corner_houses",
    surface_area=239,
    window_area=5.53694918,
    r_values={"low": 0.86234292, "medium": 1.05413341, "high": 2.73029519},
    behaviour_fitting={"low": 1.63456613, "medium": 4.84495401, "high": 0.96159576},
)


def profile_keys(stock: tuple[HouseType, ...] = NL2019_STOCK) -> list[str]:
    """Curve keys in generation order: house-major, insulation level inner."""
    return [
        f"insulation_{house.name}_{level}"
        for house in stock
        for level in INSULATION_LEVELS
    ]
