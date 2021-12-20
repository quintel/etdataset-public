from etm_tools.energy_balance_operations.converters import HeatersAndCHPsConverter

# Using an altered version of dummy EB:
#                                                                              Electricity  Coking coal  Anthracite  Total
# Final consumption - industry sector - chemical and petrochemical - energy use     0       9900         1200        10100
# Gross heat production - autoproducer heat only                                    0       5000         10000       15000
# Gross heat production - main activity producer heat only                          0       5000         10000       15000
# Transformation input - heat...main activity...heat only...energy                  0       8000         8000        16000
# Transformation input - heat...autoproducer heat only...energy                     0       8000         8000        16000


def ready_energy_balance_for_coal_conversions(eb):
    # Add neccesary flows to the dummy EB
    for flow in HeatersAndCHPsConverter.production_labels('heat only'):
        eb.add_row_with_energy(flow, {'Coking coal': 5000, 'Anthracite': 10000})
    for flow in HeatersAndCHPsConverter.production_labels('combined heat and power', 'heat'):
        eb.add_row_with_energy(flow, {'Coking coal': 3000, 'Anthracite': 6000})
    for flow in HeatersAndCHPsConverter.production_labels('combined heat and power', 'electricity'):
        eb.add_row_with_energy(flow, {'Coking coal': 7500, 'Anthracite': 12500})

    for flow in HeatersAndCHPsConverter.transformation_labels('heat only'):
        eb.add_row_with_energy(flow, {'Coking coal': 8000, 'Anthracite': 8000})
    for flow in HeatersAndCHPsConverter.transformation_labels('combined heat and power'):
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

    # Make sure all requested products are in the dummy EB
    for product in HeatersAndCHPsConverter.PRODUCT_GROUPS['Coal']:
        if not product in eb.eb.columns:
            eb.eb[product] = 0


def test_conversion(energy_balance):
    ready_energy_balance_for_coal_conversions(energy_balance)

    producers = [
        {
            'name': 'Coal heater',
            'network': 'industrial',
            'input': 'Coal',
            'type': 'heater'
        },
        {
            'name': 'Coal CHP',
            'network': 'flexible',
            'input': 'Coal',
            'type': 'chp'
        },
    ]

    HeatersAndCHPsConverter.convert(energy_balance, producers)

    assert 'Coal heater - industrial' in energy_balance.eb.index
    assert energy_balance.eb['Coking coal']['Coal heater - industrial'] == 16000
    assert energy_balance.eb['Heat']['Coal heater - industrial'] == 30000

    # Residential heat final consumption = 18000, industry = 30000. Already 30000 in industry. So
    # 100% should go to residential
    assert 'Coal CHP - residential' in energy_balance.eb.index
    assert energy_balance.eb['Coking coal']['Coal CHP - residential'] == 8000
    assert energy_balance.eb['Heat']['Coal CHP - residential'] == 18000
    assert energy_balance.eb['Electricity']['Coal CHP - residential'] == 40000

    assert 'Coal CHP - industry' in energy_balance.eb.index
    assert energy_balance.eb['Coking coal']['Coal CHP - industry'] == 0
    assert energy_balance.eb['Heat']['Coal CHP - industry'] == 0
    assert energy_balance.eb['Electricity']['Coal CHP - industry'] == 0

    # And no 'normal' CHP (without sector name)
    assert not 'Coal CHP' in energy_balance.eb.index
