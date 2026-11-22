# Ingestion and normalisation pipeline

## Purpose

The ingestion pipeline converts immutable raw JSON files into relational
PostgreSQL records for analysis and dashboard queries. It is separate from data
collection: raw files can accumulate while the database is unavailable and be
processed later without calling the source APIs again.

The same pipeline supports both incremental ingestion and backfill. A normal
scheduled run processes a bounded set of unregistered or pending snapshots. A
backfill uses the same logic with an unrestricted batch size until the backlog
is exhausted.

## Airport reference-data ingestion

'data/reference_data/airports.json' is maintained manually. The
'ingest_airports' script is run when that reference file changes. For each
configured airport, it inserts the IANA timezone if necessary and then inserts
the airport, coordinates, and OpenSky bounding box. 'ON CONFLICT DO NOTHING'
makes reruns safe: existing airport records are not duplicated. The current
script inserts new reference entries only; it does not update values for an
existing airport.

## Pipeline stages

'src.data.run_ingestion' executes three stages in order:

1. raw-snapshot registration;
2. OpenWeather normalisation;
3. OpenSky normalisation.

Each stage writes structured log messages and returns counters. The orchestrator
logs each result and exits with a non-zero status if any stage reports failures.
This makes the scheduled job observable through logs and its exit code.

### 1. Raw-snapshot registration

The registration stage discovers JSON files under 'data/raw', parses their path
and UTC filename, and records the following metadata in
'ingestion.raw_snapshot':

- provider, resource, airport ICAO code, and collection time;
- relative raw-file path;
- complete JSON payload.

'raw_file_path' is unique. An already registered file is therefore recognised
without duplicating its payload, while 'ON CONFLICT DO NOTHING' also protects
against an unlikely concurrent registration attempt.

The default registration batch selects up to 20 unregistered files for each
'(provider, airport)' stream. Files are ordered oldest first within each stream.
This bounds a scheduled run and prevents a busy airport or provider from
starving the others. Passing no limit permits a full registration backfill.

A file is committed independently. Invalid JSON, file-system errors, and
database errors are logged against the individual file, while the remaining
files can still be processed.

### 2. OpenWeather normalisation

The weather normaliser selects the oldest pending snapshot where:

provider = 'openweather'
resource = 'current'
normalised_at IS NULL
normalisation_error IS NULL


For each payload, it selects the first reported weather condition, upserts the
weather icon and condition lookup values, and inserts one 'weather_state' row.
It stores the source measurement time ('dt') as 'source_observed_at' and marks
the raw snapshot as normalised only after the relational rows have been written.
Optional fields, such as wind gust, are handled safely when absent.

### 3. OpenSky normalisation

The OpenSky normaliser also processes the oldest pending snapshots. Before the
batch starts, it loads the static mapping between OpenSky position-source codes
and 'position_source' identifiers. This avoids repeated lookup-table writes for
every aircraft state and validates that the required source codes are present.

For every OpenSky state vector, the normaliser:

- validates required structure and 'on_ground' status;
- upserts the aircraft and its origin country;
- inserts a squawk code when present;
- trims the callsign and converts Unix timestamps to UTC;
- inserts a 'flight_state' observation linked to the airport and raw snapshot.

All aircraft states from one raw response are processed in one transaction. An
OpenSky snapshot with no reported states is still a valid observation and is
marked normalised after validation.

## Transaction and failure semantics

The pipeline uses 'ingestion.raw_snapshot' as its processing ledger:

| State | Meaning |
| --- | --- |
| 'normalised_at IS NULL' and 'normalisation_error IS NULL' | Pending and eligible for normalisation |
| 'normalised_at IS NOT NULL' | Successfully normalised |
| 'normalisation_error IS NOT NULL' | Failed and retained for diagnosis |

For either normaliser, a failed snapshot transaction rolls back all related
lookup and observation writes. A separate transaction then records a truncated
exception message in 'normalisation_error'. Consequently, a partial snapshot
cannot appear as a successful normalised result.

Failed snapshots are not retried automatically. After correcting the underlying
problem—for example a schema mismatch or malformed payload—they can be requeued
by clearing their error marker. This makes recovery explicit and prevents a
scheduled job from repeatedly failing on the same input.

## Idempotency and batching

Database constraints prevent duplicate normalised observations:

- one weather observation per raw weather snapshot;
- one aircraft state per '(snapshot_id, aircraft_icao24)' pair.

The normalisers process a configurable bounded number of snapshots per run
(default: 100 for each source). They report attempted, inserted, existing, and
failed counts. These limits allow the pipeline to catch up gradually when raw
collection is faster than database normalisation, while keeping individual
scheduled runs predictable.

Together with the raw JSON archive and processing ledger, this design provides
replayability, explicit failure recovery, and a clear lineage from each
dashboard value to the source response that produced it.
