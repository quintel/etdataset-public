import pandas as pd
from .plant import Producer, Plant
from etm_tools.utils.utils import cached_property

class CHPProducers():
    '''Wraps the chp inputs csv in the data folder and makes them into Plants and Producers'''

    # Special treatment
    BIO_ICE = 'Biogas CHP'
    COAL_GAS_PLANT = 'Coal gas CHP'

    GAS_BASED_CHPS = ['Internal Combustion CHP', 'Gas Turbine CHP', 'Combined Cycle CHP']

    def __init__(self, frame):
        self.frame = frame


    @classmethod
    def from_csv(cls, path):
        return cls(pd.read_csv(path, index_col=['Gen Tech', 'Network']))


    @cached_property
    def gas_based_chps(self):
        return [self._gas_based_producer(tech) for tech in self.GAS_BASED_CHPS]


    @cached_property
    def steam_turbine_chps(self):
        return [steam_turbine_producer(fuel, producer) for fuel, producer in
            self.frame.loc['Steam Turbine CHP'].groupby('Fuel')]


    ## Individual Producers ----------------------------------------------------
    @cached_property
    def biogas_chp(self):
        '''
        NOTE: Hard-Coded as just a residential plant!

        Returns: Producer (Biogas CHP)
        '''
        producer_row = self.frame[self.frame['Name'] == self.BIO_ICE]

        return Producer(
            self.BIO_ICE,
            'residential',
            resindential_plant=plant(
                producer_row,
                'Residential'
            ),
            fuel=['Biogas'],
            metadata={'flh': producer_row['Full load hours'].values[0]}
        )


    @cached_property
    def coal_gas_chp(self):
        '''
        NOTE: Hard-Coded as just an industrial plant!

        Returns: Producer (Coal gas CHP)
        '''
        producer_row = self.frame[self.frame['Name'] == self.COAL_GAS_PLANT]

        return Producer(
            self.COAL_GAS_PLANT,
            'industrial',
            industrial_plant=plant(
                producer_row,
                'Industrial'
            ),
            fuel=producer_row['Fuel'].to_list(),
            metadata={'flh': producer_row['Full load hours'].values[0]}
        )


    ## Private -----------------------------------------------------------------
    def _gas_based_producer(self, tech):
        efficiencies = self.frame[self.frame['Fuel'] != 'Biogas']

        return Producer(
            tech,
            network(efficiencies.loc[tech]),
            resindential_plant=plant(efficiencies.loc[tech], network='Residential'),
            industrial_plant=plant(efficiencies.loc[tech], network='Industrial'),
            fuel=['Gas', 'Oil'],
            metadata={
                 # We get the mean of residential and industrial efficiency
                'efficiency': efficiencies.loc[tech]['Electrical efficiency'].mean()
            }
        )


## Static methods --------------------------------------------------------------

def steam_turbine_producer(fuel, producer):
    '''Based on a gruopby, works slightly different than the gas based ones'''
    return Producer(
        name_for_steam_turbine(producer, fuel),
        network(producer),
        resindential_plant=plant(producer, network='Residential'),
        industrial_plant=plant(producer, network='Industrial'),
        fuel=[fuel]
    )


def plant(producers, network='Industrial'):
    '''
    Producers is a slice from the efficiencies frame containing one or two plants,
    depending on if the producer can be either a residential or industrial plant, or both
    '''
    try:
        return Plant.from_chp(producers.loc[network], network.lower())
    except KeyError:
        return None


def network(producers):
    networks = producers.index.unique().to_list()
    return networks[0].lower() if len(networks) == 1 else 'flexible'


def name_for_steam_turbine(producer, fuel):
    '''
    Producers is a slice from the efficiencies frame containing one or two plants,
    depending on if the producer can be either a residential or industrial plant, or both

    Returns: str (A name)
    '''
    if len(producer.index) == 1:
        return producer['Name'].values[0]
    return f'Steam Turbine CHP - {fuel}'
