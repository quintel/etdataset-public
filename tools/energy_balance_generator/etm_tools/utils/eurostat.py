import requests
import io

from etm_tools.energy_balance_operations.input_files import Translation

BASE_URL = 'https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/'

class EurostatAPI():

    def __init__(self):
        pass


    def get_csv(self, country_codes, csv_type='energy_balance', year=2019):
        '''
        Returns a String IO object containing the downloaded energybalance

        Params:
            country_codes (str|list[str]): The country codes you want to download the EB for
            csv_type (str):                The type of download requested from Eurostat, can be
                                           any of 'energy_balance', 'fossil_fuels', 'oil_products'
                                           or 'network_gas'
            year (int):                    The year for which to download the CSV

        Returns:
            StringIO object containing the requested csv download from Eurostat
        '''
        eb_setting = Translation.load(eb_type=csv_type)
        flows = EurostatAPI.join(eb_setting.unique("Flows codes"))
        products = EurostatAPI.join(eb_setting.unique("Product codes"))


        return self._handle_response(self._request(
            eb_setting.eurostat_code(),
            f'{flows}.{products}',
            eb_setting.unit(),
            country_codes,
            {'startPeriod': year, 'endPeriod': year}
        ))


    def _request(self, key, options, unit, country_codes, params):
        country_codes = EurostatAPI.join(country_codes)
        params['format'] = 'SDMX-CSV'
        return requests.get(f'{BASE_URL}{key}/A.{options}.{unit}.EU27_2020+{country_codes}', params=params)


    def _handle_response(self, response):
        '''Return StringIO obect of returned csv (from request) if the request was successful'''
        if response.ok:
            return io.StringIO(response.content.decode("utf-8"))

        # TODO: this can be nicer
        raise SystemExit(f'Could not connect to Eurostat ({response.content})')


    @staticmethod
    def join(codes):
        if not isinstance(codes, str):
            codes = '+'.join(codes)

        return codes
