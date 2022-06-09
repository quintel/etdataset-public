import pytest
import pandas as pd
from etm_tools.energy_balance_operations.chp_capacities import CHPCapacities

@pytest.fixture
def chp_capacities(capacities_as_frame):
    return CHPCapacities(
        capacities_as_frame,
        2019,
        'NL'
    )


@pytest.fixture
def capacities_as_frame():
    return pd.read_csv('tests/fixtures/chp_capacities_eurostat_nl_2019.csv',
        index_col=0, header=[0,1,2])


def test_capacity(chp_capacities):
    assert chp_capacities.capacity('Internal Combustion CHP', 'electricity') == 180.028#3042.178
    assert round(chp_capacities.capacity('Steam Turbine CHP', 'heat')) == 3011


def test_simplify_with_steam_trubines_missing(capacities_as_frame):
    capacities_as_frame = capacities_as_frame.drop(CHPCapacities.STEAM_TURBINES, axis=1, level=0)

    capacities = CHPCapacities(capacities_as_frame, 2019, 'NL')

    assert capacities.capacity('Steam Turbine CHP') == 0


def test_simplify_with_one_steam_turbine_missing(capacities_as_frame):
    capacities_as_frame = capacities_as_frame.drop(CHPCapacities.STEAM_TURBINES[0], axis=1, level=0)

    capacities = CHPCapacities(capacities_as_frame, 2019, 'NL')

    assert capacities.capacity('Steam Turbine CHP') != 0
