from .api import API
from src.utils.env_loader import load_env_var
from src.utils.exception_handling_decorator import exception_handling

class CiriumSkyAPI:

    def __init__(self):
        self.app_key = load_env_var("CIRIUMSKY_API_APPKEY")
        self.app_id = load_env_var("CIRIUMSKY_API_APPID")

    @exception_handling
    def getCiriumSkyAPI(self, urlpart, queryparams):
        headers={
            'Authorization': self.app_key,
            'Accept':'application/json'
        }
        
        url = "https://api.sky.cirium.com/" + urlpart
        data = API(url).call('GET', headers=headers, params=queryparams)
        return data

    def getAirlines(self, only_active=False):
        queryparams={"onlyActive": only_active}
        data = self.getCiriumSkyAPI("v1/airlines", queryparams=queryparams)
        print(data)
        
    def getAirports(self, only_active=False):
        queryparams={"onlyActive": only_active}
        data = self.getCiriumSkyAPI("v1/airports", queryparams=queryparams)
        print(data)