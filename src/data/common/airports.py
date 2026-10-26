import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

AIRPORTS_FILE = (
    PROJECT_ROOT / "data" / "reference_data" / "airports.json"
)

def load_airports():
    with AIRPORTS_FILE.open(encoding="utf-8") as file:
        return json.load(file)