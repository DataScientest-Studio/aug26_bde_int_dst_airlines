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

## Run with the backend
1. Create a .env file in the repo root (never commit it!) with:
   AIRLINES_DB_NAME, AIRLINES_DB_HOST, AIRLINES_DB_USER,
   AIRLINES_DB_PASSWORD, AIRLINES_DB_PORT
   Use the Supabase "Session pooler" connection (the direct
   db.xxx.supabase.co host only works with IPv6).
2. Start the backend from the repo root:
   uvicorn main:app --reload
3. Then start the dashboard in a second terminal:
    cd src\features\dashboard
    python main.py