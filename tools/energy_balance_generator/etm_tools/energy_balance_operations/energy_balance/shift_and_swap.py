class ShiftAndSwap():
    '''Shift and swap energy between rows'''

    def shift_energy(self, from_flows, to_flows, product_amounts, safe_guard='nonnegative',
        dup=True, totals=True):
        '''
        Shift amounts (TJ) of energy from flows to other flows.

        Params:
            from_flows (str | list[str]):      The flows where the energy should be taken from
            to_flows (str | list[str]):        The flows where the energy should be moved to
            product_amounts (Dict[str,float]): Dictionary containing the amount of
                                               energy to be shifted per product in TJ
            safeguard ('nonnegative' | None):  What safeguard should be applied to the shifting
            dup (True|False):                  Should flows be duplicated before shifting
            totals (True|False):               If True, the totals column will be recalculated
        '''
        if isinstance(from_flows, str): from_flows = [from_flows]
        if isinstance(to_flows, str): to_flows = [to_flows]

        if safe_guard == 'nonnegative':
            self._adjust_for_nonegative(from_flows, product_amounts)

        self._shift(from_flows, product_amounts, direction='take', duplicate=dup)
        self._shift(to_flows, product_amounts, direction='give', duplicate=dup)

        if totals: self.recalculate_totals(from_flows + to_flows)

    def shift_negative_energy(self, from_flow, to_flow):
        '''
        Shift negative amounts (TJ) of energy from flow to other flow as positive energy.

        Params:
            from_flows (str):      The flows where the energy should be taken from
            to_flows (str):        The flows where the energy should be moved to
        '''
        product_amounts = self.all_negative_products(from_flow)

        self._shift([from_flow], product_amounts, direction='give', duplicate=False)
        self._shift([to_flow], product_amounts, direction='give', duplicate=False)

        self.recalculate_totals([from_flow, to_flow])

    def swap_energy(self, from_flow, to_flow, from_products, to_products, backup_flow=''):
        '''
        Swap the energy in from_products in the form_flow with energy with energy
        from the to_products in the to_flow. E.g. Move all the Oil in the from_flow to
        the to_flow, in exchange for the to_flow's Naturual Gas.
        If there is not enough of the to_products to swap, the swap is limited to the
        available amount. When a backup flow is specified, the remaining product will
        be (tried to be) swapped with that flow.

        Params:
            from_flow(str):             The flow the 'from_products' energy is taken from.
            to_flow(str):               The flow that will recieve toe 'from_porducts' energy
                                        in exchange for energy in the 'to_products'
            from_products(List[str]):   The products that should be emptied in the from_flow
            to_products(List[str]):     The products that compensate for that emptied energy
        '''
        move_energy = self.share_to_tj(from_flow, products=from_products, merge_products=True)
        max_shift = self.sum(to_flow, to_products)
        backup_needed = False

        if max_shift < move_energy:
            if not backup_flow:
                self.warn_swap_overload(max_shift, from_flow, to_flow, from_products, to_products)
            backup_needed = True
            move_energy = max_shift

        # Shift 'from_products' away
        self.shift_energy(from_flow, to_flow,
            self.product_amounts_proportionate(
                from_flow, from_products, amount_to_shift=move_energy
            ),
            dup=False, totals=False
        )

        # Shift 'to_products' back
        self.shift_energy(to_flow, from_flow,
            self.product_amounts_proportionate(
                to_flow, to_products, amount_to_shift=move_energy
            ),
            dup=False, totals=False
        )

        if backup_flow and backup_needed:
            self.swap_energy(from_flow, backup_flow, from_products, to_products)

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
                    self.warn_change(amount, flow, product, self.eb[product][flow])
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
