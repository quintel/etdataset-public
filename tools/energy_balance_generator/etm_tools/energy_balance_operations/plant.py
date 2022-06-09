'''This is a docstringless mess I'm sorry!'''

class Plant():
    def __init__(self, name, network='industrial', fuel=[], backup_flh=None):
        self.name = name
        self.network = network
        self.fuel = fuel
        self.backup_flh = backup_flh
        self.use_backup = False


    def input(self):
        if len(self.fuel) == 1:
            return self.fuel[0]

        return self.fuel


    @classmethod
    def from_chp(cls, row, network):
        '''Returns a Plant based on a line from the inputs CHPs file'''
        return cls(row['Name'], network, fuel=row['Fuel'].split(' and '), backup_flh=row['Backup full load hours'])


class Producer(Plant):
    def __init__(self, name, network, fuel=[], kind='heater', resindential_plant=None,
        industrial_plant=None, metadata={}):
        super().__init__(name, network, fuel)
        self.residential_plant = resindential_plant
        self.industrial_plant = industrial_plant
        self.kind = kind
        self.metadata = metadata


    def name_for(self, network):
        if network == 'residential':
            if self.residential_plant:
                return self.residential_plant.name

            return f'{self.name} - residential'

        if network == 'industrial':
            if self.industrial_plant:
                return self.industrial_plant.name

            return f'{self.name} - industrial'

        return self.name


    def subplant(self, network):
        if network == 'residential':
             return self.residential_plant
        if network == 'industrial':
            return self.industrial_plant


    def subplants(self):
        '''Yields tuples of network and subplant'''
        if self.residential_plant:
            yield ('residential', self.residential_plant)
        if self.industrial_plant:
            yield ('industrial', self.industrial_plant)


    def has_subplants(self):
        return self.residential_plant and self.industrial_plant


    def has_subplants_with_different_fuels(self):
        if self.has_subplants():
            return self.residential_plant.fuel != self.industrial_plant.fuel

        return False


    def subplants_shared_fuel(self):
        '''NOTE: Only the first fuel is returned'''
        if not self.has_subplants():
             return ''
        for f in (set(self.industrial_plant.fuel) & set(self.residential_plant.fuel)): return f


    def subplants_fuel_diff(self):
        '''NOTE: Only the first fuel is returned'''
        if not self.has_subplants():
            return ''
        for f in (set(self.industrial_plant.fuel) - set(self.residential_plant.fuel)): return f


    def turn_on_backup_flh(self):
        '''Set use_backup property to True for all subplants'''
        for _, plant in self.subplants():
            plant.use_backup = True


    def has_subplant_with_backup_on(self):
        for _, plant in self.subplants():
            if plant.use_backup:
                return True

        return False


    def first_subplant(self):
        '''Unordered. Returns first subplant. Handy if there is only one.'''
        for _, plant in self.subplants(): return plant


    @classmethod
    def from_dict(cls, producer):
        '''Returns a Producer based on a line in the yaml file'''
        return cls(producer['name'], producer['network'], [producer['input']], producer['type'])
