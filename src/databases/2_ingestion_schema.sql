/* Schema for tracking the json files and raw ingestion */

create schema if not exists ingestion;

create table if not exists ingestion.raw_snapshot(
    snapshot_id bigint generated always as identity primary key,
    provider text not null,
    resource text not null,
    airport_icao char(4) references public.airport(airport_icao),
    collected_at timestamptz not null,
    source_observed_at timestamptz,
    raw_file_path text not null unique,
    payload jsonb not null,
    ingested_at timestamptz not null default now(),
    normalised_at timestamptz,
    normalisation_error text
);

