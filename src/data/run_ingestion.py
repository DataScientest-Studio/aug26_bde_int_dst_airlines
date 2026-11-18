import logging
import sys

from src.data.ingestors.raw_snapshots import (
    run_raw_snapshot_registration
)

from src.data.ingestors.openweather import (
    run_openweather_normalisation
)

from src.data.ingestors.opensky import (
    run_opensky_normalisation
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger(__name__)


def pipeline_has_failures(results):
    return any(result['failed'] > 0 for result in results.values())


def run_ingestion_pipeline():
    stages = (
        ("raw_snapshot_registration", run_raw_snapshot_registration),
        ("openweather_normalisation", run_openweather_normalisation),
        ("opensky_normalisation", run_opensky_normalisation)
    )

    results = {}

    logger.info("Starting ingestion pipeline")

    for stage_name, run_stage in stages:
        logger.info("Starting stage | stage=%s", stage_name)

        result = run_stage()
        results[stage_name] = result

        logger.info("Stage complete | stage=%s | result=%s",
                    stage_name, result)

    logger.info("Ingestion pipeline complete | failed=%s",
                pipeline_has_failures(results))

    return results


def main():
    results = run_ingestion_pipeline()

    if pipeline_has_failures(results):
        sys.exit(1)


if __name__ == "__main__":
    main()