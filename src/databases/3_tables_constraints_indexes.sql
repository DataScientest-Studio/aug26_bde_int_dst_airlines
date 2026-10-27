create table if not exists public.weather_state (
  weather_state_id serial primary key,
  airport_icao char(4) references airport(airport_icao) not null,
  weather_id int4 references weather(weather_id) not null,
  temperature_c numeric(5,2) null,
  wind_speed_mps numeric(5,2) null,
  wind_direction_deg int4 null,
  wind_gust_mps numeric(5,2) null,
  cloudiness_percent int4 null,
  visibility_m int4 null,
  time_of_record timestamptz not null,
  snapshot_id bigint references ingestion.raw_snapshot(snapshot_id)
);

create table if not exists public.flight_state(
  flight_state_id serial primary key,
  airport_icao char(4) references airport(airport_icao) not null,
  category_id int4 references category(category_id) null,
  squawk_id char(4) references squawk(squawk_id) null,
  position_source_id int2 references position_source(position_source_id) null,
  aircraft_icao24 char(6) references aircraft(aircraft_icao24),
  callsign varchar(8),
  time_position timestamptz null,
  last_contact timestamptz null,
  latitude numeric(9,6) null,
  longitude numeric(9,6) null,
  baro_altitude numeric(7,2) null,
  geo_altitude numeric(7,2) null,
  on_ground boolean not null,
  velocity numeric(6,2) null,
  true_track numeric(5,2) null,
  vertical_rate numeric(4,2) null,
  created_at timestamptz not null,
  snapshot_id bigint references ingestion.raw_snapshot(snapshot_id)
);

create table if not exists public.travel (
  travel_id serial primary key,
  departure_airport_icao char(4) references airport(airport_icao),
  arrival_airport_icao char(4) references airport(airport_icao),
  aircraft_icao24 char(6) references aircraft(aircraft_icao24),
  airline_icao char(3) references airline(airline_icao),
  travel_date date null,
  travel_status int4 references status(status_id) null,
  departure_delay int8 null,
  departure_scheduled timestamptz null,
  departure_estimated timestamptz null,
  departure_actual timestamptz null,
  arrival_delay int8 null,
  arrival_scheduled timestamptz null,
  arrival_estimated timestamptz null,
  arrival_actual timestamptz null
);


/* Constraints: */
alter table public.airport
  add constraint airport_latitude_range
    check (latitude between -90 and 90),
  add constraint airport_longitude_range
    check (longitude between -180 and 180),
  add constraint airport_bbox_latitude_order
    check (lamin < lamax),
  add constraint airport_bbox_longitude_order
    check (lomin < lomax);

alter table public.weather_state
  add constraint weather_cloudiness_range
    check (cloudiness_percent between 0 and 100),
  add constraint weather_wind_direction_range
    check (wind_direction_deg between 0 and 360);

/* Indexes: */
create index if not exists flight_state_airport_time_idx
    on public.flight_state (airport_icao, created_at desc);

create index if not exists flight_state_aircraft_time_idx
    on public.flight_state (aircraft_icao24, created_at desc);

create index if not exists weather_state_airport_time_idx
    on public.weather_state (airport_icao, time_of_record desc);

create index if not exists raw_snapshot_provider_airport_time_idx
    on ingestion.raw_snapshot (provider, airport_icao, collected_at desc);