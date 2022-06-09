import pandas as pd
from pytest import fixture
import pytest
from etm_tools.energy_balance_operations.converters.heaters_and_chps.gas_chps import GasCHPsConverter, CHPLogger
from etm_tools.energy_balance_operations.chp_capacities import CHPCapacities
from etm_tools.energy_balance_operations.chp_producers import CHPProducers
from etm_tools.utils.conversion_map import ConversionMap
from etm_tools.energy_balance_operations.heat_network import HeatNetworks
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


def ready_energy_balance_for_gas_chps(eb):
    for product in ( GasCHPsConverter.PRODUCT_GROUPS['Gas'] +
        GasCHPsConverter.PRODUCT_GROUPS['Coal gas'] +
        GasCHPsConverter.PRODUCT_GROUPS['Oil'] + GasCHPsConverter.PRODUCT_GROUPS['Biogas'] +
        ['Electricity', 'Heat']):
        if not product in eb.eb.columns:
            eb.eb[product] = 0

    # Add flows
    for flow in (GasCHPsConverter.production_flows('electricity') +
        GasCHPsConverter.production_flows('heat')):
        eb.add_row_with_energy(flow, {'Natural gas': 2000, 'Biogases': 100, 'Crude oil': 800})

    for flow in GasCHPsConverter.transformation_input_flows('electricity'):
        eb.add_row_with_energy(flow, {'Natural gas': 2200, 'Biogases': 110, 'Crude oil': 1000})


def test_conversion(energy_balance, chp_capacities, chp_producers):
    ready_energy_balance_for_gas_chps(energy_balance)

    GasCHPsConverter.convert(energy_balance, chp_producers, chp_capacities,
        heat_network=HeatNetworks(1000,500), flh_calc=FullLoadHoursCalculator())

    assert energy_balance.eb['Electricity'].loc[GasCHPsConverter.BIO_ICE] > 0


def test_calculate_output_shares(energy_balance, chp_producers, chp_capacities):
    ready_energy_balance_for_gas_chps(energy_balance)

    converter = GasCHPsConverter(energy_balance, chp_producers)
    result = CHPLogger()
    converter.result = result

    converter.calculate_output_shares(chp_capacities, 'electricity')

    total_ice_cap = chp_capacities.capacity('Internal Combustion CHP', 'electricity')

    assert result.get(converter.BIO_ICE, 'electricity', 'capacity') < total_ice_cap
    assert (result.get(converter.BIO_ICE, 'electricity', 'capacity') +
            result.get('Internal Combustion CHP', 'electricity', 'capacity')) == total_ice_cap
    assert result.get('Internal Combustion CHP', 'electricity', 'output_share') < 1


def test_calculate_input_shares(energy_balance, chp_capacities, chp_producers):
    ready_energy_balance_for_gas_chps(energy_balance)

    converter = GasCHPsConverter(energy_balance, chp_producers)
    result = CHPLogger()
    converter.result = result
    converter.calculate_output_shares(chp_capacities, 'electricity')

    converter.calculate_input_shares()

    assert round(result.get('Internal Combustion CHP', item='input_share'), 2) == 0.04#0.38 in CHP mode


def test_with_a_lot_of_biogas(energy_balance, chp_capacities, chp_producers):
    ready_energy_balance_for_gas_chps(energy_balance)
    heat_network = HeatNetworks(1000,500)
    flh_calc = FullLoadHoursCalculator()

    # Add substantial amount of biogas
    energy_balance.eb['Biogases'][GasCHPsConverter.production_flows('electricity')] = 1500

    converter = GasCHPsConverter(energy_balance, chp_producers)
    result = CHPLogger()
    converter.result = result

    # Parse the biogas plant
    biogas_producer = chp_producers.biogas_chp
    converter.split(biogas_producer, heat_network, flh_calc, chp_capacities, cap_tech='Internal Combustion CHP')

    # Caculate shares and add to result
    converter.calculate_output_shares(chp_capacities, 'electricity')

    total_ice_cap = chp_capacities.capacity('Internal Combustion CHP', 'electricity')

    # Assigned capacity to Biogas should be equal or smaller than total ICE capacity
    assert result.get(GasCHPsConverter.BIO_ICE, 'electricity', 'capacity') <= total_ice_cap
    assert result.get(GasCHPsConverter.BIO_ICE, 'electricity', 'capacity') > 0
    # Some stuff should still go to 'normal' ICE
    assert result.get('Internal Combustion CHP', 'electricity', 'output_share') > 0


def test_with_coal_gas_and_low_capacities(energy_balance, chp_capacities, chp_producers):
    ready_energy_balance_for_gas_chps(energy_balance)
    heat_network = HeatNetworks(1000,500)
    flh_calc = FullLoadHoursCalculator()

    converter = GasCHPsConverter(energy_balance, chp_producers)
    result = CHPLogger()
    converter.result = result

    # Put a tiny bit of coal gas in the EB, and low capacities for CHPs
    energy_balance.eb[converter.PRODUCT_GROUPS['Coal gas']] = 10
    chp_capacities.eb[chp_capacities.eb.columns] = 1

    coal_gas_plant = chp_producers.coal_gas_chp
    converter.split(coal_gas_plant, heat_network, flh_calc, chp_capacities)

    # Assigned capacity should not be bigger than total CHP capacity
    total_capacity = chp_capacities.sum(converter.GAS_BASED_CHPS, 'electricity')
    assert result.get(coal_gas_plant.name, 'electricity', 'capacity') <= total_capacity


def test_backup_flh(energy_balance, chp_capacities, chp_producers):
    ready_energy_balance_for_gas_chps(energy_balance)
    flh_calc = FullLoadHoursCalculator()

    # Set all backups to 1000 for easy calculation
    for producer in chp_producers.gas_based_chps:
        for _, plant in producer.subplants():
            plant.backup_flh = 1000

    # Set high amount of coal gas, and lower all chp capacities, so we get the
    # CHPCapacityError
    energy_balance.eb[GasCHPsConverter.PRODUCT_GROUPS['Coal gas']] = 2000
    chp_capacities.eb[chp_capacities.eb.columns] = 10

    # Now try to run conversions
    GasCHPsConverter.convert(energy_balance, chp_producers, chp_capacities,
        heat_network=HeatNetworks(1000,500), flh_calc=flh_calc)

    # Backup should be in the FLH calc for the plants that are not yet splitted up
    for producer in chp_producers.gas_based_chps:
        if not producer.has_subplants():
            assert flh_calc.full_load_hours[producer.name] == 1000
