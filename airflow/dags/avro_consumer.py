from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import MapType, StringType
from confluent_kafka.schema_registry import SchemaRegistryClient
from fastavro import parse_schema, schemaless_reader
from io import BytesIO
import os
import json

# -------------------- Configs --------------------
KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
# KAFKA_BOOTSTRAP_SERVERS = "localhost:29092"
SCHEMA_REGISTRY_URL = os.getenv("SCHEMA_REGISTRY_URL", "http://schema-registry:8081")
# SCHEMA_REGISTRY_URL = os.getenv("SCHEMA_REGISTRY_URL", "http://localhost:8012")
TOPIC_NAME = "clickstream"
SCHEMA_SUBJECT = f"{TOPIC_NAME}-value"

# ---------------- Fetch Schema from Registry ----------------
schema_registry_conf = {'url': SCHEMA_REGISTRY_URL}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)
latest_schema = schema_registry_client.get_latest_version(SCHEMA_SUBJECT)
schema_str = latest_schema.schema.schema_str
parsed_schema = parse_schema(json.loads(schema_str))

print("✅ Avro schema fetched from Schema Registry.")

# ---------------- Spark Session ----------------
spark = SparkSession.builder \
    .appName("KafkaAvroManualDeserializer") \
    .master("spark://spark-master:7077") \
    .config("spark.jars.packages",
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,"
            "org.apache.spark:spark-avro_2.12:3.5.1") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# ---------------- UDF to Deserialize Avro ----------------
def decode_avro(binary):
    if binary is None:
        return None
    try:
        bio = BytesIO(binary[5:])  # Skip magic byte + schema ID
        record = schemaless_reader(bio, parsed_schema)
        return {k: str(v) for k, v in record.items()}
    except Exception as e:
        print(f"Deserialization error: {e}")
        return None

decode_udf = udf(decode_avro, MapType(StringType(), StringType()))

# ---------------- Kafka Stream ----------------
df_kafka = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
    .option("subscribe", TOPIC_NAME) \
    .option("startingOffsets", "latest") \
    .load()

# ---------------- Apply UDF ----------------
df_with_event = df_kafka.withColumn("event", decode_udf(col("value")))

# ---------------- Dynamically select fields ----------------
schema_json = json.loads(schema_str)
fields = [f["name"] for f in schema_json["fields"]]

df_parsed = df_with_event.select([col("event")[field].alias(field) for field in fields])

# ---------------- Output Stream ----------------
query = df_parsed.writeStream \
    .format("console") \
    .outputMode("append") \
    .option("truncate", False) \
    .start()

query.awaitTermination()
