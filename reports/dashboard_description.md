0. 
Project: dashboard with an aviation theme.

1.
Main data source: 
OpenSky  
https://opensky-network.org/data/api

2.
Possible supplementary data: 
Aviationstack 
https://docs.apilayer.com/aviationstack/docs/api-documentation

OpenWeather
https://openweathermap.org/api/one-call-4?collection=one_call_api

3.
Limitations:
Only OpenSky provides live data with a sufficient access rate on a free plan (around 400 requests/day); therefore, it is used as the main source. 
Aviationstack provides up to 100 requests per month, which may become useful at more advanced stages of the project.

4.
Description: 

4.1.
General:
The essence of the project is determined by the available data. 
OpenSky provides live physical-state data (speed, direction, geographical position, etc.) for aircraft, rather than scheduled-flight data. 
Therefore, the dashboard reports the state of air traffic around selected locations (cities/airports). 
As an initial stage, it is suggested to limit the dashboard to two cities/airports:
(*) Munich and Frankfurt. 

4.2.
Main features:
a. Select an airport and time/date:
     provide a list of aircraft in the area of the selected airport, together with their states (coordinates, on the ground/in the air, speed, identifiers, etc.) for the selected timestamp.
b. retrieve statistics for the last 12/24/48 hours:
    show air-traffic statistics for the selected period, for example as an hourly histogram.
Extra features:
c. Enrich aircraft data with flight information (airline, scheduled/actual departure and arrival) where possible, using Aviationstack.
d. Add weather conditions to main features a and b.

4.3.
Technical side:
For 4.2.a, we could either request the current air-traffic state via the API or use historical data (depending on which historical data are available), based on the time/date selected by the user. 
For 4.2.b, we have to collect and store data for both airports (*) every 30 or 60 minutes. We can then rely on our own database and use the locally stored data.
For 4.2.c, the proposed approach is to make two Aviationstack API calls for each airport every 24 hours. These calls would request flights for today and yesterday. Some flights for today may not yet have actual arrival/departure times, which could provide an opportunity for a future prediction model. Flights for yesterday are assumed to have complete data. All data obtained from Aviationstack must be stored locally. It can later be used to obtain schedule information for aircraft, for example by joining on an aircraft identifier and flight date.
For 4.2.d, we collect weather data for the airports (*) at the same frequency (every 30 or 60 minutes) as in 4.2.b. These data will be stored locally and provided for 4.2.a and 4.2.b as additional information.

