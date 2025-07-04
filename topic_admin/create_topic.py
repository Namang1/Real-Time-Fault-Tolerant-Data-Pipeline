from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError

KAFKA_BROKER = "kafka:9092"

admin_client = KafkaAdminClient(
    bootstrap_servers=KAFKA_BROKER,
    client_id='clickstream-admin'
)

topic_name = "clickstream"
num_partitions = 3
replication_factor = 1

topic = NewTopic(
    name=topic_name,
    num_partitions=num_partitions,
    replication_factor=replication_factor
)

try:
    admin_client.create_topics([topic])
    print(f"✅ Created topic `{topic_name}` with {num_partitions} partitions.")
except TopicAlreadyExistsError:
    print(f"⚠️ Topic `{topic_name}` already exists.")
finally:
    admin_client.close()



# bin/sql-client.sh -f /opt/sql_jobs/flink_sql_job.sql

# bin/sql-client.sh \
#   --jar /opt/flink/lib/ext/flink-connector-kafka-1.17.0.jar \
#   --jar /opt/flink/lib/ext/flink-sql-avro-1.17.0.jar \
#   --jar /opt/flink/lib/ext/iceberg-flink-runtime-1.17-1.4.3.jar \
#   --jar /opt/flink/lib/ext/hadoop-aws-3.3.5.jar \
#   --jar /opt/flink/lib/ext/hadoop-common-3.3.5.jar \
#   --jar /opt/flink/lib/ext/hadoop-hdfs-3.3.5.jar \
#   --jar /opt/flink/lib/ext/hadoop-auth-3.3.5.jar \
#   --jar /opt/flink/lib/ext/aws-java-sdk-bundle-1.12.525.jar \
#   -f /opt/sql_jobs/flink_sql_job.sql
