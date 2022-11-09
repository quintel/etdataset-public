import pandas as pd

class Lookup():
    '''Extravagant lookups adn calculations'''

    def sum(self, flow, products):
        '''Sum of the products in the flow'''
        return self.eb[products].loc[flow].sum()

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
            total = self.sum(flow, products)
            share_to_shift = amount_to_shift / total if total else 0.0

        if safe_guard == 'nonnegative' and share_to_shift > 1.0:
            self.warn_change(amount_to_shift, flow, products,
                self.sum(flow, products))
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
            product_shares[product] = Lookup.safe_division(
                self.eb[product][subflow], self.eb[product][main_flow])

        return product_shares

    def all_negative_products(self, flow) -> dict:
        '''
        Return a dict of all negative products and their values.
        Takes the absolute value to make the values positive.
        '''
        sel_flow = self.eb.loc[flow]
        return sel_flow[sel_flow < 0].abs().to_dict()

    def match_index(self, regex):
        '''Generator'''
        return (item for item in self.eb.index.tolist() if regex.match(item))

    def has_flow(self, flow):
        return flow in self.eb.index

    @staticmethod
    def safe_division(arg_1, arg_2):
        if arg_2 == 0:
            return 0

        return arg_1 / arg_2
