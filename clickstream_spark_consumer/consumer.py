from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, LongType

# Define schema based on producer message
schema = StructType() \
    .add("user_id", StringType()) \
    .add("page", StringType()) \
    .add("timestamp", LongType())

# Initialize Spark session with Delta support
spark = SparkSession.builder \
    .appName("ClickstreamConsumer") \
    .config("spark.sql.shuffle.partitions", "2") \
    .config("spark.sql.streaming.checkpointLocation", "./checkpoints/clickstream") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Read from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "clickstream") \
    .option("startingOffsets", "earliest") \
    .load()

# Parse JSON
json_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Write to Delta Lake (or Parquet)
output_path = "../data/delta/clickstream"

query = json_df.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "./checkpoints/clickstream") \
    .start(output_path)

query.awaitTermination()
