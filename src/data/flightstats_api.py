from .api import API
from src.utils.env_loader import load_env_var

class FlightStatsAPI:

    def __init__(self):
        self.api_token = load_env_var("FLIGHTSTATS_API_TOKEN")

    def getFlightStatsAPI(self):
        header={
            'Authorization': self.api_token,
            'Accept':'application/json'
        }
        
        data = API('https://api.sky.cirium.com/v1/flights/status/airline/WQ/flight-number/123/departure-date/2026-08-23').call('GET', headers=header)
        print(data)