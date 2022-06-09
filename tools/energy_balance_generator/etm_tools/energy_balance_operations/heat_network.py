
class HeatNetworks():
    '''Holds a bunch of heat networks'''
    def __init__(self, industry_consumption, residential_consumption):
        self.industrial_network = Network(industry_consumption)
        self.residential_network = Network(residential_consumption)
        self.unassigned_producers = []
        self.unassigned_heat = 0.0


    def add_producer(self, producer, heat):
        '''
        Assigns a producer to one of the networks

        Params:
            producer (dict[str,str]): A producer as listed in the heaters_and_chp config
            heat (float):             Amount of heat produced in TJ
        '''
        if producer.network == 'residential':
            self.residential_network.add(heat)
        elif producer.network == 'industrial':
            self.industrial_network.add(heat)
        else:
            self.unassigned_producers.append(producer)
            self.unassigned_heat += heat


    def assign_flexible_producers(self):
        '''
        Generates tuples of producer, sector and the share of energy to shift to that sector
        '''
        share_for_ind, share_for_res = self.calculate_shares()

        for producer in self.unassigned_producers:
            yield (producer, 'residential', share_for_res)
            yield (producer, 'industrial', share_for_ind)


    def calculate_shares(self):
        '''
        Calculates the shares in which the flexible producers should be split up according to the
        deficits in the heat networks.
        When the shares can't be calculated, a 50/50 split is returned.

        Returns:
            (float, float): The share of flexible heat to go to industry, and the share to go to
                            residential.
        '''
        if not self.unassigned_heat:
            return (0.5, 0.5)

        share_for_res = self.residential_network.deficit() / self.unassigned_heat
        share_for_ind = self.industrial_network.deficit() / self.unassigned_heat

        if share_for_res == 0.0 and share_for_ind == 0.0:
            return (0.5, 0.5)

        if not share_for_res + share_for_ind == 1.0:
            share_for_ind, share_for_res = HeatNetworks.warn_rescale(share_for_ind, share_for_res)

        return (share_for_ind, share_for_res)


    @staticmethod
    def warn_rescale(share_one, share_two):
        '''Returns a tuple of the rescaled shares (they should now sum to 1.0)'''
        print('\033[93mUnassigned heat from flexible producers does not match heat deficit in ' +
            f'Final Consumption ({round(share_one + share_two, 2) * 100}%)\033[0m')

        return (share_one / (share_one + share_two), share_two / (share_one + share_two))


class Network():
    '''Represents a heat network for e.g. residential or industry'''

    def __init__(self, heat_consumption=0.0):
        self.heat_supply = 0.0
        self.heat_consumption = heat_consumption


    def add(self, heat_supply):
        self.heat_supply += heat_supply


    def deficit(self):
        deficit = self.heat_consumption - self.heat_supply
        return deficit if deficit >= 0 else 0
