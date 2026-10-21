from fastapi import APIRouter

class Route_Test2:
    
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/test2", self.get_test, methods=["GET"])

    def get_test(self):
        return {'data': 'TEST2'}