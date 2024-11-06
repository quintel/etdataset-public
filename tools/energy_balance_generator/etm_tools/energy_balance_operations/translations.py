import pandas as pd

class Translation():
    def __init__(self, translations):
        self.trs = translations

    def translate_to(self, eb_type, filters=[]) -> dict:
        '''Translate to europe_code or world_code, optionally filter the translations'''
        return self._to_dict(self._reverse_index(eb_type, filters=filters))

    def _reverse_index(self, eb_type, filters=[]):
        return self._filter(eb_type, filters).reset_index().set_index(eb_type)

    def _filter(self, eb_type, filters):
        return self.trs[eb_type].loc[filters] if filters else self.trs[eb_type]

    def _to_dict(self, filtered_eb) -> dict:
        return list(filtered_eb.to_dict().values())[0]

    @classmethod
    def load(cls, path):
        df = pd.read_csv(path, usecols=['europe_label', 'europe_code', 'world_label'])  # Load only the relevant columns
        df.set_index('europe_label', inplace=True)  # Set europe_label as the index
        return cls(df)

flow_translations = Translation.load('config/flows_world_to_europe.csv')
product_translations = Translation.load('config/products_world_to_europe.csv')
