from src.utils.api import API

class OpenSkyAPI:

    def __init__(self):
        self.url = 'https://opensky-network.org/api'

    def getOpenSkyAPI(self, urlpart, queryparams):
        url = self.url + urlpart
        data = API(url).call('GET', params=queryparams)
        return data

    def getStates(self, bbox):
        queryparams = bbox
        data = self.getOpenSkyAPI('/states/all', queryparams=queryparams)
        return data