from fastapi import FastAPI
from .test_api import Route_Test
from .test_api2 import Route_Test2
from .routers.get_airport_list import Get_Airport_List
from .routers.get_flight_summary import Get_Flight_Summary
from .routers.get_flight import Get_Flight
from .routers.get_flight_list import Get_Flight_List

class FAPI: 
    """Core FastAPI application wrapper.

    Initializes the FastAPI instance and registers all application routers.
    """

    def __init__(self):
        """Initialize the FastAPI app and register API routes."""
        self.app = FastAPI()

        # List of all route handler instances to be registered
        router_list = [
            Route_Test().router,
            Route_Test2().router,
            Get_Airport_List().router,
            Get_Flight_Summary().router,
            Get_Flight().router,
            Get_Flight_List().router
        ]

        # Register each router with the FastAPI application instance
        for router in router_list:
            self.app.include_router(router)

