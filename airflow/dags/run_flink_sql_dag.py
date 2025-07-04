from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id='run_flink_sql_job',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@hourly',
    catchup=False,
) as dag:

    run_flink_sql = BashOperator(
        task_id='run_sql_job',
        bash_command='/opt/flink/bin/sql-client.sh -f /opt/flink/clickstream-filtering.sql'
    )
