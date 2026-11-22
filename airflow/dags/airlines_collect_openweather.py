from datetime import UTC, datetime, timedelta
from airflow.sdk import DAG, task
from airlines_dag_utils import run_project_module

with DAG(
    dag_id = "airlines_collect_openweather",
    description = "Collect current OpenWeather observations for configured airports",
    schedule = "0 * * * *",
    start_date = datetime(2026, 10, 1, tzinfo=UTC),
    catchup = False,
    max_active_runs = 1,
    default_args = {"retries": 1, "retry_delay": timedelta(minutes=3)},
    tags = ["airlines", "collector", "openweather"]
) as dag:

    @task(task_id = "collect_weather")
    def collect_weather() -> None:
        run_project_module("src.data.collectors.collector_openweather")

    collect_weather()
