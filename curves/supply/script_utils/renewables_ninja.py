'''Download and renewables.ninja data into pd Dataframes'''

import requests
import io
import pandas as pd

COUNTRY_MAP = { 'AT': "AT_austria", 'BE': "BE_belgium", 'BG': "BG_bulgaria", 'CY': "CY_cyprus",
    'CZ': "CZ_czechia", 'DE': "DE_germany", 'DK': "DK_denmark", 'EE': "EE_estonia",
    'ES': "ES_spain", 'FI': "FI_finland", 'FR': "FR_france", 'GB': 'UK_united_kingdom',
    'GR': "EL_greece", 'HR': "HR_croatia", 'HU': "HU_hungary", 'IE': "IE_ireland", 'IT': "IT_italy",
    'LT': "LT_lithuania", 'LU': "LU_luxembourg", 'LV': "LV_latvia", 'NL': "NL_netherlands",
    'PL': "PL_poland", 'PT': "PT_portugal", 'RO': "RO_romania", 'SE': "SE_sweden",
    'SI': "SI_slovenia", 'SK': "SK_slovakia", 'NO': 'NO_norway', 'CH': 'CH_switzerland',
    'RS': 'RS_serbia'}


class RenewablesNinja():

    BASE_URL = 'https://www.renewables.ninja/'

    # Params for coordinates use
    BASE_PARAMS = {
        'dataset': 'merra2',
        'format': 'csv',
        'capacity': 1,
        'header': False
    }

    PV_PARAMS = {
        'system_loss': 0.1,
        'tracking': 0,
        'tilt': 35,
        'azim': 180
    }

    WEATHER_PARAMS = {}

    WIND_PARAMS = {
        'height': 100, # What to do here?
        'turbine': 'Vestas V150 4000' # PICK ONE!! enercon6500
    }

    def __init__(self, year, coordinates={}, countries=[]):
        '''
        You can supply either coordinates:
            {'region_key': {'lat': 30, 'lon': 50}, ...}
        Or a list of countries:
            ['AT', 'BE', ...]
        depending on which endpoint you want to use.
        '''
        self.coordinates = coordinates
        self.countries = countries
        self.year = year


    def get_pv_from_coordinates(self, country):
        '''
        Returns a pd.DataFrame of the PV curve from the API', using the coordinates endpoint.
        '''
        return self._handle_response(
            self._request_with_coordinates('pv', self.PV_PARAMS, country))


    def get_pv_from_country(self, country):
        '''
        Returns a pd.DataFrame of the PV curve from the API, using the countries endpoint.
        '''
        merra_file = f'ninja_pv_country_{country}_merra-2_corrected.csv'

        return self._handle_response(self._request_merra_file(country, merra_file))


    def get_all_pv(self):
        '''
        Returns a generator going over all countries or coordinates
        Picks countries if set, else tries going over all keys in the coordinates.
        '''
        if self.countries:
            for country in self.countries:
                yield COUNTRY_MAP.get(country, country), self.get_pv_from_country(country)
        else:
            for country in self.coordinates:
                yield COUNTRY_MAP.get(country, country), self.get_pv_from_coordinates(country)


    def get_wind_curves_from_coordinates(self, country):
        '''
        Returns a pd.DataFrame of the Wind curve from the API, using the coordinates endpoint.
        '''
        return self._handle_response(
            self._request_with_coordinates('wind', self.WIND_PARAMS, country))


    def get_wind_curves_from_country(self, country):
        '''
        Returns a pd.DataFrame of the Wind curve from the API, using the countries endpoint.
        '''
        merra_file = f'ninja_wind_country_{country}_current-merra-2_corrected.csv'

        return self._handle_response(self._request_merra_file(country, merra_file))


    def get_all_wind_curves(self):
        '''
        Returns a generator going over all countries or coordinates
        Picks countries if set, else tries going over all keys in the coordinates.
        '''
        if self.countries:
            for country in self.countries:
                yield COUNTRY_MAP.get(country, country), self.get_wind_curves_from_country(country)
        else:
            for country in self.coordinates:
                yield COUNTRY_MAP.get(country, country), self.get_wind_curves_from_coordinates(country)


    def get_weather_curves_from_coordinates(self, country):
        '''
        Returns a pd.DataFrame of the Wind curve from the API, using the coordinates endpoint.
        '''
        return self._handle_response(
            self._request_with_coordinates('weather', self.WEATHER_PARAMS, country))


    def get_weather_curves_from_country(self, country):
        '''
        Returns a pd.DataFrame of the Wind curve from the API, using the countries endpoint.
        '''
        merra_file = f'ninja_weather_country_{country}_merra-2_land_area_weighted.csv'

        return self._handle_response(self._request_merra_file(country, merra_file))


    def get_all_weather_curves(self):
        '''
        Returns a generator going over all countries or coordinates
        Picks countries if set, else tries going over all keys in the coordinates.
        '''
        if self.countries:
            for country in self.countries:
                yield COUNTRY_MAP.get(country, country), self.get_weather_curves_from_country(country)
        else:
            for country in self.coordinates:
                yield COUNTRY_MAP.get(country, country), self.get_weather_curves_from_coordinates(country)


    def _request_with_coordinates(self, endpoint, extra_params, country):
        '''Returns an API response'''
        params = self.BASE_PARAMS | self.coordinates[country] | self._date_params() | extra_params

        return requests.get(f'{self.BASE_URL}/api/data/{endpoint}', params=params)


    def _request_merra_file(self, country, merra_file):
        '''Returns an API response'''
        return requests.get(f'{self.BASE_URL}/country_downloads/{country}/{merra_file}')


    def _date_params(self):
        return {
            'date_from': f'{self.year}-01-01',
            'date_to': f'{self.year}-12-31',
        }


    def _handle_response(self, response):
        '''Return pd.Dataframe of returned csv (from request) if the request was successful'''
        if response.ok:
            if self.countries:

                # Intermediate export of wind curve since this function doesn't work properly anymore
                df = pd.read_csv(io.StringIO(response.content.decode("utf-8")), skiprows=2,
                    index_col=0, header=0, parse_dates=True)
                df.to_csv(f'wind_curve_output.csv')

                return pd.read_csv(io.StringIO(response.content.decode("utf-8")), skiprows=2,
                    index_col=0, header=0, parse_dates=True)[str(self.year)]

            return pd.read_csv(io.StringIO(response.content.decode("utf-8")))

        raise SystemExit(f'Could not connect to renewables.ninja ({response.content})')
