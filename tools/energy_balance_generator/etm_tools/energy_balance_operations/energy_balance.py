import pandas as pd
from etm_tools.utils import EurostatAPI
from .input_files import Translation

class EnergyBalance:
    def __init__(self, eb, year, area):
        self.eb = eb
        self.year = year
        self.area = area


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


    def add_empty_row(self, name):
        '''Add an empty row to the energy balance, with optional flow translation code'''
        self.append(pd.Series(0, index=self.eb.columns).rename(name))


    def calculate_total(self, flow):
        '''Sets the Total column to the sum of all other columns'''
        self.eb['Total'][flow] = self.eb.loc[flow].sum() - self.eb['Total'][flow]


    def recalculate_totals(self, flows):
        '''Recalculate the Total columns of all given flows'''
        for flow in flows:
            self.calculate_total(flow)


    def sum(self, flow, products):
        '''Sum of the products in the flow'''
        return self.eb[products].loc[flow].sum()


    def append(self, row):
        '''Extends pd.DataFrame.append'''
        self.eb = self.eb.append(row)


    def rename(self, old_flow_name, new_flow_name):
        '''Rename a flow'''
        self.eb.rename(index={old_flow_name: new_flow_name}, inplace=True)


    def remove(self, flow):
        '''Delete a flow'''
        self.eb.drop(flow, axis='index', inplace=True)


    def to_csv(self, path):
        '''Exports the EB to a csv is a nice human readable format'''
        self.eb.to_csv(path)


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


    def shift_energy(self, from_flows, to_flows, product_amounts, safe_guard='nonnegative'):
        '''
        Shift amounts (TJ) of energy from flows to other flows.

        Params:
            from_flows (str | list[str]):      The flows where the energy should be taken from
            to_flows (str | list[str]):        The flows where the energy should be moved to
            product_amounts (Dict[str,float]): Dictionary containing the amount of
                                               energy to be shifted per product in TJ
            safeguard ('nonnegative' | None):  What safeguard should be applied to the shifting
        '''
        if isinstance(from_flows, str): from_flows = [from_flows]
        if isinstance(to_flows, str): to_flows = [to_flows]

        if safe_guard == 'nonnegative':
            self._adjust_for_nonegative(from_flows, product_amounts)

        self._shift(from_flows, product_amounts, direction='take')
        self._shift(to_flows, product_amounts, direction='give')

        self.recalculate_totals(from_flows + to_flows)


    def product_amounts_proportionate(self, flow, products, amount_to_shift=None,
        share_to_shift=None, safe_guard='nonnegative'):
        '''
        Calculate a product_amounts Dictionay based on the products in an existing flow,
        and the amount_to_shift amount or the share_to_shift, these new product amounts should sum
        to.

        Params:
            amount_to_shift (float): Amount to shift from flow (TJ), to be spread over the products.
                                     You can only enter one of amount_to_shift or share_to_shift.
            share_to_shift (float):  Factor of the flow to shift (between 0 and 1), to be spread
                                     over the products

        Returns:
            Dict[str, float]: product amounts that can be used to shift
        '''
        if amount_to_shift is not None and not share_to_shift:
            total = self.eb[products].loc[flow].sum()
            share_to_shift = amount_to_shift / total if total else 0.0

        if safe_guard == 'nonnegative' and share_to_shift > 1.0:
            EnergyBalance.warn_change(amount_to_shift, flow, products,
                self.eb[products].loc[flow].sum())
            share_to_shift = 1.0

        return {product: self.eb[product][flow] * share_to_shift for product in products}


    def all_product_amounts_proportionate(self, flow, demand_per_product_group):
        '''TODO: write docstring'''
        all_product_amounts = {}
        for amount_to_shift, products in demand_per_product_group.items():
            all_product_amounts.update(
                self.product_amounts_proportionate(flow, products, amount_to_shift=amount_to_shift))

        return all_product_amounts


    def share_to_tj(self, flows=[], share=1.0, products=[], merge_products=False):
        '''
        Calculates the total amount of TJ based on a share, for the given products
        and flows. The energy in the products in these flows is summed to a total,
        of which the share is returned.

        Params:
            flows (str|list[str]):       Names of the flows or flow
            share (float):               Share to be calculated
            products (list[str]):        List of products of which to calculate the total TJ
            merge_products (True|False): If set to True, the energy of products is summed, before
                                         share is calculated. This results in a returned float.
                                         Else the products are kept apart in a dict.

        Returns:
            float | Dict[str,float]: The total amount of energy in TJ, or the amount of energy
                                     in TJ per product.
        '''
        if merge_products:
            return self.eb[products].loc[flows].sum().sum() * share

        return (self.eb[products].loc[flows].sum() * share).to_dict()


    def product_shares_to_tj(self, flow, product_shares):
        '''Turn product_shares dict into product_amounts dict based on a flow'''
        return self.eb[product_shares.keys()].loc[flow].mul(pd.Series(product_shares)).to_dict()


    def calculate_share_in_flow(self, subflow, main_flow):
        '''Returns a dict with (product: share of subflow in main flow) of all products in the EB'''
        product_shares = {}
        for product in self.eb.columns:
            product_shares[product] = EnergyBalance.safe_division(
                self.eb[product][subflow], self.eb[product][main_flow])

        return product_shares


    def _adjust_for_nonegative(self, flows, product_amounts):
        '''
        Lowers the amounts shifted to 100% of original when the original value will become negative

        Params:
            flows(list[str]):                  Energy balance flows that need to be adjusted
            product_amounts(Dict[str, float]): The amount of energy (TJ) that should
                                               be shifted per product.
        '''
        for flow in flows:
            for product, amount in product_amounts.items():
                if self.eb[product][flow] - amount < 0:
                    EnergyBalance.warn_change(amount, flow, product, self.eb[product][flow])
                    product_amounts[product] = self.eb[product][flow]


    def _shift(self, flows, product_amounts, direction='take', duplicate=True):
        '''
        Duplicates each flow and shifts energy for all products in the given direction

        Params:
            flows( list[str]):                  Energy balance flows that need to be adjusted
            product_amounts (Dict[str, float]): The amount of energy (TJ) that should
                                                be shifted per product.
            direction ('take' | 'give'):        'take' removes the energy from the flow, 'give'
                                                adds the energy to the flow
            duplicate (True|False):             If True, duplicates the row before altering
        '''
        for flow in flows:
            if duplicate:
                self.duplicate_row(flow)
            for product, amount in product_amounts.items():
                if direction == 'take':
                    self.eb[product][flow] -= amount
                elif direction == 'give':
                    self.eb[product][flow] += amount


    @classmethod
    def from_csv(cls, path):
        '''Sets up an EnergyBalance from an Eurostat energy balance csv file'''
        frame = pd.read_csv(path, index_col=['FLOWS','PRODUCTS'],
            usecols=['FLOWS', 'PRODUCTS','OBS_VALUE', 'geo', 'TIME_PERIOD'])

        cls.validate_eb(frame)
        area, year = cls.handle_area_and_year(frame)

        frame = frame.reset_index().pivot('FLOWS','PRODUCTS','OBS_VALUE').fillna(0.0)

        return cls(frame, year, area)


    @classmethod
    def from_eurostat(cls, country, year, eb_type='energy_balance'):
        '''
        Download an EB file for the given country and year from Eurostat, and
        convert it to an EnergyBalance
        '''
        trnsl = Translation.load(eb_type=eb_type)

        # Download into dataframe
        frame = pd.read_csv(
            EurostatAPI().get_csv(country, csv_type=eb_type, year=year),
            index_col=['nrg_bal', 'siec'],
            usecols=['nrg_bal', 'siec', 'OBS_VALUE', 'geo', 'TIME_PERIOD'])

        # Remove unwanted countries
        frame = frame[frame['geo']==country]

        # Validation
        cls.validate_eb(frame)
        area, year = cls.handle_area_and_year(frame)

        # Put it the human readable format: pivot into table view, fill in the translations
        frame = frame.reset_index().pivot('nrg_bal','siec','OBS_VALUE').fillna(0.0)
        frame.rename(
            columns=trnsl.product_translation(),
            index=trnsl.flow_translation(),
            inplace=True)
        frame = frame.reindex(
            columns=trnsl.unique('Product names'),
            index=trnsl.unique('Flows names'),
            fill_value=0.0)

        return cls(frame, year, area)


    @staticmethod
    def handle_area_and_year(raw_eb):
        '''Reads area and year from a raw energy balance frame and removes the columns afterwards'''
        area = raw_eb['geo'].unique()[0]
        year = raw_eb['TIME_PERIOD'].unique()[0]
        raw_eb.drop(['geo', 'TIME_PERIOD'], axis='columns', inplace=True)

        return area, year


    @staticmethod
    def validate_eb(raw_eb):
        '''Make sure the data is for one year and one area only'''
        EnergyBalance.raise_for_not_unique(raw_eb, 'geo')
        EnergyBalance.raise_for_not_unique(raw_eb, 'TIME_PERIOD')


    @staticmethod
    def raise_for_not_unique(raw_eb, column):
        if len(raw_eb[column].unique()) > 1:
            raise InvalidEnergyBalanceException(
                f'Column {column} in the Energy Balance must contain the same value for all rows.')


    @staticmethod
    def warn_change(amount_wanted, flow, product, amount_possible):
        print(f'\033[93mCould not move full amount of {amount_wanted} TJ from {flow} {product},',
              f'limiting the shift to {amount_possible} TJ\033[0m')


    @staticmethod
    def extract_translations(original_df, tr_from, tr_to):
        return original_df.reset_index().set_index(tr_from)[tr_to].to_dict()


    @staticmethod
    def safe_division(arg_1, arg_2):
        if arg_2 == 0:
            return 0

        return arg_1 / arg_2

class InvalidEnergyBalanceException(BaseException):
    pass
