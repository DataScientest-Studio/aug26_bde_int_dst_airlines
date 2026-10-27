from src.utils.api import API
from src.utils.env_loader import load_env_var
from src.utils.exception_handling_decorator import exception_handling

class OpenWeatherAPI:

    def __init__(self):
        self.api_key = load_env_var("OPENWEATHER_API_KEY")
        self.url = "https://api.openweathermap.org/data"

    @exception_handling
    def getOpenWeatherAPI(self, urlpart, queryparams):
        queryparams = {**queryparams, "appid": self.api_key}
        url = self.url + urlpart
        data = API(url).call('GET', params=queryparams)
        return data

    def getCurrentState(self, latitude, longitude):
        queryparams={
            "lat": latitude, "lon": longitude, "units": "metric"
            }
        data = self.getOpenWeatherAPI("/2.5/weather", queryparams=queryparams)
        return data
