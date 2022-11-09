from etm_tools.utils.conversion_map import ConversionMap, SourceAnalysis

def test_conversion():
    cm = ConversionMap()

    inputs = cm.inputs('industry_chemical', 'AT')

    assert 'demand_fertilizers_network_gas_energetic' in inputs
    assert inputs['demand_fertilizers_network_gas_energetic'] > 0


def test_all_keyword():
    cm = ConversionMap()

    a_param = {
        'file': 'source_analyses_output/chemical_non_energetic_shares_network_gas_analysis',
        'file_type': 'compact',
        'field': 'ALL'}

    val = cm.lookup_value(a_param, 'AT')

    assert isinstance(val, dict)

    assert len(val.keys()) > 1

def test_source_analysis():
    sa = SourceAnalysis('source_analyses_input/input_industry_metal_aluminium', 2019)

    val = sa.get('industry_aluminium_production', 'ES', value='Value')
    assert val == 0.22

    all = sa.get('ALL', 'ES', value='Value')
    assert isinstance(all, dict)
    assert 'industry_aluminium_production' in all

    list_vals = sa.get(['industry_aluminium_production'], 'ES', value='Value')
    assert isinstance(list_vals, dict)
    assert 'industry_aluminium_production' in list_vals
