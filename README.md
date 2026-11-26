# Airport-area Air-Traffic Dashboard

This project is a data-engineering pipeline and dashboard for observing aircraft around selected airports and displaying local weather at the same time. It is not a commercial flight-tracking service, a complete airport timetable, or continuous radar coverage.

The implemented data layer collects source responses, preserves them as immutable raw JSON, registers them in PostgreSQL, and normalises them into dashboard-facing tables. The dashboard, API, and modelling components can use clean relational observations without losing their link to the original source response.

## Scope

The current scope covers five German airport areas:

| Airport | ICAO | IATA |
| --- | --- | --- |
| Munich | 'EDDM' | 'MUC' |
| Frankfurt | 'EDDF' | 'FRA' |
| Berlin Brandenburg | 'EDDB' | 'BER' |
| Hamburg | 'EDDH' | 'HAM' |
| Duesseldorf | 'EDDL' | 'DUS' |

For a selected airport, the data product can provide:

- aircraft detected inside the configured airport-area bounding box;
- position, altitude, velocity, track, vertical rate, ground status, callsign, and observation times when supplied by OpenSky;
- current weather conditions, including temperature, wind, cloudiness, visibility, and weather icon;
- stored historical snapshots collected since the project began;
- traceability from a dashboard observation back to its raw API response.

The dashboard represents periodic snapshots. It does not infer a complete route, operating airline, departure, arrival, or a continuous aircraft trajectory from an OpenSky state vector alone.

## Data-source decisions

The project began by evaluating airline and schedule APIs. Live test requests were essential: developer-portal documentation, issued credentials, and actual endpoint behaviour did not always match.

| Source | Decision | Reason |
| --- | --- | --- |
| OpenSky | Used | Reliable airport-area aircraft state vectors |
| OpenWeather | Used | Current weather by airport coordinates |
| Air France-KLM | Not used | Endpoint and contract access mismatch; the submitted support ticket received no response during the project |
| Aviationstack | Not used as a core source | Free-plan date and history restrictions, request limits, and pagination prevented complete schedule collection |
| Lufthansa | Not used | API deprecated |
| Cirium | Not used | Trial access too limited |

### OpenSky attribution

OpenSky data are used with the required academic attribution:

> Matthias Schäfer, Martin Strohmeier, Vincent Lenders, Ivan Martinovic and Matthias Wilhelm. "Bringing Up OpenSky: A Large-scale ADS-B Sensor Network for Research". In Proceedings of the 13th IEEE/ACM International Symposium on Information Processing in Sensor Networks (IPSN), pages 83-94, April 2014.

The result is an airport-area live-status dashboard rather than a schedule-enrichment or timetable product. Schedule-related database entities remain available for a future provider with suitable access.

## Architecture

~~~text
Airport reference data
        |
        +--> OpenSky collector every 30 minutes
        |        |
        |        +--> data/raw/opensky/states/.../*.json
        |
        +--> OpenWeather collector every 60 minutes
                 |
                 +--> data/raw/openweather/current/.../*.json

Raw-snapshot registration
        |
        +--> ingestion.raw_snapshot  [bronze processing ledger]
                 |
                 +--> OpenWeather normalisation --> public.weather_state
                 |
                 +--> OpenSky normalisation    --> public.flight_state
                                                    |
                                                    +--> dashboard, API, and analysis
~~~

Collection, registration, and normalisation are deliberately separate. A database outage or normalisation failure must not stop collection of source data. Retained raw responses can be processed later without another API request.

## Project layout

~~~text
data/
  reference_data/airports.json  Airport configuration and OpenSky boxes
  raw/                          Immutable collected JSON, ignored by Git
src/
  data/collectors/              OpenSky and OpenWeather collectors
  data/ingestors/               Registration and source-specific normalisers
  data/utils/                   Shared HTTP, raw-storage, and support utilities
  databases/                    SQL schema, constraints, migrations, and DB helper
  features/dashboard/           Dashboard-related application code
airflow/                        Optional containerised Airflow deployment
reports/                        Detailed technical reports and lessons learned
~~~

## Data collection and raw storage

The airport configuration in 'data/reference_data/airports.json' supplies each airport ICAO code, coordinates, and OpenSky bounding box.

| Collector | Request | Frequency | Raw resource |
| --- | --- | --- | --- |
| OpenSky | Current aircraft state vectors within an airport bounding box | Every 30 minutes | 'opensky/states' |
| OpenWeather | Current weather at airport latitude and longitude | Every 60 minutes | 'openweather/current' |

Each successful response is written unchanged to:

~~~text
data/raw/<provider>/<resource>/airport=<ICAO>/<UTC timestamp>.json
~~~

For example:

~~~text
data/raw/opensky/states/airport=EDDM/2026-11-17T103015123456Z.json
~~~

Raw files are immutable pipeline inputs. The storage utility writes to a temporary file in the destination directory and atomically renames it to the final '.json' name. The registration stage only sees complete JSON files, even if collection is interrupted.

### Collector error handling and logging

The shared HTTP client uses a 30-second timeout and distinguishes among unsuccessful HTTP responses, connection or timeout failures without a usable response, and invalid JSON responses. API credentials are loaded from environment variables and never committed.

Collectors process airports independently. They log a start event and then either a successful stored-file record or a failure with the exception type for each airport. One failure does not stop the remaining airport requests. A collector exits non-zero when any airport fails, making scheduled execution observable through logs and exit status.

## Database design

PostgreSQL on Supabase stores two deliberately separate concerns:

| Schema | Purpose |
| --- | --- |
| 'ingestion' | Durable raw-source lineage and processing state |
| 'public' | Normalised reference data and dashboard-facing observations |

'ingestion.raw_snapshot' is the processing ledger and bronze layer. It stores provider, resource, airport, collection time, source observation time, raw file path, complete JSONB payload, normalisation state, and an optional error message.

The main 'public' entities are:

- reference data: 'airport', 'timezone', 'aircraft', 'position_source', 'squawk', 'weather', and 'weather_icon';
- observations: 'weather_state' and 'flight_state';
- lineage: every normalised observation retains its 'snapshot_id' reference to 'ingestion.raw_snapshot'.

The schema includes indexes for the dashboard's main access patterns, particularly airport plus observation time and aircraft plus observation time. The executable SQL files in 'src/databases/' are the source of truth for the schema.

### Constraints and idempotency

The pipeline is designed for an exactly-once effect even when a stage is safely rerun:

- 'raw_file_path' is unique in 'ingestion.raw_snapshot', so the same raw file cannot be registered twice;
- 'weather_state' is unique per 'snapshot_id';
- 'flight_state' is unique per '(snapshot_id, aircraft_icao24)';
- lookup tables use stable business keys and conflict-safe inserts or upserts.

The same aircraft can correctly occur in multiple snapshots because those rows represent different observations over time. Duplicate prevention applies only within one source snapshot.

## Ingestion and normalisation

'src.data.run_ingestion' executes the stages below in order. Each stage returns counters, writes structured logs, and contributes to a non-zero process exit status if it fails.

| Stage | Responsibility |
| --- | --- |
| Raw-snapshot registration | Discovers complete files under 'data/raw', parses their path and UTC filename, and records metadata plus JSON payload in 'ingestion.raw_snapshot' |
| OpenWeather normalisation | Resolves weather and icon lookup data and inserts one 'weather_state' observation per weather snapshot |
| OpenSky normalisation | Validates state vectors, resolves aircraft and static lookup data, and inserts one 'flight_state' per aircraft in a snapshot |

Registration and normalisation use bounded, configurable batches. Registration selects old files fairly across '(provider, airport)' streams, so a busy source or airport cannot starve the others. Backfill uses the same code path with a larger or unrestricted limit.

For each snapshot, all normalised rows and the 'normalised_at' update are written in one database transaction. If anything fails, the transaction rolls back. A separate short transaction records 'normalisation_error', leaving the raw payload available for diagnosis and explicit requeueing after the cause is fixed.

The processing state is therefore:

| State | Meaning |
| --- | --- |
| 'normalised_at IS NULL' and 'normalisation_error IS NULL' | Pending and eligible for normalisation |
| 'normalised_at IS NOT NULL' | Successfully normalised |
| 'normalisation_error IS NOT NULL' | Failed, retained for diagnosis, and not retried automatically |

## Running locally

Create and activate a Python virtual environment, install the repository dependencies, and copy the environment template to '.env'. Configure the required API and Supabase database settings locally; do not commit '.env'.

Typical data-layer commands from the project root are:

~~~bash
python -m src.data.ingestors.ingest_airports
python -m src.data.collectors.collector_opensky
python -m src.data.collectors.collector_openweather
python -m src.data.ingestors.raw_snapshots
python -m src.data.ingestors.openweather
python -m src.data.ingestors.opensky
python -m src.data.run_ingestion
~~~

Use 'src.data.run_ingestion' for the normal registration-plus-normalisation sequence. Individual commands are useful for development, recovery, and demonstration.

## Operations and orchestration

### Current lightweight runtime

The current small VM uses cron because it is simple and appropriate for the workload. Wrapper scripts change to the project directory, load '.env', use the project virtual environment, and write logs. The ingestion wrapper uses 'flock' so a slow run cannot overlap with the next scheduled run.

Cron does not inherit variables from an interactive shell. Making the working directory, virtual environment, and environment file explicit is therefore required for unattended jobs.

### Airflow deployment option

The repository also contains a tested, optional containerised Airflow deployment in 'airflow/'. Airflow orchestrates the existing Python modules; it does not reimplement collection or data-processing logic.

Airflow metadata is stored in a small local PostgreSQL container, separate from the Supabase project database. All DAG schedules use UTC and are created paused by default.

| DAG | Schedule | Module |
| --- | --- | --- |
| 'airlines_collect_opensky' | Every 30 minutes | 'src.data.collectors.collector_opensky' |
| 'airlines_collect_openweather' | Hourly at ':00' | 'src.data.collectors.collector_openweather' |
| 'airlines_register_raw_snapshots' | At ':05' and ':35' | 'src.data.ingestors.raw_snapshots' |
| 'airlines_normalise_openweather' | Hourly at ':15' | 'src.data.ingestors.openweather' |
| 'airlines_normalise_opensky' | At ':15' and ':45' | 'src.data.ingestors.opensky' |

Initial Airflow setup:

~~~bash
cp airflow/.env.template airflow/.env
mkdir -p data/raw
chmod 600 airflow/.env
docker compose --env-file airflow/.env -f docker-compose.airflow.yml build
docker compose --env-file airflow/.env -f docker-compose.airflow.yml up airflow-init
docker compose --env-file airflow/.env -f docker-compose.airflow.yml up -d
~~~

The Airflow UI is available at 'http://localhost:8080' by default. The root '.env' must also be available because collectors and ingestors use it for OpenWeather and Supabase settings. Stop the deployment with:

~~~bash
docker compose --env-file airflow/.env -f docker-compose.airflow.yml down
~~~

Do not use 'down -v' unless intentionally removing Airflow metadata and task logs. Cron and Airflow are alternative schedulers: only one should actively trigger the production data pipeline at a time.

## Limitations

- OpenSky state vectors do not reliably identify an operating airline, route, origin, destination, or scheduled and actual arrival and departure times.
- 'icao24' identifies an aircraft transponder, not a specific flight. Callsigns can be absent, reused, or insufficient to establish a scheduled flight.
- Coverage is limited to aircraft detected by OpenSky inside the configured geographic boxes. An empty snapshot does not prove that an airport has no traffic.
- The data represent periodic snapshots rather than continuous trajectories or real-time radar.
- Historical data begin when project collection begins. A date selector can show stored observations, not arbitrary historical source data.

## Lessons learned

- Preserve raw data before transformation. It separates collection from database availability and enables replay without spending another API request.
- Treat 'ingestion.raw_snapshot' as a bronze layer and processing ledger, not merely a file inventory.
- Use atomic file writes so downstream ingestion never reads a partial JSON response.
- Make reruns safe with unique constraints and conflict-safe writes.
- Use a transaction per source snapshot. A failed snapshot must not appear partially normalised and successful.
- Log enough context to diagnose operational problems: stage, airport or snapshot ID, file path, counters, and error type.
- Bound batch work and distribute it fairly. Real database throughput, especially for many aircraft states, can be much slower than expected.
- Seed static lookup data rather than repeatedly upserting it in a high-volume path. Repeated conflicting inserts can still consume identity-sequence values.
- Test actual API behaviour early. Plan limits, endpoint permissions, pagination, and historical access can change the viable product scope.

## Detailed documentation

The root README is the consolidated project overview. The following documents retain the full technical discussion:

1. [API evaluation and source selection](reports/report.MD)
2. [Cirium Sky API reference](reports/cirium_sky_api.MD)
3. [Dashboard data-product description](reports/dashboard_description.md)
4. [Collectors and operational logging](reports/collectors_and_logging.md)
5. [Database documentation](reports/database_documentation.MD)
6. [Database schema diagram](reports/figures/db_schema.png)
7. [Ingestion and normalisation pipeline](reports/ingestion_normalisation.md)
8. [Lessons learned](reports/lessons_learned.md)
9. [Airflow deployment guide](airflow/README.md)
10. [Dashboard documentation](src/features/dashboard/README.md)
