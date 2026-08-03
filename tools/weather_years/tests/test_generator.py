"""What the generator produces, and which way its curves move.

Every assertion is either structural — how many curves, how long, how named, how
normalised — or directional: colder days need more heat, sunlight offsets it,
wind adds to it. Nothing asserts the value of a particular hour, so these hold
on any input year while still catching a swapped house type, an inverted
temperature response or a dropped wind term.
"""

from __future__ import annotations

from dataclasses import replace

import numpy as np
import pytest

from weather_years import (
    InputError,
    PerProfileRandomState,
    SharedRandomState,
    WeatherYearGenerator,
    generate_weather_year,
    profile_keys,
)
from weather_years.constants import (
    HEAT_CAPACITY_HOUSE,
    HOURS_PER_DAY,
    HOURS_PER_YEAR,
    PROFILE_TOTAL,
)

HOUSEHOLD = "insulation_terraced_houses_low"
NON_RESIDENTIAL = ("buildings_heating", "agriculture_heating")


def curves_by_key(inputs, **options) -> dict[str, np.ndarray]:
    return {
        curve.key: curve.values for curve in generate_weather_year(inputs, **options)
    }


def daily_totals(hourly: np.ndarray) -> np.ndarray:
    return hourly.reshape(-1, HOURS_PER_DAY).sum(axis=1)


def coldest_days(temperature: np.ndarray, count: int = 30) -> np.ndarray:
    """Day indices of the coldest days of the year."""
    return np.argsort(daily_totals(temperature))[:count]


# The output contract etsource reads.


def test_household_inputs_produce_the_twelve_insulation_profiles(synthetic_inputs):
    curves = generate_weather_year(synthetic_inputs)

    assert [curve.key for curve in curves] == profile_keys()


def test_wind_and_g2a_add_the_two_non_residential_profiles(synthetic_full_inputs):
    curves = curves_by_key(synthetic_full_inputs)

    assert set(curves) == set(profile_keys()) | set(NON_RESIDENTIAL)
    # The G2A method draws no distinction between the two sectors.
    assert np.array_equal(*(curves[key] for key in NON_RESIDENTIAL))


def test_every_curve_is_a_normalised_year(synthetic_full_inputs):
    """ETM reads these as shares of annual demand: 8760 values summing to 1/3600."""
    for key, values in curves_by_key(synthetic_full_inputs).items():
        assert len(values) == HOURS_PER_YEAR, key
        assert values.sum() == pytest.approx(PROFILE_TOTAL, rel=1e-12), key
        assert (values >= 0).all(), key


# How the curves respond to the weather.


def test_demand_rises_as_the_days_get_colder(synthetic_full_inputs):
    """The response that must not invert, for every curve the generator makes."""
    temperature = daily_totals(synthetic_full_inputs.temperature)

    for key, values in curves_by_key(synthetic_full_inputs).items():
        correlation = np.corrcoef(daily_totals(values), temperature)[0, 1]
        assert correlation < -0.8, f"{key} correlates {correlation:.2f} with temperature"


def test_sunlight_reduces_household_demand(synthetic_inputs):
    """Solar gain through the windows offsets heating; removing it raises demand."""
    unlit = replace(synthetic_inputs, irradiation=np.zeros(HOURS_PER_YEAR))
    cold = coldest_days(synthetic_inputs.temperature)

    sunny_days, unlit_days = (
        daily_totals(curves_by_key(inputs)[HOUSEHOLD])
        for inputs in (synthetic_inputs, unlit)
    )

    # Curves are normalised, so compare where the demand sits rather than its
    # size: without solar gain the mild shoulder days need heating too.
    assert unlit_days[cold].sum() < sunny_days[cold].sum()


def test_wind_chill_raises_building_demand(synthetic_full_inputs):
    """Wind is part of the G2A effective temperature, not decoration."""
    still = replace(synthetic_full_inputs, wind_speed=np.zeros(HOURS_PER_YEAR))
    windiest = np.argsort(synthetic_full_inputs.wind_speed)[-100:]

    windy_curve = curves_by_key(synthetic_full_inputs)["buildings_heating"]
    still_curve = curves_by_key(still)["buildings_heating"]

    assert windy_curve[windiest].sum() > still_curve[windiest].sum()


def test_heat_capacity_is_computed_from_the_house_geometry():
    """A rounded literal here drifted from its own documented geometry once and
    moved household curves by up to a third of their peak."""
    assert HEAT_CAPACITY_HOUSE == pytest.approx(2.8160022528, abs=1e-12)


# Whether a curve depends on what was generated alongside it.

PROFILE = ("detached_houses", "medium")
PROFILE_KEY = f"insulation_{PROFILE[0]}_{PROFILE[1]}"


def profile_on_its_own(inputs, randomness) -> np.ndarray:
    generator = WeatherYearGenerator(inputs, randomness=randomness)

    return generator.household_profile(*PROFILE).values


def test_per_profile_smoothing_reproduces_a_single_profile(synthetic_inputs):
    """Regenerating one house type alone is only trustworthy in this mode."""
    in_set = curves_by_key(synthetic_inputs, randomness=PerProfileRandomState())

    assert np.array_equal(
        in_set[PROFILE_KEY],
        profile_on_its_own(synthetic_inputs, PerProfileRandomState()),
    )


def test_per_profile_streams_are_keyed_on_the_profile():
    """Two profiles must not share a stream, or their smoothing would correlate.

    The key is digested rather than passed to `hash()`, which is salted per
    process, so the same profile also seeds the same way in the next run.
    """
    randomness = PerProfileRandomState()

    def shifts(profile_key):
        return randomness.deviations(profile_key, size=24, scale=2.0)

    assert not np.array_equal(
        shifts("insulation_apartments_low"), shifts("insulation_apartments_high")
    )


def test_shared_smoothing_depends_on_generation_order(synthetic_inputs):
    """Frozen deliberately: every weather year ETM ships was generated from one
    shared random stream, so reproducing them requires the order-dependence."""
    in_set = curves_by_key(synthetic_inputs, randomness=SharedRandomState())
    alone = profile_on_its_own(synthetic_inputs, SharedRandomState())

    deviation = np.max(np.abs(in_set[PROFILE_KEY] - alone)) / np.max(alone)
    assert deviation > 0.001, (
        "Shared-stream smoothing no longer depends on generation order, so it no "
        "longer reproduces the weather years ETM ships."
    )


# Inputs that would otherwise produce plausible wrong curves.

REJECTED = {
    "temperature in kelvin": (
        "kelvin",
        lambda good: {"temperature": good.temperature + 273.15},
    ),
    "irradiation in W/m²": (
        r"W/m²",
        lambda good: {"irradiation": good.irradiation * 1e4 / 3600},
    ),
    "a leap year that was not trimmed": (
        f"{HOURS_PER_YEAR} hourly values",
        lambda good: {"temperature": np.concatenate([good.temperature, np.zeros(24)])},
    ),
    "a thermostat without a row per hour": (
        f"{HOURS_PER_DAY} rows",
        lambda good: {"thermostat": good.thermostat.head(12)},
    ),
    "G2A parameters missing a column": (
        "slope",
        lambda good: {"g2a_parameters": good.g2a_parameters.drop(columns="slope")},
    ),
}


@pytest.mark.parametrize(("expected", "break_it"), REJECTED.values(), ids=REJECTED)
def test_an_unusable_input_is_rejected_by_name(synthetic_full_inputs, expected, break_it):
    """Each message names the unit or shape it wanted, and how to get there."""
    with pytest.raises(InputError, match=expected):
        replace(synthetic_full_inputs, **break_it(synthetic_full_inputs))
