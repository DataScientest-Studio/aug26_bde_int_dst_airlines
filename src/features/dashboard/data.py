# ===== data.py: alle Daten  =====

# Testdata in same forme of API (flight_list) \src\fapi\models
# 3 parts: flight, airport und weather
# later will be replaced ----> API-Aufruf
from datetime import datetime
import requests
from pprint import pprint


# transform flight_list to flat rows for data flight table
def build_table_rows(flight_list):
    rows = []  # empty list
    for entry in flight_list:
        flight = entry["flight"]
        airport = entry["airport"]
        weather = entry["weather"]

        # Status in the air / landed
        if flight["on_ground"] == True:
            status = "Landed"
        else:
            status = "In the air"

        # airport - can be null/empty ---> iata most known
        if airport["iata"]:
            airport_code = airport["iata"]
        else:
            airport_code = airport["icao"]

        # display baro_altitude
        if flight["baro_altitude"] is None:
            altitude = "-"
        else:
            altitude = round(flight["baro_altitude"], 1)

        # Velocity in km/h
        if flight["velocity"] is None:
            speed_kmh = "-"
        else:
            speed_kmh = round(flight["velocity"] * 3.6)

        # ISO time text --> HH:MM
        if flight["last_contact"] is None:
            last_contact = "-"
        else:
            last_contact = (
                datetime.fromisoformat(flight["last_contact"])
                .astimezone()
                .strftime("%H:%M")
            )
        # weather icon: code (e.g. "01n") --> image link
        if weather["icon_id"] is None:
            icon_url = ""
        else:
            icon_url = (
                "https://openweathermap.org/img/wn/" + weather["icon_id"] + "@2x.png"
            )

        row = {
            "callsign": flight["callsign"] or "-",
            "status": status,
            "altitude": altitude,
            "speed": speed_kmh,
            "airport": airport_code,
            "city": airport["city"],
            "last_contact": last_contact,
            "temp": weather["temp"],
            "weather": weather["description"],
            "icon": icon_url,
        }
        # add the row to the list
        rows.append(row)
    return rows


# Returns the list of flights for the dashboard.
# The API filters in  database (API get_flight_list).
def get_flight_list(date, airport, time_from, time_to, search):
    # base address: max. 100 flights for this date
    url = "http://127.0.0.1:8000/get_flight_list?limit=100&offset=0&date=" + date

    # add each filter only if it is chosen
    if airport is not None:
        url = url + "&iata=" + airport
    if time_from is not None:
        url = url + "&time_from=" + time_from
    if time_to is not None:
        url = url + "&time_to=" + time_to
    if search is not None and search != "":
        url = url + "&callsign=" + search

    response = requests.get(url)
    # JSON text --> dictionary
    data = response.json()
    return data["flight_list"]


# Returns the airports as options for the dropdown.
def get_airport_options():
    # API address: get airport list
    url = "http://127.0.0.1:8000/get_airport_list"
    response = requests.get(url)
    # JSON text --> dictionary
    data = response.json()

    options = []  # empty list
    for airport in data["airport_list"]:
        # text in the dropdown, e.g. "FRA - Frankfurt"
        label = airport["iata"] + " - " + airport["city"]
        # value for the filter: the iata code (same as in the table)
        option = {"label": label, "value": airport["iata"]}
        options.append(option)
    return options


# Returns the hours 00:00 ... 23:00 as options for the time dropdowns.
def get_time_options():
    options = []  # empty list
    for hour in range(24):
        # e.g. 7 --> "07:00" (zfill adds a leading zero)
        text = str(hour).zfill(2) + ":00"
        option = {"label": text, "value": text}
        options.append(option)
    return options
