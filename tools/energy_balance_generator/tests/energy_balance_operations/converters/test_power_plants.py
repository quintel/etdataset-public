import pytest
import pandas as pd

from etm_tools.energy_balance_operations.converters import PowerPlantConverter
from etm_tools.energy_balance_operations.full_load_hours import FullLoadHoursCalculator

# Using an altered version of dummy EB:
#                                                                              Electricity  Coking coal  Anthracite  Total
# Final consumption - industry sector - chemical and petrochemical - energy use     0       9900         1200        10100
# Gross electricity production - autoproducer electricity only                      0       5000         10000       15000
# Gross electricity production - main activity producer electricity only            0       5000         10000       15000
# Transformation input - electricity...main activity...electricity only...energy    0       8000         8000        16000
# Transformation input - electricity...autoproducer electricity only...energy       0       8000         8000        16000

@pytest.fixture
def plants(first_plant_share):
    # plant_type          input output       input_share          output_share
    # plant_type          input output       X                    X
    # 'Nice coal plant'   Coal  Electricity  first_plant_share    first_plant_share
    # 'Other coal plant'  Coal  Electricity  1-first_plant_share  1-first_plant_share
    country = 'X'

    return pd.DataFrame([['Coal', 'Electricity', first_plant_share, first_plant_share],['Coal', 'Electricity', 1-first_plant_share, 1-first_plant_share]],
    columns=[('input', 'input'), ('output', 'output'), ('input_share', country), ('output_share', country)], index=['Nice coal plant', 'Other coal plant'])


def ready_energy_balance_for_coal_conversions(eb):
    # Add neccesary flows to the dummy EB
    for flow in PowerPlantConverter.production_labels('electricity'):
        eb.add_row_with_energy(flow, {'Coking coal': 5000, 'Anthracite': 10000})

    for flow in PowerPlantConverter.transformation_labels('electricity'):
        eb.add_row_with_energy(flow, {'Coking coal': 8000, 'Anthracite': 8000})

    # Make sure all requested products are in the dummy EB
    for product in PowerPlantConverter.PRODUCT_GROUPS['Coal']:
        if not product in eb.eb.columns:
            eb.eb[product] = 0


@pytest.mark.parametrize('first_plant_share', [1.0, 0.75, 0.5, 0.25])
def test_electricity_output_calculation(energy_balance, plants):
    ready_energy_balance_for_coal_conversions(energy_balance)

    ppc = PowerPlantConverter(energy_balance)

    # Grab the plant share we are currently testing for
    test_share = plants['input_share', 'X']['Nice coal plant']
    test_flow = 'Gross electricity production - main activity producer electricity only'

    # Safety check: there is some anthracite in the producer table to start with
    assert energy_balance.eb['Anthracite'][test_flow] == 10000

    # Convert!!
    ppc.conversion('X', plants=plants)

    # Nothing happend to producer table
    assert energy_balance.eb['Anthracite'][test_flow] == 10000

    # The nice plant got the test_share share of the produced things
    assert energy_balance.eb['Electricity']['Nice coal plant'] == (30000 * test_share)

    # The other plant got the rest
    assert energy_balance.eb['Electricity']['Other coal plant'] == (30000 * (1 - test_share))


@pytest.mark.parametrize('first_plant_share', [1.0, 0.75, 0.5, 0.25])
def test_electricity_input_calculation(energy_balance, plants):
    ready_energy_balance_for_coal_conversions(energy_balance)

    # Grab the plant share we are currently testing for
    test_share = plants['input_share', 'X']['Nice coal plant']
    test_flow = 'Transformation input - electricity and heat generation - autoproducer electricity only - energy use'

    ppc = PowerPlantConverter(energy_balance)

    # Safety check: there is some anthracite in transformation to start with
    assert energy_balance.eb['Anthracite'][test_flow] == 8000

    # Convert!!
    ppc.conversion('X', plants=plants)

    # Nothing happend to transformation flow
    assert energy_balance.eb['Anthracite'][test_flow] == 8000

    # The nice plant got the test_share share of the transformed things
    assert energy_balance.eb['Anthracite']['Nice coal plant'] == (16000 * test_share)

    # The other plant got the rest
    assert energy_balance.eb['Anthracite']['Other coal plant'] == (16000 * (1 - test_share))


@pytest.mark.parametrize('first_plant_share', [1.0, 0.75, 0.5, 0.25])
def test_full_load_hours(energy_balance, plants):
    ready_energy_balance_for_coal_conversions(energy_balance)
    conv = FullLoadHoursCalculator.TJ_TO_MWH

    # Give each plant a capacity of 300
    plants['net_max_generating_capacity_MW', 'X'] = 300

    # Grab the plant share we are currently testing for
    test_share = plants['input_share', 'X']['Nice coal plant']

    # Here we go!
    flh_calc = FullLoadHoursCalculator()
    ppc = PowerPlantConverter(energy_balance)

    ppc.conversion('X', plants, flh_calc=flh_calc)

    assert flh_calc.full_load_hours['Nice coal plant'] == (test_share * 100 * conv)
    assert 'Other coal plant' in flh_calc.full_load_hours

