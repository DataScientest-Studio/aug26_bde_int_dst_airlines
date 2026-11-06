from dash import html

# ===== Header: Titel + last update =====
#
# main.py holt sie sich später mit "from components.header import header"
header = html.Div(
    className="header",
    children=[
        html.Div(
            children=[
                html.H1("Airlines Live Dashboard"),
                # Callback 3 (last update time)
                html.P(id="last-update", className="subtitle"),
            ],
        ),
    ],
)
