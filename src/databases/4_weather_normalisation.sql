/*
enforce some idempotency for weather data
*/
alter table public.weather
    add constraint weather_condition_unique
    unique (icon_id, main, description);

alter table public.weather_state
    add constraint weather_state_snapshot_unique
    unique (snapshot_id);
    