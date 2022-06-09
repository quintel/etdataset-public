from etm_tools.energy_balance_operations.converters import IndustryMetalConverter

def ready_energy_balance_for_metal_conversions(eb):
    # Make sure all requested products are in the dummy EB
    for product in (IndustryMetalConverter.ELECTRICITY_PRODUCTS +
        IndustryMetalConverter.NETWORK_GAS_PRODUCTS +
        IndustryMetalConverter.COAL_GAS_PRODUCTS):
        if not product in eb.eb.columns:
            eb.eb[product] = 0

    # Add neccesary flows to the dummy EB
    for flow in [IndustryMetalConverter.TO_CO, IndustryMetalConverter.TO_BF]:
         eb.add_row_with_energy(flow, {'Natural gas': 100, 'Biogases': 1000, 'Electricity': 9000})

    eb.add_row_with_energy(IndustryMetalConverter.IND_NON_FER_MET,
        {'Natural gas': 5000, 'Biogases': 10000})




def test_conversion(energy_balance):
    ready_energy_balance_for_metal_conversions(energy_balance)

    inputs = {
        'demand_aluminium_electricity_energetic': 0,
        'demand_aluminium_network_gas_energetic': 7500,
    }

    IndustryMetalConverter.convert(energy_balance, **inputs)

    # New row was created
    assert IndustryMetalConverter.IND_MET_ALU in energy_balance.eb.index

    assert energy_balance.eb['Natural gas'][IndustryMetalConverter.IND_MET_ALU] == 2500
