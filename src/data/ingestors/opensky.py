import logging
import sys
import psycopg2
from datetime import datetime, timezone

from src.databases.databases import Database


# default limit for files per batch for the module
DEFAULT_SNAPSHOT_BATCH_SIZE = 100


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger(__name__)


# from OpenSky docs:
POSITION_SOURCES = {0: "ADS_B", 1: "ASTERIX", 2: "MLAT", 3: "FLARM"}

# value indexes within state-vectors
ICAO24_INDEX = 0
CALLSIGN_INDEX = 1
ORIGIN_COUNTRY_INDEX = 2
TIME_POSITION_INDEX = 3
LAST_CONTACT_INDEX = 4
LONGITUDE_INDEX = 5
LATITUDE_INDEX = 6
BARO_ALTITUDE_INDEX = 7
ON_GROUND_INDEX = 8
VELOCITY_INDEX = 9
TRUE_TRACK_INDEX = 10
VERTICAL_RATE_INDEX = 11
GEO_ALTITUDE_INDEX = 13
SQUAWK_INDEX = 14
POSITION_SOURCE_INDEX = 16


# insert into public.aircraft or update its country
def upsert_aircraft(db, state_vector):
    aircraft_icao24 = state_vector[ICAO24_INDEX]
    origin_country = state_vector[ORIGIN_COUNTRY_INDEX]

    if not aircraft_icao24:
        raise ValueError("OpenSky state vector has no icao24")

    rows = db.execute_sql(
        """
        insert into public.aircraft (aircraft_icao24, origin_country)
        values (%s, %s)
        on conflict (aircraft_icao24) do update
        set origin_country = excluded.origin_country
        returning aircraft_icao24;
        """,
        (aircraft_icao24, origin_country)
    )

    return rows[0]['aircraft_icao24']


def upsert_position_source(db, source_code):
    if source_code is None:
        return None

    if source_code not in POSITION_SOURCES:
        raise ValueError(f"Unknown OpenSky position source code: {source_code}")

    rows = db.execute_sql(
        """
        insert into public.position_source (opensky_code, position_source_val)
        values (%s, %s)
        on conflict (opensky_code) do update
        set position_source_val = excluded.position_source_val
        returning position_source_id;
        """,
        (source_code, POSITION_SOURCES[source_code])
    )

    return rows[0]['position_source_id']


# no description of squawk codes supported here
def upsert_squawk(db, squawk_code):
    if squawk_code is None:
        return None

    squawk_code = squawk_code.strip()

    if len(squawk_code) != 4:
        raise ValueError(f"Invalid squawk value: {squawk_code}")

    db.execute_sql(
        """
        insert into public.squawk (squawk_id)
        values (%s)
        on conflict (squawk_id) do nothing;
        """,
        (squawk_code,)
    )

    return squawk_code

# select one raw json for processing
def fetch_next_pending_snapshot(db):
    rows = db.execute_sql(
        """
        select snapshot_id, airport_icao, collected_at, payload
        from ingestion.raw_snapshot
        where provider = %s
          and resource = %s
          and normalised_at is null
          and normalisation_error is null
        order by collected_at
        limit 1;
        """,
        ("opensky", "states"),
    )

    return rows[0] if rows else None


# convert Unix-timestamp to Postgres-compatible timestamp
def unix_timestamp_to_utc(value):
    if value is None:
        return None

    if not isinstance(value, (int, float)):
        raise ValueError(f"Invalid Unix timestamp: {value}")

    return datetime.fromtimestamp(value, tz=timezone.utc)


def get_source_observed_at(payload):
    source_observed_at = unix_timestamp_to_utc(payload.get("time"))

    if source_observed_at is None:
        raise ValueError("OpenSky payload has no valid 'time' value")

    return source_observed_at


# remove trailing spaces
def clean_callsign(value):
    if value is None:
        return None

    cleaned_value = value.strip()
    return cleaned_value or None


# process one state vector
def insert_flight_state(db, snapshot, state_vector):
    if len(state_vector) <= POSITION_SOURCE_INDEX:
        raise ValueError("OpenSky state vector is incomplete")

    if state_vector[ON_GROUND_INDEX] is None:
        raise ValueError("OpenSky state vector has no on_ground value")

    aircraft_icao24 = upsert_aircraft(db, state_vector)
    position_source_id = upsert_position_source(db, state_vector[POSITION_SOURCE_INDEX])
    squawk_id = upsert_squawk(db, state_vector[SQUAWK_INDEX])

    rows = db.execute_sql(
        """
        insert into public.flight_state(
            airport_icao,
            category_id, 
            squawk_id,
            position_source_id,
            aircraft_icao24,
            callsign,
            time_position,
            last_contact,
            latitude,
            longitude,
            baro_altitude,
            geo_altitude,
            on_ground,
            velocity,
            true_track,
            vertical_rate,
            created_at,
            snapshot_id
        )
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s)
        on conflict (snapshot_id, aircraft_icao24) do nothing
        returning flight_state_id;
        """,
        (
            snapshot["airport_icao"],
            None, # category is not availabel in (non-extended) current payloads
            squawk_id,
            position_source_id,
            aircraft_icao24,
            clean_callsign(state_vector[CALLSIGN_INDEX]),
            unix_timestamp_to_utc(state_vector[TIME_POSITION_INDEX]),
            unix_timestamp_to_utc(state_vector[LAST_CONTACT_INDEX]),
            state_vector[LATITUDE_INDEX],
            state_vector[LONGITUDE_INDEX],
            state_vector[BARO_ALTITUDE_INDEX],
            state_vector[GEO_ALTITUDE_INDEX],
            state_vector[ON_GROUND_INDEX],
            state_vector[VELOCITY_INDEX],
            state_vector[TRUE_TRACK_INDEX],
            state_vector[VERTICAL_RATE_INDEX],
            snapshot["collected_at"],
            snapshot["snapshot_id"]
        )
    )

    if rows:
        return rows[0]["flight_state_id"], True

    return None, False


# upd status of a snapshot in ingestion.raw_snapshot
def mark_snapshot_normalised(db, snapshot):
    source_observed_at = get_source_observed_at(snapshot['payload'])

    db.execute_sql(
        """
        update ingestion.raw_snapshot
        set source_observed_at = %s,
            normalised_at = now(),
            normalisation_error = null
        where snapshot_id = %s;
        """,
        (source_observed_at, snapshot["snapshot_id"])
    )


def mark_snapshot_failed(db, snapshot_id, error):
    error_message = f"{type(error).__name__}: {error}"

    db.execute_sql(
        """
        update ingestion.raw_snapshot
        set normalisation_error = %s
        where snapshot_id = %s;
        """,
        (error_message[:1000], snapshot_id)
    )

# process all aircrafts from one raw json
def normalise_opensky_snapshot(db, snapshot):
    state_vectors = snapshot['payload'].get('states')

    if state_vectors is None:
        state_vectors = []

    if not isinstance(state_vectors, list):
        raise ValueError("OpenSky payload has an invalid 'states'")

    inserted_count = 0
    existing_count = 0

    for state_vector in state_vectors:
        if not isinstance(state_vector, list):
            raise ValueError("OpenSky payload contains an invalid state vector")

        _, inserted = insert_flight_state(db, snapshot, state_vector)

        if inserted:
            inserted_count += 1
        else:
            existing_count += 1

    mark_snapshot_normalised(db, snapshot)

    return inserted_count, existing_count


def run_opensky_normalisation(max_snapshots=DEFAULT_SNAPSHOT_BATCH_SIZE):
    normalised_snapshots = 0
    inserted_states = 0
    existing_states = 0
    failed_snapshots = 0
    attempted_count = 0

    logger.info("Starting OpenSky normalisation")

    with Database() as db:
        while (max_snapshots is None or attempted_count < max_snapshots):
            snapshot = fetch_next_pending_snapshot(db)

            if snapshot is None:
                break

            attempted_count += 1
            snapshot_id = snapshot['snapshot_id']

            try:
                # all aircraft from one raw response are handled in one transaction
                with db.dbconnection:
                    inserted, existing = normalise_opensky_snapshot(db, snapshot)

            except (TypeError, ValueError, psycopg2.Error) as exc:
                logger.exception("FAILED | snapshot_id=%s", snapshot_id)

                # start new transaction (previous rolled back) to save error message
                with db.dbconnection:
                    mark_snapshot_failed(db, snapshot_id, exc)

                failed_snapshots += 1
                continue

            normalised_snapshots += 1
            inserted_states += inserted
            existing_states += existing

            logger.info("NORMALISED | snapshot_id=%s | inserted=%s | existing=%s",
                        snapshot_id, inserted, existing)

    logger.info("OpenSky normalisation complete | attempted=%s | snapshots=%s | inserted_states=%s | existing_states=%s | failed=%s",
                attempted_count, normalised_snapshots, inserted_states, existing_states, failed_snapshots)

    return {
        'attempted': attempted_count,
        'normalised_snapshots': normalised_snapshots,
        'inserted_states': inserted_states,
        'existing_states': existing_states,
        'failed': failed_snapshots
    }


def main():
    result = run_opensky_normalisation()

    if result['failed']:
        sys.exit(1)


if __name__ == "__main__":
    main()
