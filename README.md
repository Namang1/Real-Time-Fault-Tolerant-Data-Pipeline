# 🔥 Real-Time Clickstream Fault-Tolerant Data Pipeline

This project is a full-fledged real-time analytics pipeline that ingests, processes, stores, and visualizes clickstream data using **Kafka**, **Avro**, **Flink**, **Spark**, **Iceberg**, **Trino**, **Superset**, and **Airflow** — all containerized via **Docker Compose**. **Jupyter** is included for development and prototyping.

## 🏗️ Architecture Overview

1. **Kafka + Schema Registry**: Ingests Avro-encoded clickstream data.
2. **Clickstream Producer**: Generates synthetic Avro clickstream events.
3. **Flink SQL Client**: Real-time Avro-to-Iceberg transformation.
4. **Spark Structured Streaming** (optional): Alternative batch + stream consumer.
5. **Iceberg + MinIO**: S3-compatible lakehouse table format with schema evolution.
6. **Hive Metastore**: Metadata management for Iceberg.
7. **Trino**: Query engine for Iceberg datasets.
8. **Superset**: Visualization layer over Trino.
9. **Airflow**: DAG orchestration for Spark/Flink jobs.
10. **Jupyter Notebook**: Interactive development and prototyping.

## 📦 Services

- `Kafka`, `Zookeeper`, `Schema Registry`
- `Clickstream Producer`
- `Flink` (JobManager, TaskManager, SQL Client)
- `Spark` (Master, Workers - commented out for resource optimization)
- `Iceberg` backed by `MinIO`
- `Trino` configured for Iceberg REST catalog
- `Superset` dashboard
- `Airflow` for orchestration
- `Jupyter` notebook (commented but supported)

## 🔧 Getting Started

```bash
# Start all services
docker-compose up -d --build

# View logs for a specific container
docker logs -f flink-taskmanager
```

## 💡 Development

- Use the **Jupyter Notebook** container for rapid prototyping and development (`pyspark` + Kafka + Avro).
- **Airflow** handles orchestration of the batch jobs.
- **Flink SQL Client** executes streaming transformations with fault tolerance.

## 🧠 Schema Evolution

- Avro-encoded messages from Kafka support **schema evolution** using **Confluent Schema Registry**.
- Iceberg handles changes like column additions without downtime.

## 📊 Visualization

- Superset + Trino query Iceberg tables in MinIO.
- Dynamic exploration of clickstream metrics, aggregations, and visual dashboards.

## 📄 Example Query

```sql
SELECT page, COUNT(*) as views
FROM iceberg.clickstream_data
WHERE action = 'click'
GROUP BY page;
```

## 📌 Resume Line

> **Built a containerized real-time data pipeline** using Kafka, Schema Registry, Apache Flink SQL, Spark Structured Streaming, Iceberg, Trino, and Superset to ingest and process Avro-encoded clickstream data with schema evolution and fault tolerance. Orchestrated data workflows using Airflow and explored development in Jupyter.

## 📂 Folder Structure

```
.
├── clickstream_producer/
├── topic_admin/
├── airflow/
├── flink/
│   ├── sql-client/
│   └── sql-jobs/
├── trino/
│   └── etc/
├── superset/
└── docker-compose.yml
```

## 🧰 Tools Used

- Kafka, Avro, Schema Registry
- Apache Flink 1.18.1 (SQL client)
- Apache Spark 3.3.1 (commented)
- Iceberg with REST catalog + MinIO
- Trino 440
- Apache Superset
- Apache Airflow 2.9.1
- Jupyter (pyspark-notebook)