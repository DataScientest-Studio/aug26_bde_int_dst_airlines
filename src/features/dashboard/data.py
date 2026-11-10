# ===== data.py: alle Daten  =====

# Testdata in same forme of API (flight_list) \src\fapi\models
# 3 parts: flight, airport und weather
# later will be replaced ----> API-Aufruf
from datetime import datetime

FLIGHT_LIST = [
    {
        # Part 1: flight data
        "flight": {
            "callsign": "DLH123",
            "on_ground": False,  # False = in the air, True = am Boden
            "baro_altitude": 10500,
            "velocity": 230,  # velocity in m/s
            "last_contact": 1762687500,  # Unix-Zeit
        },
        # Part 2: Airport data (Airport_model.py)
        "airport": {
            "icao": "EDDF",
            "iata": "FRA",
            "city": "Frankfurt",
        },
        # Part 3: Airport data (Airport_model.py)
        "weather": {
            "temp": 8.5,
            "description": "broken clouds",
        },
    },
    {
        "flight": {
            "callsign": "EWG45",
            "on_ground": True,
            "baro_altitude": 0,
            "velocity": 0,
            "last_contact": 1762687320,
        },
        "airport": {
            "icao": "EDDK",
            "iata": "CGN",
            "city": "Köln",
        },
        "weather": {
            "temp": 7.2,
            "description": "clear sky",
        },
    },
]


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

        # Velocity in km/h
        speed_kmh = round(flight["velocity"] * 3.6)

        # unix time ---> real time
        last_contact = datetime.fromtimestamp(flight["last_contact"]).strftime("%H:%M")

        row = {
            "callsign": flight["callsign"],
            "status": status,
            "altitude": flight["baro_altitude"],
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


# print(build_table_rows(FLIGHT_LIST))
