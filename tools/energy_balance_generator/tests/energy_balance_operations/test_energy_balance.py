from etm_tools.energy_balance_operations.energy_balance import EnergyBalance

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


def test_swap_energy(energy_balance):
    from_flow = 'Final consumption - industry sector - chemical and petrochemical - energy use'
    to_flow = 'Gross electricity production - autoproducer electricity only'

    energy_balance.swap_energy(
        from_flow,
        to_flow,
        ['Anthracite'], ['Coking coal']
    )

    assert energy_balance.eb['Coking coal'][from_flow] == 11100
    assert energy_balance.eb['Anthracite'][from_flow] == 0

    assert energy_balance.eb['Coking coal'][to_flow] == 3800
    assert energy_balance.eb['Anthracite'][to_flow] == 11200


def test_swap_energy_from_two_products(energy_balance):
    from_flow = 'Final consumption - industry sector - chemical and petrochemical - energy use'
    to_flow = 'Gross electricity production - autoproducer electricity only'

    energy_balance.eb['Product X'] = 1000

    # When swapping from two products to one
    energy_balance.swap_energy(
        from_flow,
        to_flow,
        ['Anthracite', 'Product X'], ['Coking coal']
    )

    assert energy_balance.eb['Coking coal'][from_flow] == 12100
    assert energy_balance.eb['Anthracite'][from_flow] == 0
    assert energy_balance.eb['Product X'][from_flow] == 0

    assert energy_balance.eb['Coking coal'][to_flow] == 2800
    assert energy_balance.eb['Anthracite'][to_flow] == 11200
    assert energy_balance.eb['Product X'][to_flow] == 2000


def test_swap_energy_with_deficit(energy_balance):
    from_flow = 'Gross electricity production - autoproducer electricity only'
    to_flow = 'Final consumption - industry sector - chemical and petrochemical - energy use'

    # Trying to swap 10000 Anth for Coal when there is only 9900 Coal available
    energy_balance.swap_energy(
        from_flow,
        to_flow,
        ['Anthracite'],['Coking coal']
    )

    # Should only swap the 9900, 100 Anthracite remains
    assert energy_balance.eb['Coking coal'][from_flow] == 14900
    assert energy_balance.eb['Anthracite'][from_flow] == 100

    assert energy_balance.eb['Coking coal'][to_flow] == 0
    assert energy_balance.eb['Anthracite'][to_flow] == 11100


def test_swap_energy_with_deficit_and_backup_flow(energy_balance):
    from_flow = 'Gross electricity production - autoproducer electricity only'
    to_flow = 'Final consumption - industry sector - chemical and petrochemical - energy use'
    backup_flow = 'Some other flow'

    energy_balance.add_row_with_energy(backup_flow, {'Coking coal': 900}, total=False)

    # Trying to swap 10000 Anth for Coal when there is only 9900 Coal available
    energy_balance.swap_energy(
        from_flow,
        to_flow,
        ['Anthracite'],['Coking coal'],
        backup_flow=backup_flow
    )

    assert energy_balance.eb['Coking coal'][from_flow] == 15000
    assert energy_balance.eb['Anthracite'][from_flow] == 0

    assert energy_balance.eb['Coking coal'][to_flow] == 0
    assert energy_balance.eb['Anthracite'][to_flow] == 11100

    # And the remaining 100 should be swapped with the backup flow
    assert energy_balance.eb['Coking coal'][backup_flow] == 800
    assert energy_balance.eb['Anthracite'][backup_flow] == 100

def test_swap_energy_with_deficit_and_backup_flow_that_has_defict(energy_balance):
    from_flow = 'Gross electricity production - autoproducer electricity only'
    to_flow = 'Final consumption - industry sector - chemical and petrochemical - energy use'
    backup_flow = 'Some other flow'

    energy_balance.add_row_with_energy(backup_flow, {'Coking coal': 50}, total=False)

    # Trying to swap 10000 Anth for Coal when there is only 9900 Coal available in to_flow,
    # and only 50 in backup
    energy_balance.swap_energy(
        from_flow,
        to_flow,
        ['Anthracite'],['Coking coal'],
        backup_flow=backup_flow
    )

    assert energy_balance.eb['Coking coal'][from_flow] == 14950
    assert energy_balance.eb['Anthracite'][from_flow] == 50

    assert energy_balance.eb['Coking coal'][to_flow] == 0
    assert energy_balance.eb['Anthracite'][to_flow] == 11100

    # And the remaining 100 should be swapped with the backup flow
    assert energy_balance.eb['Coking coal'][backup_flow] == 0
    assert energy_balance.eb['Anthracite'][backup_flow] == 50


def test_negative_products(energy_balance):
    negative_flow = 'Some flow with negative values'
    energy_balance.add_row_with_energy(negative_flow, {'Coking coal': -50, 'Anthracite': 20}, total=False)

    neg = energy_balance.all_negative_products(negative_flow)
    assert 'Coking coal' in neg
    assert not 'Anthracite' in neg
    assert neg['Coking coal'] == 50


def test_load_from_world_balance():
    path = 'tests/fixtures/SG.csv'

    eb = EnergyBalance.from_world_balance_file(2019, 'SG', path)

    assert 'Transformation input - electricity and heat generation - energy use' in eb.eb.index
    assert  eb.all_negative_products('Transformation output - electricity and heat generation - main activity producer electricity only')
