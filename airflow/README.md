Airflow orchestration

This directory contains a containerised Apache Airflow deployment for the
existing collectors and ingestion pipeline. 
Airflow orchestrates the project modules; it does not duplicate their data-processing logic.

Architecture:
- Airflow DAG task
- python -m src.data....
- collector writes data|raw|... JSON
- raw-snapshot registration -> ingestion.raw_snapshot
- source-specific normalisation -> public tables in Supabase



Airflow metadata is stored in its own local PostgreSQL container (airflow-db).

DAGs:
All schedules use UTC. DAGs are created paused by default.
DAG|Schedule|Module
airlines_collect_opensky|every 30 minutes|src.data.collectors.collector_opensky
airlines_collect_openweather|hourly at :00|src.data.collectors.collector_openweather
airlines_register_raw_snapshots|at :05 and :35|src.data.ingestors.raw_snapshots
airlines_normalise_openweather|hourly at :15|src.data.ingestors.openweather
airlines_normalise_opensky|at :15 and :45|src.data.ingestors.opensky


Volumes: 
Host path | Container path | Purpose
airflow/dags/ | /opt/airflow/dags | DAG definitions
data/raw/ | /opt/airlines/data/raw | Persistent raw JSON
.env | /opt/airlines/.env (read-only) | OpenWeather and Supabase settings
Docker volume | /opt/airflow/logs | Airflow task logs


The Docker image contains only src/, data/reference_data/, and the
dependencies in airflow/requirements.txt. It does not contain credentials or raw data.

First-time setup:
$ cp airflow/.env.template airflow/.env
$ mkdir -p data/raw
$ chmod 600 airflow/.env

Configure these values in airflow/.env:
- AIRFLOW_UID: result of '$id -u' on Linux/macOS.
- AIRFLOW_METADATA_DB_PASSWORD: password for Airflow's local PostgreSQL.
- AIRFLOW_ADMIN_*: credentials for the Airflow UI.
- AIRFLOW_FERNET_KEY: stable encryption key for Airflow metadata.
- AIRFLOW_JWT_SECRET: stable random API/UI signing secret.
- AIRFLOW_WEB_PORT: host port for the UI.
The project-root .env must also exist because the collector and ingestion
modules use it for OpenWeather and Supabase credentials.


Build and start:
$ docker compose --env-file airflow/.env -f docker-compose.airflow.yml build
$ docker compose --env-file airflow/.env -f docker-compose.airflow.yml up airflow-init
$ docker compose --env-file airflow/.env -f docker-compose.airflow.yml up -d

Open the UI at http://localhost:8080.
airflow-init is expected to exit with code 0: it applies Airflow metadata
migrations and creates the configured administrator.

Stop:
$ docker compose --env-file airflow/.env -f docker-compose.airflow.yml down

This preserves Airflow metadata and task logs in Docker volumes. Do not use
down -v unless you intentionally want to remove Airflow execution history.