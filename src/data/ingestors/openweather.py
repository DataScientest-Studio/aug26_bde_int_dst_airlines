import logging
import sys
import psycopg2
from datetime import datetime, timezone

from src.databases.databases import Database


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# derive the image url of the icon from OpenWeather (can be useful for dashboard)
def build_icon_url(icon_code):
    return f"https://openweathermap.org/img/wn/{icon_code}@2x.png"


# insert/update into public.icon
def upsert_icon(db, icon_code):
    query = """
        insert into public.icon (icon_id, icon)
        values (%s, %s)
        on conflict (icon_id) do update
        set icon = excluded.icon;
    """

    db.execute_sql(query, (icon_code, build_icon_url(icon_code)))


# insert/update into public.weather
def upsert_weather_condition(db, condition):
    query = """
        insert into public.weather (icon_id, main, description)
        values (%s, %s, %s)
        on conflict (icon_id, main, description) do update
        set description = excluded.description
        returning weather_id;
    """
    # DO UPDATE makes Postgres return weather_id both for a new condition and an already-existing one 
    # we need weather_id to insert weather_state.weather_id

    rows = db.execute_sql(
        query, 
        (condition['icon'],
        condition['main'],
        condition['description'])
    )

    return rows[0]['weather_id']


# insert into public.weather_state
def insert_weather_state(db, snapshot, weather_id):
    payload = snapshot['payload']

    time_of_record = datetime.fromtimestamp(payload['dt'], tz=timezone.utc)

    query = """
        insert into public.weather_state(
            airport_icao,
            weather_id,
            temperature_c,
            wind_speed_mps,
            wind_direction_deg,
            wind_gust_mps,
            cloudiness_percent,
            visibility_m,
            time_of_record,
            snapshot_id
        )
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        on conflict (snapshot_id) do nothing
        returning weather_state_id;
    """

    # safely check optional fields such as wind.gust
    rows = db.execute_sql(
        query,
        (snapshot['airport_icao'],
         weather_id,
         payload['main']['temp'],
         payload.get('wind', {}).get('speed'),
         payload.get('wind', {}).get('deg'),
         payload.get('wind', {}).get('gust'),
         payload.get('clouds', {}).get('all'),
         payload.get('visibility'),
         time_of_record,
         snapshot['snapshot_id']
        )
    )

    if rows:
        return rows[0]['weather_state_id'], True

    return None, False


# OpenWeather may provide several condition per location
# our schema supports only one weather condition per observation
def get_primary_weather_condition(payload):
    weather_conditions = payload.get('weather')

    if not weather_conditions:
        raise ValueError("OpenWeather payload has no weather condition")

    return weather_conditions[0]


# retrieve one unprocessed OpenWeather response
def fetch_next_pending_snapshot(db):
    rows = db.execute_sql(
        """
        select snapshot_id, airport_icao, payload
        from ingestion.raw_snapshot
        where provider = %s 
          and resource = %s 
          and normalised_at is null
          and normalisation_error is null
        order by collected_at
        limit 1;
        """,
        ("openweather", "current")
    )

    return rows[0] if rows else None


# mark a raw snapshot complete only after its normalised rows are written successfully
# source_observed_at is OpenWeather measurement time (dt)
# normalised_at is the time of processing
def mark_snapshot_normalised(db, snapshot_id, payload):
    source_observed_at = datetime.fromtimestamp(payload['dt'], tz=timezone.utc)

    db.execute_sql(
        """
        update ingestion.raw_snapshot
        set source_observed_at = %s,
            normalised_at = now(),
            normalisation_error = null
        where snapshot_id = %s;
        """,
        (source_observed_at, snapshot_id)
    )


# mark normalisation failure
def mark_snapshot_failed(db, snapshot_id, error):
    error_message = f"{type(error).__name__}: {error}"

    db.execute_sql(
        """
        update ingestion.raw_sanpshot
        set normalisation_error = %s
        where snapshot_id = %s;
        """,
        (error_message[:1000], snapshot_id)
    )

# normalisation and insertion pipeline (one snapshot): 
# icon -> weather condition -> weather observation -> raw snapshot status
def normalise_openweather_snapshot(db, snapshot):
    
    payload = snapshot['payload']
    condition = get_primary_weather_condition(payload)
    upsert_icon(db, condition['icon'])
    weather_id = upsert_weather_condition(db, condition)
    weather_state_id, inserted = insert_weather_state(db, snapshot, weather_id)
    mark_snapshot_normalised(db, snapshot['snapshot_id'], payload)
    
    return weather_state_id, inserted


# batch processing
def main():
    normalised_count = 0
    existing_count = 0
    failed_count = 0

    logger.info("Starting OpenWeather normalisation")

    with Database() as db:
        while True:
            snapshot = fetch_next_pending_snapshot(db)

            if snapshot is None:
                break

            snapshot_id = snapshot['snapshot_id']

            try:
                with db.dbconnection:
                    weather_state_id, inserted = normalise_openweather_snapshot(db, snapshot)

                if inserted:
                    normalised_count += 1
                    logger.info("NORMALISED | snapshot_id=%s | weather_state_id=%s",
                                snapshot_id, weather_state_id)
                else:
                    existing_count += 1
                    logger.info("ALREADY NORMALISED | snapshot_id=%s", snapshot_id)

            except (TypeError, ValueError, psycopg2.Error) as exc:
                logger.exception("FAILED | snapshot_id=%s", snapshot_id)

                # failed normalisation transaction rolled back;
                # start a separate transaction to record the error
                with db.connection:
                    mark_snapshot_failed(db, snapshot_id, exc)

                failed_count += 1

    logger.info("OpenWeather normalisation complete | normalised=%s | already_normalised=%s | failed=%s",
                normalised_count, existing_count, failed_count)

    if failed_count:
        sys.exit(1)

if __name__ == "__main__":
    main()
