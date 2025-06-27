from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from datetime import datetime

default_args = {
    "start_date": datetime(2025, 6, 27),
}

with DAG(
    dag_id="consume_avro_kafka_dag",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    description="Submit a Spark job to consume Avro from Kafka using Schema Registry",
) as dag:

    submit_spark_job = DockerOperator(
        task_id="submit_spark_job",
        image="bitnami/spark:3.5.1",
        command="""
/opt/bitnami/spark/bin/spark-submit \
--master spark://spark-master:7077 \
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,\
org.apache.spark:spark-avro_2.12:3.5.1,\
io.confluent:kafka-schema-registry-client:7.5.0,\
io.confluent:kafka-avro-serializer:7.5.0 \
/opt/airflow/dags/avro_consumer.py
""",
        network_mode="spark-network",
        mounts=[
            Mount(source="/opt/airflow/dags", target="/opt/airflow/dags", type="bind")
        ],
        docker_url="unix://var/run/docker.sock",
        api_version="auto",
        auto_remove=True,
    )

    submit_spark_job
