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
        }
        # add the row to the list
        rows.append(row)
    return rows


# Returns the list of flights for the dashboard.
def get_flight_list():
    # API address: get flight List
    url = "http://127.0.0.1:8000/get_flight_list?limit=10&offset=0"
    response = requests.get(url)
    # JSON text -->  dictionary
    data = response.json()
    return data["flight_list"]
