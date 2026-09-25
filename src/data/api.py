import requests
from typing import Literal

HTTPMethod = Literal["GET", "POST", "PUT", "DELETE"]

class API:
    def __init__(self, url: str):
        self.url = url
    
    def call(self, method: HTTPMethod = "GET", headers=None, params=None):
        if method == 'GET':
            res = requests.get(self.url, headers = headers, params = params)

            if res.status_code == 200:
                return res.json()
            else: 
                return {
                    "Error": res.text
                }
        elif method == 'POST':
            return {
                "Error": 'NYI'
            }
        elif method == 'PUT':
            return {
                "Error": 'NYI'
            }
        elif method == 'DELETE':
            return {
                "Error": 'NYI'
            }
        else:
            return {
                "Error": f"Unsupported method: {method}"
            }

    
    
