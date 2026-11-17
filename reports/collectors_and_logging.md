# Data collectors and operational logging

## Purpose

The collectors obtain source data and store it unchanged as raw JSON. They do
not transform the payload or write normalised observations directly to the
database. This separation preserves a replayable source record and allows the
ingestion pipeline to be retried independently of API collection.

The collectors use the airport configuration in
'data/reference_data/airports.json'. It supplies each airport's ICAO code,
coordinates, and OpenSky bounding box.

## Collectors

| Collector | Source and request | Schedule | Raw resource |
| --- | --- | --- | --- |
| OpenSky | Current aircraft state vectors within an airport bounding box | Every 30 minutes | 'opensky/states' |
| OpenWeather | Current weather for an airport's latitude and longitude | Every 60 minutes | 'openweather/current' |

OpenSky provides observations of aircraft physical state, including position,
altitude, ground status, velocity, track, and timestamps. OpenWeather provides
current weather conditions such as temperature, wind, cloudiness, and
visibility. API credentials are loaded from environment variables; they are not
stored in the repository.

## Raw-data storage

Each successful request is written under 'data/raw' using the layout:

data/raw/<provider>/<resource>/airport=<ICAO>/<UTC timestamp>.json


For example:

data/raw/opensky/states/airport=EDDM/2026-11-17T103015123456Z.json


The filename records the collection time in UTC and the path identifies the
provider, resource, and airport. Raw files are treated as immutable inputs to
later ingestion.

To avoid corrupted files, the storage utility writes the JSON payload to a
temporary file in the target directory and then atomically replaces it with the
final filename. A process interruption therefore leaves either a complete JSON
file or no final file.

## Error handling and logging

A shared HTTP client applies a 30-second request timeout and converts failures
into a project-specific exception. It distinguishes among:

- an HTTP response with an unsuccessful status;
- a request failure without a usable response, such as a connection failure or
  timeout;
- a successful HTTP response that cannot be decoded as JSON.

Each collector processes airports independently. For every airport it logs the
start of collection, then either a success record with the stored filepath (and
OpenSky state count) or a failure record with the exception type. One failed
airport does not prevent attempts for the remaining airports.

After processing all airports, a collector exits with status '0' only when all
requests succeeded. If any airport failed, it logs the affected ICAO codes and
exits with status '1'. This makes a scheduled run observable through its logs
and exit status, without requiring a separate monitoring service.

## Operational execution

The collectors run as separate scheduled jobs. Their frequencies are chosen to
stay within the available source limits while providing regular dashboard
snapshots. Collection and ingestion remain separate jobs: a temporary database
or normalisation failure does not prevent raw-source capture, and stored raw
files can be processed later.
