from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(
    os.environ.get("AIRLINES_PROJECT_ROOT", "/opt/airlines")
).resolve()


def run_project_module(module_name: str) -> None:
    """Run one project module and propagate a non-zero exit code to Airflow."""
    if not PROJECT_ROOT.is_dir():
        raise RuntimeError(f"Project root does not exist: {PROJECT_ROOT}")

    environment = os.environ.copy()
    existing_pythonpath = environment.get("PYTHONPATH")
    environment["PYTHONPATH"] = (f"{PROJECT_ROOT}:{existing_pythonpath}"
                                if existing_pythonpath else str(PROJECT_ROOT))

    subprocess.run(
        [sys.executable, "-m", module_name],
        cwd=PROJECT_ROOT,
        env=environment,
        check=True,
    )
