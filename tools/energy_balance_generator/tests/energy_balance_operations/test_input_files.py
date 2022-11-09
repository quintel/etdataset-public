from etm_tools.energy_balance_operations.input_files import EBConfig

TR = {'energy_balance': {
    'products': [
        'Oil shale and oil sands',
        'Aviation gasoline',
    ], 'flows': [
        'Transformation output - blast furnaces',
        'Transformation output - gas works',
    ]}}


def test_translation():
    tr = EBConfig(TR, eb_type='energy_balance')

    # Keeps order
    flow_tr = tr.flow_translation()
    assert flow_tr[list(flow_tr.keys())[0]] == 'Transformation output - blast furnaces'
    assert flow_tr[list(flow_tr.keys())[1]]  == 'Transformation output - gas works'

    # Get all keys
    assert 'Oil shale and oil sands' in tr.all('products')
    assert 'Aviation gasoline' in tr.all('products')
    assert len(tr.all('products')) == 2

    assert 'TO_GW' in tr.all_codes('flows')


def test_translation_from_config():
    tr = EBConfig.load('config/eurostat.yml', eb_type='crude_oil')

    assert 'O4100_TOT' in tr.product_translation()
    assert 'FC_IND_CPC_NE' in tr.flow_translation()
