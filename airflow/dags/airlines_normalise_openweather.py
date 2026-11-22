from datetime import UTC, datetime
from airflow.sdk import DAG, task
from airlines_dag_utils import run_project_module

with DAG(
    dag_id = "airlines_normalise_openweather",
    description = "Run normalisation for OpenWeather snapshots",
    schedule = "15 * * * *",
    start_date = datetime(2026, 10, 1, tzinfo=UTC),
    catchup = False,
    max_active_runs = 1,
    default_args = {"retries": 0},
    tags = ["airlines", "normalisation", "silver"]
) as dag:

    @task(task_id = "normalise_openweather_snapshots")
    def normalise_openweather_snapshots() -> None:
        run_project_module("src.data.ingestors.openweather")

    normalise_openweather_snapshots()
    