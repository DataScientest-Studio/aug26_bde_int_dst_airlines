import json
from psycopg2.extras import Json
from datetime import datetime, timezone
from pathlib import Path

from src.databases.databases import Database
from src.data.common.storage import BASE_DIR

FILENAME_FORMAT = "%Y-%m-%dT%H%M%S%fZ"

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
        Json(payload)
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
