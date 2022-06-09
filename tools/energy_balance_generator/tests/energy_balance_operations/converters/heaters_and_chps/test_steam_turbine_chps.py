import pytest
import pandas as pd
from etm_tools.energy_balance_operations.converters.heaters_and_chps.steam_turbine_chps import SteamTurbineCHPConverter
from etm_tools.energy_balance_operations.chp_capacities import CHPCapacities
from etm_tools.energy_balance_operations.heat_network import HeatNetworks
from etm_tools.utils.conversion_map import ConversionMap
from etm_tools.energy_balance_operations.chp_producers import CHPProducers
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


def ready_energy_balance_for_steam_turbines(eb):
    products = [p for v in SteamTurbineCHPConverter.PRODUCT_GROUPS.values() for p in v]
    for product in (products + ['Electricity', 'Heat']):
        if not product in eb.eb.columns:
            eb.eb[product] = 0

    # Add flows
    for flow in (SteamTurbineCHPConverter.production_flows('electricity') +
        SteamTurbineCHPConverter.production_flows('heat')):
        eb.add_row_with_energy(flow,
            {'Coke oven gas': 2000, 'Anthracite': 100, 'Lignite': 800,
            'Primary solid biofuels': 300, 'Renewable municipal waste': 200}
        )

    for flow in SteamTurbineCHPConverter.transformation_input_flows():
        eb.add_row_with_energy(flow,
            {'Coke oven gas': 2200, 'Anthracite': 110, 'Lignite': 1000,
            'Primary solid biofuels': 500, 'Renewable municipal waste': 400}
        )


def test_conversion(energy_balance, chp_capacities, chp_producers):
    ready_energy_balance_for_steam_turbines(energy_balance)
    heat_networks = HeatNetworks(1000,500)

    SteamTurbineCHPConverter.convert(energy_balance, chp_producers, chp_capacities,
        heat_network=heat_networks, flh_calc=FullLoadHoursCalculator())

    # Added to EB
    assert 'Steam Turbine CHP - Wood pellets' in energy_balance.eb.index

    # Added to HN
    heat_networks_flexibles = [producer.name for producer in heat_networks.unassigned_producers]
    assert 'Steam Turbine CHP - Wood pellets' in heat_networks_flexibles


def test_plant(energy_balance, chp_producers):
    ready_energy_balance_for_steam_turbines(energy_balance)

    conv = SteamTurbineCHPConverter(energy_balance, chp_producers)

    for producer in chp_producers.steam_turbine_chps:
        if producer.name == conv.EXCLUDE:
            continue

        if producer.network == 'residential':
            assert producer.residential_plant.name
