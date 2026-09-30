import requests
from typing import Literal

HTTPMethod = Literal["GET", "POST", "PUT", "DELETE"]

class API:
    def __init__(self, url: str):
        self.url = url
    
    def call(self, method: HTTPMethod = "GET", headers=None, params=None):
        if method == 'GET':
            try: 
                res = requests.get(self.url, headers = headers, params = params)
                
                # Throw Error if API status = 4xx or 5xx
                res.raise_for_status()

                return res.json()

            except requests.exceptions.RequestException as err:
                raise Exception(f"[API-ERROR] {err.response.json()}")
        elif method == 'POST':
            raise NotImplementedError(f"{method}: NYI")
        elif method == 'PUT':
            raise NotImplementedError(f"{method}: NYI")
        elif method == 'DELETE':
            raise NotImplementedError(f"{method}: NYI")
        else:
            raise Exception(f"Unsupported method: {method}")

    
    
