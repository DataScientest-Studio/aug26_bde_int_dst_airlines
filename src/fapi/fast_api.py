from fastapi import FastAPI
from .test_api import Route_Test
from .test_api2 import Route_Test2

class FAPI: 
    """Core FastAPI application wrapper.

    Initializes the FastAPI instance and registers all application routers.
    """
    
    def __init__(self):
        """Initialize the FastAPI app and register API routes."""
        self.app = FastAPI()

        # List of all route handler instances to be registered
        router_list = [
            Route_Test(),
            Route_Test2()
        ]

        # Register each router with the FastAPI application instance
        for router in router_list:
            self.app.include_router(router)

