import pandas as pd

class Translation():
    def __init__(self, translations):
        self.trs = translations

    def translate_to(self, eb_type, filters=[]) -> dict:
        '''Translate to eurostat_code or world_code, optionally filter the translations'''
        return self._to_dict(self._reverse_index(eb_type, filters=filters))

    def _reverse_index(self, eb_type, filters=[]):
        return self._filter(eb_type, filters).reset_index().set_index(eb_type)

    def _filter(self, eb_type, filters):
        return self.trs[eb_type].loc[filters] if filters else self.trs[eb_type]

    def _to_dict(self, filtered_eb) -> dict:
        return list(filtered_eb.to_dict().values())[0]

    @classmethod
    def load(cls, path, index):
        return cls(pd.read_csv(path, index_col=0, usecols=[index, 'eurostat_code', 'world_code']))


flow_translations = Translation.load('config/flows.csv', 'Flow')
product_translations = Translation.load('config/products.csv', 'Product')
