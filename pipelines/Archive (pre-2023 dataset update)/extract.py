import requests
from json.decoder import JSONDecodeError
from pathlib import Path

import config.config as config


class PblService():
    """
    Setup a basic service to download the data files
    published by the PBL
    """
    def __init__(self, geo_id):
        self.geo_id = geo_id
        
    def call(self, file_type='xls'):
        if file_type == 'xls':
            path = Path(__file__).parents[1] / f"data" / "raw" / f"pbl_referentieverbruiken_{self.geo_id}.xlsx"
            response = requests.get(f"https://dataportaal.pbl.nl/downloads/VIVET/Referentieverbruik_warmte/Gemeentebestanden_XLS/gemeente_{self.geo_id}.xlsx",
                                    allow_redirects=True, stream=True)
        elif file_type == 'csv':
            path = Path(__file__).parents[1] / f"data" / "raw" / f"Data_{self.geo_id}.csv"
            response = requests.get(f"https://dataportaal.pbl.nl/downloads/VIVET/Referentieverbruik_warmte/Databestanden_gemeenten_CSV/Data_{self.geo_id}.csv",
                                    allow_redirects=True, stream=True)
            
        if response.status_code == 200:
            with open(path, 'wb') as f:
                f.write(response.content)
            f.close()
                    

class KlimaatmonitorService():
    """
    Setup a basic service to connect to Klimaatmonitor
    """
    def __init__(self):
        self.session = SessionWithUrlBase(
            url_base=config.BASE_URLS['KLIMAATMONITOR'], 
            api_key=config.API_KEYS['KLIMAATMONITOR'])

    def __call__(self, *args, **kwargs):
        raise NotImplementedError()

    @classmethod
    def execute(cls, *args, **kwargs):
        """
        Creates a new Service and executes it
        """
        service = cls()
        return service.__call__(*args, **kwargs)
    
    
class EpOnlineService():
    """
    Setup a basic service to connect to EP-Online
    """
    def __init__(self):
        self.session = SessionWithUrlBase(
            url_base=config.BASE_URLS['EP_ONLINE'], 
            api_key=config.API_KEYS['EP_ONLINE'])

    def __call__(self, *args, **kwargs):
        raise NotImplementedError()

    @classmethod
    def execute(cls, *args, **kwargs):
        """
        Creates a new Service and executes it
        """
        service = cls()
        return service.__call__(*args, **kwargs)
    
    
class QueryEnergyDemand(KlimaatmonitorService):
    """
    TODO
    """
    def __call__(self, var, geo_id, year):
        """
        var        str representing Klimaatmonitor variable code, e.g. 'gaswoningen_2019'
        geo_id     str representing the area for which the data should be collected, e.g. 'GM0363'
        year       str representing the year for which the data should be collected, e.g. 2019
        
        Returns json response
        """
        response = self.session.get(
            f"/Variables/('{var}')/GeoLevels('{geo_id}')/PeriodLevels('year')/Periods('{year}')/Values",
            # f"/Variables/({var})/GeoLevels({geo_id})/PeriodLevels('year')/Periods({year})/Values",
            headers={'Connection': 'close'}
        )
        
        # e.g. https://swing.eu/JiveServices/odata/Variables('bevtot')/GeoLevels('all')/PeriodLevels('year')/Periods('2019')/Values

        return self.__handle_response(response)

    
    def __handle_response(self, response):
        """
        Returns a service result, by which we can check later if it's a success or not
        """
        if response.ok:
            value = response.json()

            return ServiceResult.success(value)
        try:
            # Check if any errors are returned
            return ServiceResult.failure(response.json())
        except JSONDecodeError:
            return f"Klimaatmonitor returned a {response.status_code} error"
            # return ServiceResult.failure([f"Klimaatmonitor returned a {response.status_code}"])
    
    
class QueryEnergyLabel(EpOnlineService):
    """
    TODO
    """
    def __call__(self, bag_id):
        """
        bag_id    the building's BAG VBO (verblijfsobject) ID
        
        Returns json response
        """
        response = self.session.get(
            f"/PandEnergielabel/AdresseerbaarObject/{bag_id}",
            headers={'Connection': 'close'}
        )

        return self.__handle_response(response)

    
    def __handle_response(self, response):
        """
        Returns a service result, by which we can check later if it's a success or not
        """
        if response.ok:
            value = response.json()

            return ServiceResult.success(value)
        try:
            # Check if any errors are returned
            return ServiceResult.failure(response.json())
        except JSONDecodeError:
            return ServiceResult.failure([f"EP-Online returned a {response.status_code}"])

        
class SessionWithUrlBase(requests.Session):
    """
    Helper class to store the base url
    """

    def __init__(self, url_base=None, api_key=None, *args, **kwargs):
        super(SessionWithUrlBase, self).__init__(*args, **kwargs)
        self.url_base = url_base
        self.api_key = api_key
        

    def request(self, method, url, headers={}, **kwargs):
        modified_url = self.url_base + url
        
        # headers['Authorization'] = f"Bearer {self.api_key}"
        headers['apikey'] = f"{self.api_key}"

        return super(SessionWithUrlBase, self).request(
            method, modified_url, headers=headers, **kwargs)
    
    
class ServiceResult():
    """
    Used as an object returned by services, holds values and errors
    """
    def __init__(self, successful=True, errors=None, value=None):
        self.errors = errors
        self.value = value
        self.successful = successful

    @classmethod
    def failure(cls, errors=None):
        """
        Creates a new (success=False) instance, containing the errors (list-like)
        """
        return cls(successful=False, errors=errors)

    @classmethod
    def success(cls, value=None):
        """
        Creates a successfull ServiceResult with value as value
        """
        return cls(value=value)