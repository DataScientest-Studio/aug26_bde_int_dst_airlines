import logging
import sys
import os

from src.data.common.airports import load_airports
from src.data.common.storage import save_json
from src.data.openweather_api import OpenWeatherAPI

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    stream=sys.stdout)

logger = logging.getLogger(__name__)

def retrieve_current_weather(openweather_client, airport_icao, airport):
    logger.info("Starting collection | airport=%s", airport_icao)

    payload = openweather_client.getCurrentState(airport["latitude"], airport["longitude"])
    
    filepath = save_json(provider="openweather", resource="current", airport_code=airport_icao, data=payload)
    
    logger.info(
        "SUCCESS | airport=%s | file=%s",
        airport_icao,
        filepath
    )

def main():
    failures = []
    client = OpenWeatherAPI()

    for icao, airport in load_airports().items():
        try:
            retrieve_current_weather(openweather_client=client, airport_icao=icao, airport=airport)
        except Exception as exc:
            #logger.exception("FAILED | airport=%s", icao)
            logger.error(
                "FAILED | airport=%s | error_type=%s",
                icao,
                type(exc).__name__
            )
            failures.append(icao)

    if failures:
        logger.error("Collection finished with failures: %s", failures)
        sys.exit(1)

    logger.info("Collection completed successfully")

if __name__ == "__main__":
    main()
