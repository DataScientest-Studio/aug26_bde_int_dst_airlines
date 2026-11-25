from dash import html, dcc, dash_table
from datetime import date
from data import get_airport_options, get_time_options

# ===== Inhalt: links Tabelle mit Filtern, rechts Flug-Box + Wetter-Box =====
# main.py holt ihn sich später mit "from components.content import content"
content = html.Div(
    children=[
        # ----- linke Spalte: Filter + Tabelle -----
        html.Div(
            className="tile",
            children=[
                html.H3("Flights"),  # Box-Titel
                # Suche, Airport, Datum und Uhrzeit nebeneinander
                html.Div(
                    className="filter-row",
                    children=[
                        # Suche nach Callsign
                        html.Div(
                            children=[
                                html.Label("Search"),
                                dcc.Input(
                                    id="search-callsign",
                                    type="text",
                                    placeholder="Search callsign, e.g. DLH123",
                                    className="search-box",
                                ),
                            ],
                        ),
                        # Filter: Airport
                        html.Div(
                            children=[
                                html.Label("Airport"),
                                dcc.Dropdown(
                                    id="filter-airport",
                                    options=get_airport_options(),
                                    placeholder="All airports",
                                ),
                            ],
                            style={"width": "180px"},
                        ),
                        # Filter: Datum
                        html.Div(
                            children=[
                                html.Label("Date"),
                                dcc.DatePickerSingle(
                                    id="filter-date", date=date.today()
                                ),
                            ],
                            style={"width": "140px"},
                        ),
                        # Filter: time from
                        html.Div(
                            children=[
                                html.Label("From"),
                                dcc.Dropdown(
                                    id="filter-time-from",
                                    options=get_time_options(),
                                    placeholder="00:00",
                                ),
                            ],
                            style={"width": "110px"},
                        ),
                        # Filter: time to
                        html.Div(
                            children=[
                                html.Label("To"),
                                dcc.Dropdown(
                                    id="filter-time-to",
                                    options=get_time_options(),
                                    placeholder="23:59",
                                ),
                            ],
                            style={"width": "110px"},
                        ),
                    ],
                ),
                # Hinweis, wenn keine Flüge gefunden werden
                html.P(id="no-flights-message"),
                # NEU: Lade-Kreisel
                dcc.Loading(
                    type="circle",
                    children=[
                        # Flug-Tabelle
                        dash_table.DataTable(
                            id="flights-table",
                            sort_action="native",
                            page_size=10,
                            columns=[
                                # content from data.py
                                {"name": "Callsign", "id": "callsign"},
                                {"name": "Status", "id": "status"},
                                {"name": "Altitude (m)", "id": "altitude"},
                                {"name": "Speed (km/h)", "id": "speed"},
                                {"name": "Airport", "id": "airport"},
                                {"name": "City", "id": "city"},
                                {"name": "Last contact", "id": "last_contact"},
                                {"name": "Temp (°C)", "id": "temp"},
                                {"name": "Weather", "id": "weather"},
                            ],
                            style_header={
                                "backgroundColor": "white",
                                "color": "#222222",
                                "fontWeight": "bold",
                                "borderBottom": "2px solid #dddddd",
                            },
                            style_cell={
                                "padding": "10px",
                                "textAlign": "left",
                                "fontFamily": "Arial",
                                "border": "none",
                                "borderBottom": "1px solid #eeeeee",
                            },
                            style_data_conditional=[
                                {
                                    "if": {"filter_query": '{status} = "Landed"'},
                                    "color": "green",
                                },
                                {
                                    "if": {"filter_query": '{status} = "In the air"'},
                                    "color": "#1f6fd1",
                                },
                            ],
                        ),
                    ],
                ),
            ],
            style={"flex": "3"},  # 3 Teile breit
        ),
        # ----- rechte Spalte: Flug-Box + Wetter-Box -----
        html.Div(
            children=[
                # Box 1: Details zum angeklickten Flug
                html.Div(
                    children=[
                        html.H3("Selected flight"),
                        html.Div(id="selected-flight"),
                    ],
                    className="tile",
                ),
                # Box 2: Wetter am Flughafen
                html.Div(
                    children=[
                        html.H3("Weather at airport"),
                        html.Div(id="weather-box"),
                    ],
                    className="tile",
                ),
            ],
            style={"flex": "1"},
        ),
    ],
    style={"display": "flex", "gap": "20px", "margin-top": "20px"},
)
