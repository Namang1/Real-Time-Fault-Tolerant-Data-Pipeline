-- Flink Configs
SET 'state.backend' = 'rocksdb';
SET 'state.backend.incremental' = 'true';
SET 'execution.checkpointing.mode' = 'EXACTLY_ONCE';
SET 'execution.checkpointing.interval' = '10s';
SET 'execution.checkpointing.min-pause' = '10s';
SET 'sql-client.execution.result-mode' = 'TABLEAU';
SET 'parallelism.default' = '1';

-- Load Jars
SHOW JARS;

-- Step 1: Create Iceberg Catalog on MinIO
DROP CATALOG IF EXISTS iceberg;
CREATE CATALOG iceberg WITH (
  'type' = 'iceberg',
  'catalog-type' = 'hadoop',
  'warehouse' = 's3a://iceberg',
  'property-version' = '1',
  'fs.s3a.endpoint' = 'http://minio:9000',
  'fs.s3a.path.style.access' = 'true',
  'fs.s3a.access.key' = 'admin',
  'fs.s3a.secret.key' = 'password'
);

USE CATALOG iceberg;

-- Step 2: Create Kafka Source Table for Avro + Schema Registry
DROP TABLE IF EXISTS clickstream_source;
CREATE TABLE clickstream_source (
    event_id STRING,
    user STRING,
    action STRING,
    `timestamp` BIGINT,
    company STRING,
    ts AS TO_TIMESTAMP_LTZ(`timestamp`, 3),
    WATERMARK FOR ts AS ts - INTERVAL '5' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'clickstream',
    'properties.bootstrap.servers' = 'kafka:9092',
    'properties.schema.registry.url' = 'http://schema-registry:8081',
    'scan.startup.mode' = 'earliest-offset',
    'format' = 'avro-confluent'
);

-- Step 3: Define Iceberg Sink Table
CREATE DATABASE IF NOT EXISTS db;

DROP TABLE IF EXISTS db.filtered_clickstream;
CREATE TABLE db.filtered_clickstream (
    event_id STRING,
    user STRING,
    action STRING,
    event_time TIMESTAMP_LTZ(3),
    company STRING
) WITH (
    'format-version' = '2',
    'write.format.default' = 'parquet'
);

-- Step 4: Filter and Write
INSERT INTO db.filtered_clickstream
SELECT
    event_id,
    user,
    action,
    ts AS event_time,
    company
FROM clickstream_source
WHERE action = 'click';
