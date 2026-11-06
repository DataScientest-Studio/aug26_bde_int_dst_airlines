from dash import html, dcc

# die App aus app.py
from app import app

# die drei Bausteine aus dem Ordner components
from components.header import header
from components.kpis import kpis
from components.content import content

# Callbacks laden, damit die App sie kennt
import callbacks

# ===== Layout: die Bausteine untereinander stapeln =====
app.layout = html.Div(
    children=[
        # Timer: alle 10 Sekunden die Uhrzeit aktualisieren
        dcc.Interval(id="refresh-timer", interval=10000),
        header,
        kpis,
        content,
    ]
)

# ===== App starten =====
app.run(debug=True)
