import pandas as pd

class Append():
    '''Append new rows to the EnergyBalance'''

    def append(self, row):
        '''Extends pd.DataFrame.append'''
        self.eb = self.eb.append(row)

    def add_empty_row(self, name):
        '''Add an empty row to the energy balance, with optional flow translation code'''
        self.append(pd.Series(0, index=self.eb.columns).rename(name))

    def duplicate_row(self, flow):
        '''
        Duplicate the flow and renames the duplicated row to 'original'.

        If the row did not yet exist, it will be created with all zero values instead
        of being duplicated.
        If the row was already dupicated, nothing will happen.
        '''
        if not flow in self.eb.index:
            self.add_empty_row(flow)
        elif not f'{flow} - original' in self.eb.index:
            self.append(self.eb.loc[flow].rename(f'{flow} - original'))

    def add_row_with_energy(self, flow, product_amounts, total=True):
        '''
        Creates a new flow with energy set as given by the product amounts.
        Fills up the total column accordingly.

        Params:
            flow (str):                        Name of the new flow to be added
            product_amounts (Dict[str,float]): Dictionary containing the amount of
                                               energy per product in TJ
            total (True|False):                If set to True, calculates the Total column
        '''
        if flow in self.eb.index:
            # TODO: add a warning here?
            return

        self.add_empty_row(flow)
        self._shift([flow], product_amounts, direction='give', duplicate=False)

        if total:
            self.calculate_total(flow)

    def add_row_from_diff(self, flow_one, flow_two, new_flow):
        '''Adds a new flow based on the difference between flow one and flow two'''
        new_data = (self.eb.loc[flow_one]- self.eb.loc[flow_two]).rename(new_flow)

        if (new_data < 0).values.any():
            print(f'\033[93mCorrecting negative values found by subtracting "{flow_one}" and ' +
                f'"{flow_two}"\033[0m')
            new_data[new_data < 0] = 0

        self.append(new_data)

    def add_row_from_share(self, flow, new_flow, share):
        '''
        Adds a new flow that is based on a share of another flow.
        For example: if share=0.5 the new flow wil copy 50% of the energy of the existing
        flow for each product. Note: no energy is shifted, you are making a copy.
        '''
        self.append((self.eb.loc[flow] * share).rename(new_flow))
