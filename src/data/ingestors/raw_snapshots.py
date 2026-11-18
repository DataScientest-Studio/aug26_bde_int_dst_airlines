import json
import sys
import logging
import psycopg2
from datetime import datetime, timezone

from src.databases.databases import Database
from src.data.common.storage import BASE_DIR

# format of raw jsons
FILENAME_FORMAT = "%Y-%m-%dT%H%M%S%fZ"

# limit for the number of raw jsons (per airport) processed in one batch
DEFAULT_BATCH_SIZE = 20

# logging: similar to collectors
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    stream=sys.stdout
)

logger = logging.getLogger(__name__)


# get the paths to all files in folder
def discover_raw_files():
    return sorted(
        path for path in BASE_DIR.rglob("*.json") if path.is_file()
    )


def get_raw_file_path(path):
    return path.relative_to(BASE_DIR).as_posix()


# retrive the paths of already registered files from db
def fetch_registered_raw_file_paths(db):
    rows = db.execute_sql(
        """
        select raw_file_path
        from ingestion.raw_snapshot;
        """
    )

    return {row["raw_file_path"] for row in rows}


# 
def select_unregistered_files(files, registered_paths, max_files_per_provider_airport):
    # we treat each combination (provider, airport) as separate stream
    # we'll try to register new raw jsons evenly across streams
    files_by_stream = {}

    # traverse the files list, skip already registered
    for path in files:
        raw_file_path = get_raw_file_path(path)

        if raw_file_path in registered_paths:
            continue

        # extract the key (provider, airport) from path
        relative_path = path.relative_to(BASE_DIR)
        provider = relative_path.parts[0]
        airport_icao = relative_path.parts[-2].removeprefix("airport=")

        stream_key = (provider, airport_icao)
        files_by_stream.setdefault(stream_key, []).append(path)

    selected_files = []

    # sorted: filenames start with timestamp, so we process old files first
    for stream_key in sorted(files_by_stream):
        stream_files = sorted(
            files_by_stream[stream_key],
            key=lambda path: (path.name, get_raw_file_path(path))
        )

        # follow the limit of files per batch
        if max_files_per_provider_airport is not None:
            stream_files = stream_files[:max_files_per_provider_airport]

        selected_files.extend(stream_files)

    return selected_files


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

def run_raw_snapshot_registration(max_files_per_provider_airport=DEFAULT_BATCH_SIZE):
    files = discover_raw_files()

    inserted_count = 0
    concurrent_existing_count = 0
    failures = []
  
    with Database() as db:
        # already processed are fetched from db
        registered_paths = fetch_registered_raw_file_paths(db)

        # total number of files yet to be processed
        unregistered_count = sum (
            get_raw_file_path(path) not in registered_paths
            for path in files)

        # files to be processed in current batch
        files_to_process = select_unregistered_files(
            files, registered_paths, max_files_per_provider_airport)

        # remaining for future batches
        deferred_count = unregistered_count - len(files_to_process)

        logger.info("Starting raw-snapshot registration | discovered=%s | "
                    "already_registered=%s | selected=%s | deferred=%s", 
                    len(files), len(files) - unregistered_count, len(files_to_process), deferred_count)

        for path in files_to_process:
            try:
                snapshot_id, inserted = process_raw_file(db, path)

                if inserted:
                    inserted_count += 1
                    logger.info("REGISTERED | snapshot_id=%s | file=%s", 
                                snapshot_id, get_raw_file_path(path))
                else:
                    # in case there is a concurrent process that has already registered the file
                    # (shouldn't happen normally with scheduled batches) 
                    concurrent_existing_count += 1
                    logger.info("ALREADY REGISTERED | snapshot_id=%s | file=%s", 
                                snapshot_id, get_raw_file_path(path))

            except (json.JSONDecodeError, psycopg2.Error, OSError):
                logger.exception("FAILED | file=%s", get_raw_file_path(path))
                failures.append(path)

        logger.info("Raw-snapshot registration complete | discovered=%s | "
                    "registered=%s | already_registered=%s | deferred=%s | failed=%s",
                    len(files), inserted_count, len(files) - unregistered_count + concurrent_existing_count, deferred_count,  len(failures))

    return {
        'discovered': len(files),
        'registered': inserted_count,
        'already_registered': (len(files) - unregistered_count + concurrent_existing_count),
        'selected': len(files_to_process),
        'deferred': deferred_count,
        'failed': len(failures)
    }


def main():
    result = run_raw_snapshot_registration()

    if result['failed']:
        sys.exit(1)


if __name__ == "__main__":
    main()
