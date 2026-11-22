ARG AIRFLOW_VERSION=3.4.0
FROM apache/airflow:${AIRFLOW_VERSION}-python3.12

ARG AIRFLOW_VERSION

COPY --chown=airflow:root airflow/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /tmp/requirements.txt

COPY --chown=airflow:root src /opt/airlines/src
COPY --chown=airflow:root data/reference_data /opt/airlines/data/reference_data

ENV AIRLINES_PROJECT_ROOT=/opt/airlines
ENV PYTHONPATH=/opt/airlines
WORKDIR /opt/airlines
