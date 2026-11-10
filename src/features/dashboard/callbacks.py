from dash import html, Input, Output
from datetime import datetime
import requests

# unsere App aus app.py (damit die Callbacks wissen, zu welcher App sie gehören)
from app import app

# Beispieldaten aus data.py
from data import FLIGHT_LIST, build_table_rows


# ===== Callback 1: Filter ändern --> Kacheln und Tabelle aktualisieren =====
@app.callback(
    # gleiche Reihenfolge wie beim return
    Output("kpi-flights", "children"),
    Output("kpi-in-air", "children"),
    Output("kpi-busiest", "children"),
    Output("kpi-duration", "children"),
    Output("flights-table", "data"),
    Output("no-flights-message", "children"),
    Input("search-callsign", "value"),
    Input("filter-date", "date"),
)
def update_dashboard(search, date):

    # searchbox is empty?
    if search is None:
        search = ""
    # data from data.py to table rows
    rows = build_table_rows(FLIGHT_LIST)

    # content/result
    selected_flights = []

    for row in rows:
        if search.upper() in row["callsign"].upper():
            selected_flights.append(row)

    # no result ---> show message
    if len(selected_flights) == 0:
        message = "No flights found for this filter."
    else:
        message = ""

    # BOX 1-3: get data from Backend
    url = "http://127.0.0.1:8000/get_flight_summary?date=" + date
    response = requests.get(url)
    summary = response.json()

    number_of_flights = summary["flights_today"]
    in_air = summary["aircraft_in_the_air"]
    busiest = summary["busiest_airport"]

    # Kachel 4: kommt später
    duration = "tbd"

    # gleiche Reihenfolge wie die Outputs
    return number_of_flights, in_air, busiest, duration, selected_flights, message


# ===== Callback 2: selct row--> show details  =====
@app.callback(
    Output("selected-flight", "children"),
    Output("weather-box", "children"),
    Input("flights-table", "active_cell"),
    Input("flights-table", "derived_viewport_data"),
)
def show_selected_flight(active_cell, rows):
    # Noch nichts angeklickt? Dann zwei Hinweise anzeigen
    if active_cell is None:
        return "Click a flight in the table.", "No flight selected."

    # Nummer der angeklickten Zeile
    row_number = active_cell["row"]

    # Den Flug aus dieser Zeile holen
    flight = rows[row_number]

    # content for Box 1:
    info_box_1 = [
        html.P("Flight number (Callsign)"),
        html.H2(flight["callsign"]),
        html.Div(
            className="row", children=[html.P("Status"), html.P(flight["status"])]
        ),
        html.Div(
            className="row",
            children=[html.P("Altitude"), html.P(str(flight["altitude"]) + " m")],
        ),
        html.Div(
            className="row",
            children=[html.P("Speed"), html.P(str(flight["speed"]) + " km/h")],
        ),
        html.Div(
            className="row",
            children=[html.P("Last contact"), html.P(flight["last_contact"])],
        ),
    ]

    # content for Box 2:

    info_box_2 = [
        html.P("City "),
        html.H2(flight["city"]),
        html.Div(
            className="row",
            children=[html.P("Temperature"), html.P(str(flight["temp"]) + " °C")],
        ),
        html.Div(
            className="row", children=[html.P("Condition"), html.P(flight["weather"])]
        ),
    ]

    # zwei Outputs, also zwei Werte, gleiche Reihenfolge
    return info_box_1, info_box_2


# ===== Callback 3: Uhrzeit der letzten Aktualisierung =====
@app.callback(
    Output("last-update", "children"),
    Input("refresh-timer", "n_intervals"),
)
def show_last_update(n):
    now = datetime.now().strftime("%H:%M:%S")
    return "Last update: " + now
