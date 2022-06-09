from .base import HeatConverter

class HeatersConverter(HeatConverter):

    def conversion(self, heaters, heat_networks=None):
        '''
        Adds all heaters to the Energy Balance and to the Heat Network

        Params:
            heaters (List[Producer]):       List of heaters that should be added
            heat_networks (HeatNetworks):   The heat network to track the generated heat
        '''
        for producer in heaters:
            heat_output = self.process_producer(producer, is_chp=False)
            heat_networks.add_producer(producer, heat_output)

