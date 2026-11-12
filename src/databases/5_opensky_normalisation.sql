/*
idempotency for OpenSky normalisation
*/

/* prevent duplicate insertion of state for the same aircraft */
alter table public.flight_state
    add constraint flight_state_snapshot_aircraft_unique
    unique (snapshot_id, aircraft_icao24);

/* used by OpenSky in state-vector; allows to match with our internal ID */
alter table public.position_source
    add column opensky_code smallint;

alter table public.position_source
    add constraint position_source_opensky_code_unique
    unique (opensky_code);