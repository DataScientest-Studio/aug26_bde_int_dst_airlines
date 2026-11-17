# Airport-area air-traffic dashboard

## Purpose and scope

The project is an airport-area air-traffic dashboard. It describes aircraft
observed around a selected airport and the local weather at the observation
time. It is not intended to reproduce a commercial flight-tracking service or
a complete airport timetable.

The current data scope covers five German airports:

- Munich ('EDDM' / 'MUC')
- Frankfurt ('EDDF' / 'FRA')
- Berlin Brandenburg ('EDDB' / 'BER')
- Hamburg ('EDDH' / 'HAM')
- Düsseldorf ('EDDL' / 'DUS')

Each airport is associated with a geographic bounding box. An aircraft is in
scope when OpenSky reports its state inside that box; "nearby" therefore means
within the configured area, not necessarily inside the airport boundary.

## Identifiers and codes

The dashboard uses several aviation identifiers. The same acronym, **ICAO**, is
used for different code systems; an airport code and an aircraft 'icao24' are
not interchangeable.

| Identifier | Meaning and dashboard use | Example |
| --- | --- | --- |
| ICAO airport code | Four-character operational airport identifier; primary airport key in the data model. | 'EDDF' — Frankfurt Airport |
| IATA airport code | Three-character commercial airport identifier; useful for recognisable labels. | 'FRA' — Frankfurt Airport |
| ICAO24 / Mode S address | Six-character hexadecimal transponder address for an observed aircraft; used to distinguish aircraft within a snapshot and across observations. | '3C664E' |
| Callsign | Identifier broadcast by the aircraft, often related to a flight or operator. It can be absent and does not by itself prove a route or airline. | 'DLH1234' |
| Airline and flight codes | IATA airline codes ('LH') and flight numbers ('LH1234'), or ICAO airline codes ('DLH') and flight IDs ('DLH1234'), identify commercial operations. They require a schedule/flight-data source and are not currently derived from OpenSky alone. | 'LH' / 'DLH' — Lufthansa |

## Available functionality

For a selected airport and collected snapshot, the dashboard data can provide:

- aircraft identifier ('icao24') and, where available, callsign and origin
  country;
- latitude and longitude, ground/air status, pressure and geometric altitude;
- velocity, true track, vertical rate, last position update, and last contact;
- the weather observation for the same airport, including condition, temperature,
  wind, cloudiness, and visibility.

Historical views can use the snapshots stored by the project. Suitable
aggregations include the number of reported aircraft per snapshot or hour, the
number of distinct observed aircraft in a time window, and the share of aircraft
reported on the ground. Weather observations can be displayed alongside these
traffic measures.

## Data collection model

OpenSky is the primary source. It supplies live physical state vectors rather
than schedules, routes, arrivals, or departures. The collector queries OpenSky
for each airport bounding box every 30 minutes and stores the raw response. The
OpenWeather collector retrieves current conditions for each airport coordinate
every 60 minutes. Historical data therefore begin only when the project starts
collecting them; a date/time selector can show stored observations, not arbitrary
past traffic from the source API.

The database preserves both the collection timestamp and, where supplied by the
source, the timestamp of the source observation. This distinction matters when
interpreting delayed or missing position updates.

## Limitations and deliberately excluded features

- An OpenSky state vector does not reliably identify the operating airline,
  flight route, origin, destination, or scheduled/actual arrival and departure
  times. 'icao24' identifies an aircraft transponder; a callsign may be absent,
  reused, or insufficient to establish a specific scheduled flight.
- Observations are limited to aircraft detected by OpenSky and to the configured
  geographic boxes. Missing records do not prove that an airport has no traffic.
- The dashboard represents periodic snapshots, not continuous trajectories or
  real-time radar.
- Aviationstack was evaluated for schedule enrichment, but its free-plan request
  limit, access restrictions, and pagination make complete airport schedule
  collection infeasible. Airline and schedule enrichment are consequently out of
  scope for the current implementation.

The database retains schedule-related entities for possible future integration
with a suitable data provider.
