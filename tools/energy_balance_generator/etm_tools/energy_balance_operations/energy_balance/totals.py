class Totals():
    def calculate_total(self, flow):
        '''Sets the Total column to the sum of all other columns'''
        self.eb['Total'][flow] = self.eb.loc[flow].sum() - self.eb['Total'][flow]

    def recalculate_totals(self, flows):
        '''Recalculate the Total columns of all given flows'''
        for flow in flows:
            self.calculate_total(flow)
