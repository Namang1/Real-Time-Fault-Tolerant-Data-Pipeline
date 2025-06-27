from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError

# Set broker address
KAFKA_BROKER = "kafka:9092"

# Initialize Kafka admin client
admin_client = KafkaAdminClient(
    bootstrap_servers=KAFKA_BROKER,
    client_id='clickstream-admin'
)

# Define topic
topic_name = "clickstream"
num_partitions = 3
replication_factor = 1

topic = NewTopic(
    name=topic_name,
    num_partitions=num_partitions,
    replication_factor=replication_factor
)

# Create topic
try:
    admin_client.create_topics([topic])
    print(f"✅ Created topic `{topic_name}` with {num_partitions} partitions.")
except TopicAlreadyExistsError:
    print(f"⚠️ Topic `{topic_name}` already exists.")
finally:
    admin_client.close()
