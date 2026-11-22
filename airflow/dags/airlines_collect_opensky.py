from datetime import UTC, datetime, timedelta
from airflow.sdk import DAG, task
from airlines_dag_utils import run_project_module

with DAG(
    dag_id = "airlines_collect_opensky",
    description = "Collect OpenSky state vectors for configured airports",
    schedule = "*/30 * * * *",
    start_date = datetime(2026, 10, 1, tzinfo=UTC),
    catchup = False,
    max_active_runs = 1,
    default_args = {"retries": 1, "retry_delay": timedelta(minutes=3)},
    tags = ["airlines", "collector", "opensky"]
) as dag:

    @task(task_id = "collect_states")
    def collect_states() -> None:
        run_project_module("src.data.collectors.collector_opensky")

    collect_states()