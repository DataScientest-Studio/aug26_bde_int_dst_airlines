from dash import html, Input, Output
from datetime import datetime

# unsere App aus app.py (damit die Callbacks wissen, zu welcher App sie gehören)
from app import app

# Beispieldaten aus data.py
from data import FLIGHTS, WEATHER


# ===== Callback 1: Filter ändern --> Kacheln und Tabelle aktualisieren =====
@app.callback(
    # gleiche Reihenfolge wie beim return
    Output("kpi-flights", "children"),
    Output("kpi-in-air", "children"),
    Output("kpi-busiest", "children"),
    Output("kpi-duration", "children"),
    Output("flights-table", "data"),
    Output("no-flights-message", "children"),
    Input("filter-airline", "value"),
    Input("search-icao24", "value"),
    Input("filter-date", "date"),
)
def update_dashboard(airline, search, date):

    if search is None:
        search = ""
    selected_flights = []

    for flight in FLIGHTS:
        if flight["date"] == date:
            # Fall 1: Suchfeld leer --> nur nach Airline filtern
            if search == "":
                if airline == "All airlines":
                    selected_flights.append(flight)
                else:
                    if flight["airline"] == airline:
                        selected_flights.append(flight)
            # Fall 2: nach icao24 suchen
            else:
                if search in flight["icao24"]:
                    selected_flights.append(flight)

    if len(selected_flights) == 0:
        message = "No flights found for this filter."
    else:
        message = ""

    # Kachel 1: Flüge zählen
    number_of_flights = len(selected_flights)

    # Kachel 2, 3 und 4: Platzhalter, kommen später aus dem Backend
    in_air = "tbd"
    busiest = "tbd"
    duration = "tbd"

    # gleiche Reihenfolge wie die Outputs
    return number_of_flights, in_air, busiest, duration, selected_flights, message


# ===== Callback 2: Zeile anklicken --> Details anzeigen =====
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

    # Inhalt für Box 1: der Flug
    flight_text = [
        html.P("Flight number"),
        html.H2(flight["flight"]),
        html.Div(
            className="row",
            children=[
                html.Div(
                    children=[
                        html.P("Departure"),
                        html.B(flight["from"] + " · " + flight["departure"]),
                    ],
                ),
                html.Div(
                    children=[
                        html.P("Arrival"),
                        html.B(flight["to"] + " · " + flight["arrival"]),
                    ],
                    style={"text-align": "right"},
                ),
            ],
        ),
        # Zeile 2: Airline
        html.Div(
            className="row",
            children=[html.P("Airline"), html.P(flight["airline"])],
        ),
        # Zeile 3: Status
        html.Div(
            className="row",
            children=[html.P("Status"), html.P(flight["status"])],
        ),
    ]

    # Das Wetter am Zielflughafen holen
    destination = flight["to"]
    weather = WEATHER[destination]

    # Inhalt für Box 2: das Wetter
    weather_text = [
        html.P(destination),
        html.H2(str(weather["temp"]) + " °C"),
        html.Div(
            className="row",
            children=[html.P("Conditions"), html.P(weather["condition"])],
        ),
    ]

    # zwei Outputs, also zwei Werte, gleiche Reihenfolge
    return flight_text, weather_text


# ===== Callback 3: Uhrzeit der letzten Aktualisierung =====
@app.callback(
    Output("last-update", "children"),
    Input("refresh-timer", "n_intervals"),
)
def show_last_update(n):
    now = datetime.now().strftime("%H:%M:%S")
    return "Last update: " + now
