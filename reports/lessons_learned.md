# Lessons learned

## Preserve raw data before transformation

Collectors write immutable JSON files before any database normalisation. This
separates API collection from database availability and preserves the original
response for inspection and replay. It also avoids spending additional API
requests when a parser, schema, or database issue must be corrected.

'ingestion.raw_snapshot' acts as a database-backed bronze layer: it records the
raw payload, file path, collection metadata, and processing state. When a large
backlog delayed normalisation, raw snapshots could still be registered and later
processed without losing provenance or duplicating data.

## Write raw files atomically

A raw JSON file is first written as a temporary file in its destination
directory and then atomically renamed to its final '.json' name. The registration
stage discovers only final JSON files. This ensures that a process interruption
cannot cause the ingestion pipeline to read a partially written source payload.

## Make processing idempotent

Unique raw file paths prevent duplicate snapshot registration. Additional unique
constraints prevent duplicate weather observations per snapshot and duplicate
OpenSky aircraft states per '(snapshot_id, aircraft_icao24)'. Consequently,
rerunning a collector-registration or normalisation job is safe and does not
require manual deletion of previous results.

This was especially valuable after repairing the position-source lookup issue:
the affected raw snapshots were requeued and normalised from their retained
payloads instead of requesting the source APIs again.

## Log enough to diagnose, not merely to announce success

Per-airport and per-snapshot logs include the stage, airport or snapshot ID,
counts, file path where relevant, and error type. This made it possible to
identify both the backlog behaviour and the 'NumericValueOutOfRange' and
'SequenceGeneratorLimitExceeded' failures during normalisation.

The pipeline also returns stage counters and exits non-zero on failure. These
signals are suitable for cron logs and basic operational monitoring without a
separate monitoring platform.

## Use transactions at the snapshot boundary

All normalised rows for one source response are written in one transaction. A
failure rolls back the incomplete work; a separate transaction records the error
on the raw snapshot. The database therefore does not contain a partially
normalised snapshot presented as successful.

## Bound work and distribute it fairly

Raw registration is limited per '(provider, airport)' stream and processes old
files first. The normalisers also use configurable batch limits. This keeps a
scheduled run bounded and avoids a busy airport or provider starving the others.

Running the pipeline against a real backlog also showed that database work can
be substantially slower than collection, particularly when many aircraft states
require individual database operations. Batch sizes and schedules must be based
on observed throughput rather than optimistic estimates.

## Treat lookup tables as static reference data

The 'position_source' issue demonstrated that 'INSERT ... ON CONFLICT DO UPDATE'
can still consume identity-sequence values before the conflict is detected. Using
that pattern for every aircraft state exhausted the smallint sequence even though
only one logical lookup row existed.

The repair seeds the finite OpenSky position-source mapping once and loads it
into memory at the start of normalisation. Static reference data should be
seeded or maintained separately, not repeatedly upserted in a high-volume path.

## Make scheduled environments explicit

Cron does not inherit variables exported in an interactive terminal. The
scheduled wrappers therefore change to the project directory, load '.env', and
invoke the project virtual environment explicitly. This prevents missing API or
database credentials during unattended runs and keeps secrets out of source
code.

## Protect scheduled jobs from overlap

The ingestion cron wrapper uses 'flock' to ensure that only one ingestion run
holds the lock at a time. It was not needed in practice because the initial
backfill was monitored immediately, but it remains important protection: an
overlapping run could otherwise process the same backlog, compete for database
resources, and extend recovery time.

## Validate real API behaviour early

Developer-portal documentation, issued credentials, and the behaviour of a live
endpoint may differ. AF/KLM endpoint routing and Aviationstack plan restrictions
were discovered only through test requests. Pagination, historical-access
restrictions, and request budgets must be tested with representative queries
before they shape the data model or collection schedule.

## Preserve timestamp semantics

The pipeline stores both the local collection timestamp and the timestamp
reported by the source. They may differ because an aircraft position can be
stale or an API response can be delayed. Keeping both prevents the dashboard
from implying more precise real-time information than the source provides.
