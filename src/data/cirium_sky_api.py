from .api import API
from src.utils.env_loader import load_env_var
from src.utils.exception_handling_decorator import exception_handling

class CiriumSkyAPI:

    def __init__(self):
        self.app_token = load_env_var("CIRIUMSKY_API_APPKEY")
        self.app_id = load_env_var("CIRIUMSKY_API_APPID")

    @exception_handling
    def getCiriumSkyAPI(self, urlparam: str):
        headers={
            'Authorization': self.app_token,
            'Accept':'application/json'
        }

        url = "https://api.sky.cirium.com/" + urlparam
        data = API('https://api.sky.cirium.com/v1/airlines/').call('GET', headers=headers)
        print(data)