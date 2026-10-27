import json
import os
import tempfile

from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
BASE_DIR = PROJECT_ROOT / "data" / "raw"

def save_json(provider, resource, airport_code, data):
  timestamp = datetime.now(timezone.utc)
  
  directory = BASE_DIR / provider / resource / f"airport={airport_code}"
  directory.mkdir(parents=True, exist_ok=True)

  filename = (
	f"{timestamp:%Y-%m-%dT%H%M%S%fZ}.json"
	#f"_{uuid4().hex[:8]}.json"
  )

  filepath = directory /filename

  # write to a temp file first
  # if the process crashes, we won't have imcomplete/corrupted JSON files
  temp_path = None

  try:
    with tempfile.NamedTemporaryFile(
      mode="w",
      encoding="utf-8",
      dir = directory,
      suffix = ".tmp",
      delete = False
    ) as temp:
      temp_path = Path(temp.name)
      json.dump(data, temp, ensure_ascii=False, indent=2)

    os.replace(temp_path, filepath)

  finally:
    if temp_path is not None:
      temp_path.unlink(missing_ok=True)

  print(f"Saved: {filepath}", flush=True)

  return filepath
