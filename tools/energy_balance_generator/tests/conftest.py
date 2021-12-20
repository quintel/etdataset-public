from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import pytest
import pandas as pd

from etm_tools.energy_balance_operations.energy_balance import EnergyBalance

@pytest.fixture
def energy_balance():
    '''
    Small dummy version of the energy balance:
                                                                                 Electricity  Coking coal  Anthracite  Total
    Final consumption - industry sector - chemical and petrochemical - energy use     0       9900         1200        10100
    Gross electricity production - autoproducer electricity only                      0       5000         10000       15000
    '''
    return EnergyBalance(
        pd.DataFrame(
            [[0,9900,1200,10100],[0,5000,10000,15000]],
            columns=['Electricity', 'Coking coal', 'Anthracite', 'Total'],
            index=[
                'Final consumption - industry sector - chemical and petrochemical - energy use',
                'Gross electricity production - autoproducer electricity only']
        ), 2019, 'EU_27')
