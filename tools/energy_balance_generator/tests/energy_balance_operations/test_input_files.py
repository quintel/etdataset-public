from etm_tools.energy_balance_operations.input_files import Translation

TR = {'energy_balance': {
    'products': {
        '04600': 'coal',
        'R2A4536': 'natural gas with kerosene'
    }, 'flows': {
        'FD_NE': 'Final demand - non energy',
        'FD_E': 'Final demand - energy only'
    }}}


def test_translation():
    tr = Translation(TR, eb_type='energy_balance')

    # Keeps order
    flow_tr = tr.flow_translation()
    assert flow_tr[list(flow_tr.keys())[0]] == 'Final demand - non energy'
    assert flow_tr[list(flow_tr.keys())[1]]  == 'Final demand - energy only'

    # Get all keys
    assert 'coal' in tr.unique('Product names')
    assert 'natural gas with kerosene' in tr.unique('Product names')
    assert len(tr.unique('Product names')) == 2


def test_translation_from_config():
    tr = Translation.load('config/eurostat.yml', eb_type='crude_oil')

    assert 'O4100_TOT' in tr.product_translation()
    assert 'FC_IND_CPC_NE' in tr.flow_translation()
