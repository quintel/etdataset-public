import requests
import pandas as pd

class WeatherXAPI():
    API_URL = 'https://weather.appx.cloud/api/v2/weather/sources/knmi/models/uurgegevens'
    TRIES = 10

    def __init__(self, start, end):
        '''
        `start` - String date, eg '2019-01-01 00:00',
        `end` - String date, eg '2019-12-31 23:59'
        '''
        self.start = start
        self.end = end


    def get_dataframe(self, lat, lon, variables):
        '''
        Returns a dataframe containing hourly data for all given variables.
        `variables` - Array with factors that should be in the DataFrame, eg ['SUNR','WIND']
        `lat` - Latitude in either GPS of RD-coordinates, eg 52.1
        `lon` - Longitude in either GPS of RD-coordinates, eg 5.18
        '''
        payload = {
            'begin': self.start,
            'end': self.end,
            'lat': lat,
            'lon': lon,
            'factors': variables,
            'response_format': 'json',
            'units': 'original'
        }

        response = self.connect(payload)

        if response.ok:
            return self.__ensure_correct_dates(pd.DataFrame(response.json()[0]))

        raise APIError(
            f'Weather API returned an error. ' +
            f'Status {response.status_code} {response.reason}, message: {response.text}'
        )

    def __ensure_correct_dates(self, dataframe):
        '''Ensures all the requested dates are in the dataframes'''
        needed_times = pd.date_range(self.start, self.end, freq='H')
        dataframe['time'] = pd.to_datetime(dataframe['time'])
        return dataframe.set_index('time').reindex(needed_times).reset_index()

    def connect(self, payload):
        ''' Tries 10 times to connect to the API, returns the response if any, or raises an error'''
        for _ in range(self.TRIES):
            try:
                return requests.get(self.API_URL, params=payload, timeout=5)
            except requests.exceptions.Timeout:
                pass
            except requests.exceptions.ConnectionError:
                print('Having trouble connecting to Weather API...')

        raise APIError(f'Connection to Weather API timed out {self.TRIES} times')



class EtlocalAPI():
    BASE_URL = 'https://data.energytransitionmodel.com/'
    SOLAR_PV_KEYS = [
        'input_households_solar_pv_demand',
        'input_buildings_solar_pv_demand',
        'input_energy_power_solar_pv_solar_radiation_production'
    ]
    WIND_KEYS = [
       'input_energy_power_wind_turbine_inland_production',
       'input_energy_power_wind_turbine_coastal_production'
    ]

    def __init__(self
    ):
        '''Crappy class to get some data from the DatasetManager'''

    def get_solar_pv(self, area):
        '''Dit is echt heel omslachtig, excuus, maar er ligt een plan om de API aan te passen! '''
        area_id = self.get_area_id(area.split('_')[0])

        response = requests.get(f'{self.BASE_URL}/api/v1/exports/{area_id}')

        if response.ok:
            data = response.json()[0]
            return sum((data[key] for key in self.SOLAR_PV_KEYS))

        raise APIError(f'Etlocal returned an error: {response.status_code}, {response.json()}')

    def get_wind_production(self, area):
        area_id = self.get_area_id(area.split('_')[0])

        response = requests.get(f'{self.BASE_URL}/api/v1/exports/{area_id}')

        if response.ok:
            data = response.json()[0]
            return sum((data[key] for key in self.WIND_KEYS))

        raise APIError(f'Etlocal returned an error: {response.status_code}, {response.json()}')

    def get_area_id(self, area_geo_code):
        '''Get the dataset id of the area'''
        response = requests.get(f'{self.BASE_URL}/datasets/{area_geo_code}.json')
        if response.ok:
            if response.json():
                return response.json()['id']

            raise APIError(f'Could not get information from Etlocal about {area_geo_code}')

        raise APIError(f'Etlocal returned an error: {response.status_code}, {response.json()}')

class APIError(BaseException):
    ''' Api error'''
