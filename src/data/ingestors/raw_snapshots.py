import json
import sys
import logging
import psycopg2
from datetime import datetime, timezone
from pathlib import Path

from src.databases.databases import Database
from src.data.common.storage import BASE_DIR

# format of raw jsons
FILENAME_FORMAT = "%Y-%m-%dT%H%M%S%fZ"

# logging: similar to collectors
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    stream=sys.stdout
)

logger = logging.getLogger(__name__)


def discover_raw_files():
    return sorted(
        path for path in BASE_DIR.rglob("*.json") if path.is_file()
    )

def parse_raw_file_metadata(path):
    relative_path = path.relative_to(BASE_DIR)
    parts = relative_path.parts

    # provider/resource/.../airport=EDDB/file.json
    if len(parts) < 4:
        raise ValueError(f"Unexpected raw-file path: {relative_path}")
    
    provider = parts[0]
    resource = "/".join(parts[1:-2]) # relative depth may be more than 1

    airport_directory = parts[-2]
    if not airport_directory.startswith("airport="):
        raise ValueError(f"Missing airport directory: {relative_path}")

    airport_icao = airport_directory.removeprefix("airport=")
    if len(airport_icao) != 4:
        raise ValueError(f"Invalid ICAO airport code: {airport_icao}")

    try:
        collected_at = datetime.strptime(path.stem, FILENAME_FORMAT).replace(tzinfo=timezone.utc)
    except ValueError as exc:
        raise ValueError(
            f"Unexpected timestamp filename: {path.name}"
        ) from exc

    return {
        "provider": provider,
        "resource": resource,
        "airport_icao": airport_icao,
        "collected_at": collected_at,
        "raw_file_path": relative_path.as_posix()
    }

def load_payload(path):
    with path.open(encoding="utf-8") as file:
        return json.load(file)

# insertion of raw json into ingestion.raw_snapshot
def register_snapshot(db, metadata, payload):
    query = """
        insert into ingestion.raw_snapshot (
            provider,
            resource,
            airport_icao,
            collected_at,
            raw_file_path,
            payload
        )
        values (%s, %s, %s, %s, %s, %s)
        on conflict (raw_file_path) do nothing
        returning snapshot_id;
    """

    params = (
        metadata['provider'],
        metadata['resource'],
        metadata['airport_icao'],
        metadata['collected_at'],
        metadata['raw_file_path'],
        psycopg2.extras.Json(payload)
    )

    rows = db.execute_sql(query, params)

    # if inserted a new row
    if rows:
        return rows[0]['snapshot_id'], True

    # if this raw file already registered
    existing_rows = db.execute_sql(
        """
        select snapshot_id
        from ingestion.raw_snapshot
        where raw_file_path = %s;
        """,
        (metadata['raw_file_path'],)
    )

    return existing_rows[0]['snapshot_id'], False

# per-file processing: if db insert fails, we roll back for one file
def process_raw_file(db, path):
    metadata = parse_raw_file_metadata(path)
    payload = load_payload(path)

    with db.dbconnection:
        snapshot_id, inserted = register_snapshot(db, metadata, payload)

    return snapshot_id, inserted

def main():
    files = discover_raw_files()

    inserted_count = 0
    existing_count = 0
    failures = []

    logger.info("Starting raw-snapshot registration | files=%s", len(files))

    with Database() as db:
        for path in files:
            try:
                snapshot_id, inserted = process_raw_file(db, path)

                if inserted:
                    inserted_count += 1
                    logger.info("REGISTERED | snapshot_id=%s | file=%s", snapshot_id, path.relative_to(BASE_DIR))
                else:
                    existing_count += 1
                    logger.info("ALREADY REGISTERED | snapshot_id=%s | file=%s", snapshot_id, path.relative_to(BASE_DIR))

            except psycopg2.Error:
                logger.exception("FAILED | file=%s", path.relative_to(BASE_DIR))
                failures.append(path)

        logger.info("Raw-snapshot registration complete | discovered=%s | inserted=%s | already_registered=%s | failed=%s",
                    len(files), inserted_count, existing_count, len(failures))

        if failures:
            sys.exit(1)

if __name__ == "__main__":
    main()
