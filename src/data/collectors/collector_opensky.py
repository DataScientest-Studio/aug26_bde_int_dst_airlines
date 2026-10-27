import logging
import sys

from src.data.common.airports import load_airports
from src.data.common.storage import save_json
from src.data.opensky_api import OpenSkyAPI

logging.basicConfig(
	level=logging.INFO, 
	format="%(asctime)s | %(levelname)s | %(message)s", 
	stream=sys.stdout)

logger = logging.getLogger(__name__)


def retrieve_states(opensky_client, airport_icao, airport):
  logger.info("Starting collection | airport=%s", airport_icao)

  payload = opensky_client.getStates(airport["opensky_bbox"])
  
  filepath = save_json(provider="opensky", resource="states", airport_code=airport_icao, data=payload)

  logger.info(
	"SUCCESS | airpot=%s | state_count=%s | file=%s",
	airport_icao,
	len(payload.get("states") or []),
	filepath
  )


def main():
  failures = []
  client = OpenSkyAPI()

  for icao, airport in load_airports().items():
    try:
      retrieve_states(opensky_client=client, airport_icao=icao, airport=airport)
    except Exception as e:
      logger.exception("FAILED | airport=%s", icao)
      failures.append(icao)

  if failures:
    logger.error("Collection finished with failures: %s", failures)
    sys.exit(1)

  logger.info("Collection completed successfully")

if __name__ == "__main__":
  main()

