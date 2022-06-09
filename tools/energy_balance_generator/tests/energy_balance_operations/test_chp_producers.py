import pytest
import pandas as pd
from etm_tools.energy_balance_operations.chp_producers import CHPProducers
from etm_tools.utils.conversion_map import ConversionMap

@pytest.fixture
def producers():
    return CHPProducers.from_csv(ConversionMap().inputs('chps', 'NL')['path'])


def test_gas_based_plants(producers):
    for producer in producers.gas_based_chps:
        assert producer.fuel == ['Gas', 'Oil']

        if not producer.industrial_plant:
            # Then there should be a residential plant
            assert producer.residential_plant.fuel == ['Gas']
        elif not producer.residential_plant:
            # Then there should be a industrial plant
            assert producer.industrial_plant.backup_flh is not None
            assert producer.industrial_plant.fuel == ['Gas', 'Oil']
        else:
            # Then both should be present and different
            assert producer.has_subplants_with_different_fuels() is True
            assert producer.subplants_fuel_diff() == 'Oil'


def test_cached_property(producers):
    '''Is it really the same object?'''
    call_one = producers.gas_based_chps
    call_two = producers.gas_based_chps

    for i in range(len(call_one)):
        assert call_one[0] == call_two[0]

    for producer in call_one:
        producer.name = 'giraffe'

    for producer in call_two:
        assert producer.name == 'giraffe'
