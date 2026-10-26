create table if not exists public.weather_state (
  weather_state_id serial primary key,
  airport_icao varchar(4) references airport(airport_icao),
  weather_id int4 references weather(weather_id),
  temperature_c numeric(5,2),
  wind_speed_mps numeric(5,2),
  wind_direction_deg int4,
  wind_gust_mps numeric(5,2),
  cloudiness_percent int4,
  visibility_m integer,
  time_of_record timestamptz,
  snapshot_id bigint references ingestion.raw_snapshot(snapshot_id)
);

create table if not exists public.flight_state(
  flight_state_id serial primary key,
  airport_icao varchar(4) references airport(airport_icao),
  category_id int4 references category(category_id),
  squawk_id int4 references squawk(squawk_id),
  position_source_id int2 references position_source(position_source_id),
/*  flight_id int4 references flight(flight_id), */
  aircraft_icao24 varchar(6) references aircraft(aircraft_icao24),
  callsign varchar(8),
  time_position timestamptz,
  last_contact timestamptz,
  latitude numeric(9,6),
  longitude numeric(9,6),
  baro_altitude numeric(7,2),
  geo_altitude numeric(7,2),
  on_ground boolean,
  velocity numeric(6,2),
  true_track numeric(5,2),
  vertical_rate numeric(4,2),
  created_at timestamptz,
  snapshot_id bigint references ingestion.raw_snapshot(snapshot_id)
);

create table if not exists public.travel (
  travel_id serial primary key,
  departure_airport_icao varchar(4) references airport(airport_icao),
  arrival_airport_icao varchar(4) references airport(airport_icao),
  aircraft_icao24 varchar(6) references aircraft(aircraft_icao24),
  airline_icao varchar(3) references airline(airline_icao),
  travel_date date,
  travel_status int4 references status(status_id),
  departure_delay int8,
  departure_scheduled timestamptz,
  departure_estimated timestamptz,
  departure_actual timestamptz,
  arrival_delay int8,
  arrival_scheduled timestamptz,
  arrival_estimated timestamptz,
  arrival_actual timestamptz
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