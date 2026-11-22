from datetime import UTC, datetime
from airflow.sdk import DAG, task
from airlines_dag_utils import run_project_module

with DAG(
    dag_id = "airlines_register_raw_snapshots",
    description = "Register collected raw JSON files in ingestion.raw_snapshot",
    schedule = "5,35 * * * *",
    start_date = datetime(2026, 10, 1, tzinfo=UTC),
    catchup = False,
    max_active_runs = 1,
    default_args = {"retries": 0},
    tags = ["airlines", "ingestion", "bronze"],
) as dag:

    @task(task_id = "register_raw_snapshots")
    def register_raw_snapshots() -> None:
        run_project_module("src.data.ingestors.raw_snapshots")

    register_raw_snapshots()
    