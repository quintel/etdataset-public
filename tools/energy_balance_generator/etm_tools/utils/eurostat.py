import requests
import io
import pandas as pd

BASE_URL = 'https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/'

class EurostatAPI():
    # We have some codes in the config that can't be passed to the API - If the API gives an error like:
    # "The following values for dimension are not allowed: NRG_BAL=FC_IND_CPC_NE, SIEC=E8000, SIEC=O4200",
    # add the relevant codes to the array below for exclusion.
    EXCLUDED_CODES = ['FC_IND_CPC_NE']

    def __init__(self):
        pass


    def get_csv(self, country_codes, csv_type='energy_balance', year=2019):
        '''
        Returns a String IO object containing the downloaded energybalance

        Params:
            country_codes (str|list[str]): The country codes you want to download the EB for
            csv_type (str):                The type of download requested from Eurostat, can be
                                           any of 'energy_balance', 'fossil_fuels', 'oil_products'
                                           or 'gas'
            year (int):                    The year for which to download the CSV

        Returns:
            StringIO object containing the requested csv download from Eurostat
        '''
        from etm_tools.energy_balance_operations.input_files import EBConfig
        eb_setting = EBConfig.load(eb_type=csv_type)

        return self._handle_response(self._request(
            eb_setting.europe_code(),
            self._create_options(eb_setting, csv_type),
            country_codes,
            {'startPeriod': year, 'endPeriod': year}
        ))

    def _request(self, key, options, country_codes, params):
        country_codes = EurostatAPI.join(country_codes)
        params['format'] = 'SDMX-CSV'
        return requests.get(f'{BASE_URL}{key}/A.{options}.{country_codes}', params=params)


    def _handle_response(self, response):
        '''Return StringIO obect of returned csv (from request) if the request was successful'''
        if response.ok:
            return io.StringIO(response.content.decode("utf-8"))

        raise SystemExit(f'Could not connect to Eurostat ({response.content})')


    def _create_options(self, eb_setting, csv_type):
        '''Returns the options string'''
        flows = EurostatAPI.join(EurostatAPI.exclude_invalid_codes(list(eb_setting.all_codes("flows"))))
        products = EurostatAPI.join(EurostatAPI.exclude_invalid_codes(list(eb_setting.all_codes("products"))))

        if csv_type == 'chps':
            plants = EurostatAPI.join(list(eb_setting.all("plants")))
            efficiencies = EurostatAPI.join(list(eb_setting.all("efficiencies")))
            return '.'.join([eb_setting.unit(), flows, plants, products, efficiencies])

        return '.'.join([flows, products, eb_setting.unit()])


    @staticmethod
    def join(codes):
        if not isinstance(codes, str):
            codes = '+'.join(codes)

        return codes

    @staticmethod
    def exclude_invalid_codes(codes):
        """
        Filters out any codes present in the EXCLUDED_CODES list.
        """
        return [str(code).strip() for code in codes if isinstance(code, str) and str(code).strip() not in EurostatAPI.EXCLUDED_CODES]
