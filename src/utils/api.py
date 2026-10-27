import requests
from typing import Literal

HTTPMethod = Literal["GET", "POST", "PUT", "DELETE"]

class APIRequestError(RuntimeError):
    """A request was made but no usable API response was obtained."""

class API:
    def __init__(self, url: str):
        self.url = url
    
    def call(self, method: HTTPMethod = "GET", headers=None, params=None):
        if method == 'GET':
            try: 
                res = requests.get(self.url, headers = headers, params = params, timeout=30)
                
                res.raise_for_status()

            # we'll distinguish error levels:
            # request executed unsuccessfully, 
            # request failed, 
            # request returned unexpected object
            except requests.exceptions.HTTPError as exc:
                status_code = (
                    exc.response.status_code
                    if exc.response is not None
                    else "unknown"
                    )
                raise APIRequestError(
                    f"[API returned an unsuccessfull HTTP status: {status_code}]"
                ) from exc

            except requests.exceptions.RequestException as exc:
                raise APIRequestError(
                    f"[API request failed: {type(exc).__name__}]"
                    ) from exc

            try:
                return res.json()

            except requests.exceptions.JSONDecodeError as exc:
                raise APIRequestError(
                    "[API returned a successfull HTTP response but not valid JSON]"
                ) from exc
            
        elif method == 'POST':
            raise NotImplementedError(f"{method}: NYI")
        elif method == 'PUT':
            raise NotImplementedError(f"{method}: NYI")
        elif method == 'DELETE':
            raise NotImplementedError(f"{method}: NYI")
        else:
            raise Exception(f"Unsupported method: {method}")

    
    
