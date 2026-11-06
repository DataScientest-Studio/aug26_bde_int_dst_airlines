# Liora Airlines Dashboard

## Start
    cd src/features/dashboard
    python main.py

open in your browser: http://127.0.0.1:8050

## Structure
    dashboard/
    ├── main.py         # START: collect together and runs the app
    ├── app.py          # onlx create the Dash app
    ├── callbacks.py    # 3 callbacks (filters, row click, last update)
    ├── data.py         # sample data FLIGHTS + WEATHER: dummy data
    ├── assets/
    │   └── style.css   # design
    └── components/
        ├── __init__.py # 
        ├── header.py   # title + last update
        ├── kpis.py     # 4 KPI Box
        └── content.py  # flights table + filters + flight box + weather box

## Packages
All packages are listed in requirements.txt in the project root.