from .api import API
from src.utils.exception_handling_decorator import exception_handling
class OpenSkyAPI:

    def __init__(self):
        self.url = 'https://opensky-network.org/api'

    @exception_handling
    def getOpenSkyAPI(self, urlpart, queryparams):
        url = self.url + urlpart
        data = API(url).call('GET', params=queryparams)
        return data

    def getStates(self, bbox):
        queryparams = bbox
        data = self.getOpenSkyAPI('/states/all', queryparams=queryparams)
        return data