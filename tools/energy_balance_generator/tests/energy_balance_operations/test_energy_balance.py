# See the conftest.py for the dummy energy_balance:
#                                                                              Electricity  Coking coal  Anthracite  Total
# Final consumption - industry sector - chemical and petrochemical - energy use     0       9900         1200        10100
# Gross electricity production - autoproducer electricity only                      0       5000         10000       15000

def test_calculate_total(energy_balance):
    # With an empty row
    energy_balance.add_empty_row('Empty')

    assert energy_balance.eb['Total']['Empty'] == 0

    energy_balance.calculate_total('Empty')

    assert energy_balance.eb['Total']['Empty'] == 0

    # Fill in some value
    energy_balance.eb['Electricity']['Empty'] = 10000
    energy_balance.calculate_total('Empty')

    assert energy_balance.eb['Total']['Empty'] == 10000

    # Fill in a second value
    energy_balance.eb['Anthracite']['Empty'] = 5000
    energy_balance.calculate_total('Empty')

    assert energy_balance.eb['Total']['Empty'] == 15000


def test_shift_energy(energy_balance):
    energy_balance.shift_energy('Gross electricity production - autoproducer electricity only',
        'New flow', {'Coking coal': 900})

    assert energy_balance.eb['Coking coal']['New flow'] == 900
    assert energy_balance.eb['Coking coal']['Gross electricity production - autoproducer electricity only'] == 4100
    assert energy_balance.eb['Coking coal']['Gross electricity production - autoproducer electricity only - original'] == 5000


def test_add_row_with_energy(energy_balance):
    # Without total
    energy_balance.add_row_with_energy('Some powerplant', {'Electricity': 900}, total=False)

    assert energy_balance.eb['Electricity']['Some powerplant'] == 900
    assert energy_balance.eb['Total']['Some powerplant'] == 0

    # With total
    energy_balance.add_row_with_energy('Some industry', {'Coking coal': 1000})

    assert energy_balance.eb['Coking coal']['Some industry'] == 1000
    assert energy_balance.eb['Total']['Some industry'] == 1000


def test_add_row_from_share(energy_balance):
    energy_balance.add_row_from_share('Gross electricity production - autoproducer electricity only',
        'My new flow', 0.5)

    assert energy_balance.eb['Coking coal']['My new flow'] == 2500


def test_share_to_tj(energy_balance):
    flows = [
        'Gross electricity production - autoproducer electricity only',
        'Final consumption - industry sector - chemical and petrochemical - energy use'
    ]

    # With one flow
    in_tj = energy_balance.share_to_tj(
        flows[0],
        0.5,
        ['Coking coal', 'Anthracite'],
        merge_products=True
    )
    assert in_tj == 7500


    # With two flows
    in_tj = energy_balance.share_to_tj(
        flows,
        0.5,
        ['Coking coal', 'Anthracite'],
        merge_products=True
    )
    assert in_tj == 13050

    # With two flows and unmerged products
    in_tj = energy_balance.share_to_tj(
        flows,
        0.5,
        ['Coking coal', 'Anthracite'],
        merge_products=False
    )
    assert in_tj == {'Anthracite': 5600.0, 'Coking coal': 7450.0}

def test_product_shares_to_tj(energy_balance):
    flow = 'Gross electricity production - autoproducer electricity only'
    product_shares = {'Anthracite': 0.5, 'Coking coal': 1.0}

    product_amounts = energy_balance.product_shares_to_tj(flow, product_shares)

    assert product_amounts['Anthracite'] == 5000
    assert product_amounts['Coking coal'] == 5000
