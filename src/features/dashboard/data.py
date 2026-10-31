# ===== data.py: alle Daten  =====


# Beispiel-Flüge
FLIGHTS = [
    {
        "flight": "LH400",
        "airline": "Lufthansa",
        "from": "FRA",
        "to": "JFK",
        "departure": "10:15",
        "arrival": "13:05",
        "status": "In the air",
        "icao24": "3c6444",
        "date": "2026-11-01",
    },
    {
        "flight": "LH123",
        "airline": "Lufthansa",
        "from": "MUC",
        "to": "CDG",
        "departure": "07:40",
        "arrival": "09:20",
        "status": "Landed",
        "icao24": "391558",
        "date": "2026-10-31",
    },
    {
        "flight": "LX318",
        "airline": "Swiss",
        "from": "ZRH",
        "to": "LHR",
        "departure": "11:30",
        "arrival": "12:10",
        "status": "In the air",
        "icao24": "40621d",
        "date": "2026-10-31",
    },
    {
        "flight": "OS201",
        "airline": "Austrian",
        "from": "VIE",
        "to": "MAD",
        "departure": "16:45",
        "arrival": "20:10",
        "status": "Scheduled",
        "icao24": "a80140",
        "date": "2026-10-31",
    },
]

# Beispiel-Wetter pro Zielflughafen
WEATHER = {
    "JFK": {"temp": 12, "condition": "Cloudy"},
    "CDG": {"temp": 15, "condition": "Sunny"},
    "LHR": {"temp": 10, "condition": "Rain"},
    "MAD": {"temp": 22, "condition": "Sunny"},
}
