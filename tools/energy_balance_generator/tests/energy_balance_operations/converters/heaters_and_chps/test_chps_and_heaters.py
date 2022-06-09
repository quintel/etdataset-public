import pytest
import pandas as pd

from etm_tools.energy_balance_operations.converters import HeatersAndCHPsConverter
from etm_tools.energy_balance_operations.plant import Producer
from etm_tools.energy_balance_operations.chp_capacities import CHPCapacities
from etm_tools.energy_balance_operations.chp_producers import CHPProducers
from etm_tools.utils.conversion_map import ConversionMap
from etm_tools.energy_balance_operations.full_load_hours import FullLoadHoursCalculator

@pytest.fixture
def chp_capacities():
    return CHPCapacities(
        pd.read_csv('tests/fixtures/chp_capacities_eurostat_nl_2019.csv',
            index_col=0, header=[0,1,2]),
        2019,
        'NL'
    )


@pytest.fixture
def chp_producers():
    return CHPProducers.from_csv(ConversionMap().inputs('chps', 'NL')['path'])


# Using an altered version of dummy EB:
#                                                                              Electricity  Coking coal  Anthracite  Total
# Final consumption - industry sector - chemical and petrochemical - energy use     0       9900         1200        10100
# Gross heat production - autoproducer heat only                                    0       5000         10000       15000
# Gross heat production - main activity producer heat only                          0       5000         10000       15000
# Transformation input - heat...main activity...heat only...energy                  0       8000         8000        16000
# Transformation input - heat...autoproducer heat only...energy                     0       8000         8000        16000

# TODO: fix thissssss
def ready_energy_balance_for_coal_conversions(eb):
    # Add neccesary flows to the dummy EB
    for flow in HeatersAndCHPsConverter.production_flows('heat', is_chp=False):
        eb.add_row_with_energy(flow, {'Coking coal': 5000, 'Anthracite': 10000})
    for flow in HeatersAndCHPsConverter.production_flows('heat'):
        eb.add_row_with_energy(flow, {'Coking coal': 3000, 'Anthracite': 6000})
    for flow in HeatersAndCHPsConverter.production_flows('electricity'):
        eb.add_row_with_energy(flow, {'Coking coal': 7500, 'Anthracite': 12500})

    for flow in HeatersAndCHPsConverter.transformation_input_flows(is_chp=False):
        eb.add_row_with_energy(flow, {'Coking coal': 8000, 'Anthracite': 8000})
    for flow in HeatersAndCHPsConverter.transformation_input_flows():
        eb.add_row_with_energy(flow, {'Coking coal': 4000, 'Anthracite': 4000})

    # Add Heat column
    eb.eb['Heat'] = 0

    # Add some final consumption
    ind = 30000 / len(HeatersAndCHPsConverter.INDUSTRY_CONSUMPTION)
    res = 18000 / len(HeatersAndCHPsConverter.RESIDENTIAL_CONSUMPTION)
    for flow in HeatersAndCHPsConverter.INDUSTRY_CONSUMPTION:
        eb.add_row_with_energy(flow, {'Heat': ind})
    for flow in HeatersAndCHPsConverter.RESIDENTIAL_CONSUMPTION:
        eb.add_row_with_energy(flow, {'Heat': res})

    all_products = (fuel for fuel_type in HeatersAndCHPsConverter.PRODUCT_GROUPS.values() for fuel in fuel_type)
    # Make sure all requested products are in the dummy EB
    for product in all_products:
        if not product in eb.eb.columns:
            eb.eb[product] = 0


def test_conversion(energy_balance, chp_capacities, chp_producers):
    ready_energy_balance_for_coal_conversions(energy_balance)

    producers = [
        Producer.from_dict({
            'name': 'Coal heater',
            'network': 'flexible',
            'input': 'Coal',
            'type': 'heater'
        }),
        Producer.from_dict({
            'name': 'Waste heater',
            'network': 'residential',
            'input': 'Waste',
            'type': 'heater'
        }),
    ]


    HeatersAndCHPsConverter.convert(energy_balance, chp_capacities, chp_producers,
        producers, FullLoadHoursCalculator())

    # Residential heat final consumption = 18000, industry = 30000.
    # Total Coking coal for the heater is 16000, Total heat for the heater is 30000
    assert 'Coal heater - residential' in energy_balance.eb.index
    assert round(energy_balance.eb['Coking coal']['Coal heater - residential']) == 6002
    assert round(energy_balance.eb['Heat']['Coal heater - residential']) == 11253
    assert energy_balance.eb['Electricity']['Coal heater - residential'] == 0

    assert 'Coal heater - industrial' in energy_balance.eb.index
    assert round(energy_balance.eb['Coking coal']['Coal heater - industrial']) == 9998
    assert round(energy_balance.eb['Heat']['Coal heater - industrial']) == 30000 - 11253
    assert energy_balance.eb['Electricity']['Coal heater - industrial'] == 0

    # And no 'normal' CHP (without sector name)
    assert not 'Coal heater' in energy_balance.eb.index
