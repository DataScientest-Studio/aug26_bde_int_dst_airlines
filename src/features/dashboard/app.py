from dash import Dash, html, dcc, dash_table, Input, Output
from data import FLIGHTS, WEATHER
from datetime import datetime

app = Dash(__name__)


# ===== Sample data. =====
# see data.py


# ===== Layout: =====
app.layout = html.Div(
    children=[
        dcc.Interval(
            id="refresh-timer",
            interval=10000,
        ),
        html.P(id="last-update"),
        # -----hier fängt der Titel an
        html.Div(
            children=[
                html.H1("Airlines Live Dashboard"),
                html.Div(
                    children=[
                        # Dropdown label
                        html.Label("Airline"),
                        dcc.Dropdown(
                            id="filter-airline",
                            options=["All airlines", "Lufthansa", "Swiss", "Austrian"],
                            value="All airlines",
                        ),
                    ],
                    style={"width": "250px"},  # Breite des Filters
                ),
            ],
            style={
                "display": "flex",  # nebeneinander
                "justify-content": "space-between",  # Titel links, Filter rechts
                "align-items": "center",  # beide auf gleicher Höhe
            },
        ),
        html.Div(
            children=[
                html.Label("Date"),
                dcc.DatePickerSingle(id="filter-date", date="2026-10-30"),
            ],
        ),
        # Row with 3 Fields :
        html.Div(
            children=[
                # Field 1: flight number
                html.Div(
                    children=[html.P("Number of Flights"), html.H2(id="kpi-flights")],
                    className="tile",
                ),
                # Field 2: Flights in Air
                html.Div(
                    children=[html.P("in the air?"), html.H2(id="kpi-in-air")],
                    className="tile",
                ),
                # Field 3: Busiest Destination/ Airoprt
                html.Div(
                    children=[
                        html.P("Busiest destination?"),
                        html.H2(id="kpi-busiest"),
                    ],
                    className="tile",
                ),
                # Field 4
                html.Div(
                    children=[
                        html.P("Avg. flight duration"),
                        html.H2(id="kpi-duration"),
                    ],
                    className="tile",
                ),
            ],
            style={"display": "flex", "gap": "40px"},
        ),
        # search field for aircraft
        # Reihe mit 2 Spalten: links Tabelle, rechts Boxen
        html.Div(
            children=[
                # ----- linke Spalte: Suchfeld + Tabelle -----
                html.Div(
                    children=[
                        # search field for aircraft
                        dcc.Input(
                            id="search-icao24",
                            type="text",
                            placeholder="Search icao24 no., e.g. 3c6444",
                        ),
                        # Flights table
                        dash_table.DataTable(
                            id="flights-table",
                            columns=[
                                {"name": "Flight", "id": "flight"},
                                {"name": "Airline", "id": "airline"},
                                {"name": "From", "id": "from"},
                                {"name": "To", "id": "to"},
                                {"name": "Departure", "id": "departure"},
                                {"name": "Arrival", "id": "arrival"},
                                {"name": "Status", "id": "status"},
                                {"name": "ICAO24", "id": "icao24"},
                                {"name": "Date", "id": "date"},
                            ],
                        ),
                    ],
                    style={"flex": "3"},
                ),
                # -----  Flug-Box + Wetter-Box -----
                html.Div(
                    children=[
                        # Box 1: Details of selected flight
                        html.Div(
                            children=[
                                html.H3("Selected flight"),
                                html.P(id="selected-flight"),
                            ],
                            className="tile",
                        ),
                        # Box 2: Weather at destination
                        html.Div(
                            children=[
                                html.H3("Weather at destination"),
                                html.P(id="weather-box"),
                            ],
                            className="tile",
                        ),
                    ],
                    style={"flex": "1"},  # 1 Teil breit
                ),
            ],
            style={"display": "flex", "gap": "20px", "margin-top": "20px"},
        ),
    ]
)


# ===== Callback 1: select Airline --> update of Field and table   =====
@app.callback(
    # same Reihnfolge wie return def update_dashboard
    Output("kpi-flights", "children"),
    Output("kpi-in-air", "children"),
    Output("kpi-busiest", "children"),
    Output("kpi-duration", "children"),
    Output("flights-table", "data"),
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
            # case 1: search box is empty --> only airline search
            if search == "":
                if airline == "All airlines":
                    selected_flights.append(flight)
                else:
                    if flight["airline"] == airline:
                        selected_flights.append(flight)
            # case 2: search to icao24 suchen
            else:
                if search in flight["icao24"]:
                    selected_flights.append(flight)

    # Kachel 1: Flüge zählen
    number_of_flights = len(selected_flights)

    # Kachel 2 und 3: Platzhalter, kommen später aus dem Backend
    in_air = "tbd"
    busiest = "tbd"
    duration = " random 3h 15 min"

    # 4 return same Reihenfolge for output
    return number_of_flights, in_air, busiest, duration, selected_flights


# ===== Callback 2: Zeile anklicken → Details anzeigen =====
@app.callback(
    Output("selected-flight", "children"),
    Output("weather-box", "children"),
    Input("flights-table", "active_cell"),
    Input("flights-table", "data"),
)
def show_selected_flight(active_cell, rows):
    # Noch nichts angeklickt? Dann zwei Hinweise anzeigen
    if active_cell is None:
        return "Click a flight in the table.", "No flight selected."

    # Nummer der angeklickten Zeile
    row_number = active_cell["row"]

    # Den Flug aus dieser Zeile holen
    flight = rows[row_number]

    # Text für Box 1: nur der Flug
    flight_text = flight["flight"] + " (" + flight["airline"] + "): "
    flight_text = flight_text + flight["from"] + " → " + flight["to"]

    # Das Wetter am Zielflughafen holen
    destination = flight["to"]
    weather = WEATHER[destination]

    # Text für Box 2: nur das Wetter
    weather_text = (
        destination + ": " + str(weather["temp"]) + " °C, " + weather["condition"]
    )

    # Zwei Outputs, also zwei Werte, gleiche Reihenfolge
    return flight_text, weather_text


# ===== Callback 3: seite aktualisieren  =====
@app.callback(
    Output("last-update", "children"),
    Input("refresh-timer", "n_intervals"),
)
def show_last_update(n):

    now = datetime.now().strftime("%H:%M:%S")
    return "Last update :" + now


# ===== App starten =====
app.run(debug=True)
