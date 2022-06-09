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
    SOLAR_PV_FLH_KEY ='input_solar_panels_roofs_and_parks_full_load_hours'

    SOLAR_THERMAL_KEYS = [
        'input_energy_heat_solar_thermal_production'
    ]
    SOLAR_THERMAL_FLH_KEY ='energy_heat_solar_thermal_full_load_hours'
    
    WIND_KEYS = [
       'input_energy_power_wind_turbine_inland_production',
       'input_energy_power_wind_turbine_coastal_production'
    ]
    
    WIND_OFFSHORE_KEYS = [
       'input_energy_power_wind_turbine_offshore_production'
    ]
    WIND_OFFSHORE_FLH_KEY ='energy_power_wind_turbine_offshore_full_load_hours'
    
    WIND_ONSHORE_KEYS = [
       'input_energy_power_wind_turbine_inland_production'
    ]
    WIND_ONSHORE_FLH_KEY ='energy_power_wind_turbine_inland_full_load_hours'
    
    WIND_COASTAL_KEYS = [
       'input_energy_power_wind_turbine_coastal_production'
    ]
    WIND_COASTAL_FLH_KEY ='energy_power_wind_turbine_coastal_full_load_hours'

    def __init__(self):
        '''Crappy class to get some data from the DatasetManager'''

    def get_value(self, area, key, extra_key=None):
        '''
        Get the value for the key or keys for the given area

        Params:
            area(str):          The ETLocal area key
            key(str|list[str]): The ETLocal key or keys to get the value from. If a list
                                is given, the values are summed
        '''
        response = requests.get(f'{self.BASE_URL}/api/v1/exports/{area}')

        if response.ok:
            data = response.json()[0]
            if isinstance(key, list):
                main_value = sum((data[single_key] for single_key in key))
            else:
                main_value = data[key]

            return main_value, data.get(extra_key, None) if extra_key else main_value

        raise APIError(f'Etlocal returned an error: {response.status_code}, {response.json()}')

    def get_solar_pv(self, area, get_flh=False):
        return self.get_value(area, self.SOLAR_PV_KEYS, extra_key=self.SOLAR_PV_FLH_KEY if get_flh else None)

    def get_solar_thermal(self, area, get_flh=False):
        return self.get_value(area, self.SOLAR_THERMAL_KEYS, extra_key=self.SOLAR_THERMAL_FLH_KEY if get_flh else None)

    def get_wind_coastal(self, area, get_flh=False):
        return self.get_value(area, self.WIND_COASTAL_KEYS, extra_key=self.WIND_COASTAL_FLH_KEY if get_flh else None)

    def get_wind_offshore(self, area, get_flh=False):
        return self.get_value(area, self.WIND_OFFSHORE_KEYS, extra_key=self.WIND_OFFSHORE_FLH_KEY if get_flh else None)

    def get_wind_onshore(self, area, get_flh=False):
        return self.get_value(area, self.WIND_ONSHORE_KEYS, extra_key=self.WIND_ONSHORE_FLH_KEY if get_flh else None)

    def get_wind_production(self, area, get_flh=False):
        return self.get_value(area, self.WIND_KEYS)

class APIError(BaseException):
    ''' Api error'''
