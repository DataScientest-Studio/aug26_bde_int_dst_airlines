from dash import html

# ===== KPI-Kacheln: Reihe mit 4 Feldern =====
# main.py holt sie sich später mit "from components.kpis import kpis"
kpis = html.Div(
    children=[
        # Box1: flight number
        html.Div(
            children=[html.P("Number of Flights"), html.H2(id="kpi-flights")],
            className="tile",
        ),
        # Box 2: Flights in Air
        html.Div(
            children=[html.P("in the air?"), html.H2(id="kpi-in-air")],
            className="tile",
        ),
        # Box3:Busiest destination?
        html.Div(
            children=[
                html.P("Busiest destination?"),
                html.H2(id="kpi-busiest"),
            ],
            className="tile",
        ),
        # Box 4: Avg. flight duration
        html.Div(
            children=[
                html.P("Avg. flight duration"),
                html.H2(id="kpi-duration"),
            ],
            className="tile",
        ),
    ],
    style={"display": "flex", "gap": "40px"},
)
