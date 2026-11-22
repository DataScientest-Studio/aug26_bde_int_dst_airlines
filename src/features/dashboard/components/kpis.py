from dash import html

# ===== KPI-Kacheln: Reihe mit 4 Feldern =====
# main.py holt sie sich später mit "from components.kpis import kpis"
kpis = html.Div(
    children=[
        # Box 1: flight number
        html.Div(
            children=[html.P("Number of Flights"), html.H2(id="kpi-flights")],
            className="tile",
        ),
        # Box 2:Busiest destination?
        html.Div(
            children=[
                html.P("Busiest destination?"),
                html.H2(id="kpi-busiest"),
            ],
            className="tile",
        ),
    ],
    style={"display": "flex", "gap": "40px"},
)
