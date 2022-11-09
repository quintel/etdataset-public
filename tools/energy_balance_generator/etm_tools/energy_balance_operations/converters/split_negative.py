import re
from .base import Converter

class SplitNegativeConverter(Converter):
    MARK = 'world'

    SPECIAL_CASES = {
        'Transformation output - electricity and heat generation - other sources':
            'Transformation input - electricity and heat generation - derived heat for electricity production',
        'Transformation output - electricity and heat generation - pumped hydro':
            'Transformation input - electricity and heat generation - electricity for pumped storage',
        'Transformation output - blended in natural gas':
            'Transformation input - for blended natural gas - energy use'
    }

    def conversion(self, match, sub, sub_for, second_sub='output', second_sub_for='intake'):
        for output_flow in self.index_match(match):
            input_flow = re.sub(sub, sub_for, output_flow, count=1)
            if second_sub:
                input_flow = re.sub(second_sub, second_sub_for, input_flow, count=1)

            if not self.energy_balance.has_flow(input_flow):
                if self.energy_balance.has_flow(input_flow + ' - energy use'):
                    input_flow += ' - energy use'
                elif output_flow in self.SPECIAL_CASES:
                    input_flow = self.SPECIAL_CASES[output_flow]
                else:
                    self.energy_balance.add_empty_row(input_flow)

            self.energy_balance.shift_negative_energy(output_flow, input_flow)

    def index_match(self, keyword):
        '''Generating the flows to be shifted to'''
        yield from self.energy_balance.match_index(re.compile(keyword))
