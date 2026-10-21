from fastapi import APIRouter

class Route_Test:
    
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/test", self.get_test, methods=["GET"])

    def get_test(self):
        return {'data': 'TEST'}