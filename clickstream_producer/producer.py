from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import StringSerializer

import time, uuid, random

schema_registry_conf = {
    'url': 'http://schema-registry:8081'
    # 'url': 'http://localhost:8012'
}
print(schema_registry_conf)
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

value_schema_str = """
{
  "type": "record",
  "name": "ClickEvent",
  "namespace": "com.example",
  "fields": [
    {"name": "event_id", "type": "string"},
    {"name": "user", "type": "string"},
    {"name": "action", "type": "string"},
    {"name": "timestamp", "type": "long"},
    {"name": "company", "type": "string", "default": ""}
  ]
}
"""
print(value_schema_str)
# Serializer
avro_serializer = AvroSerializer(
    schema_str=value_schema_str,
    schema_registry_client=schema_registry_client,
    to_dict=lambda obj, ctx: obj
)

producer_conf = {
    'bootstrap.servers': 'kafka:9092',
    'key.serializer': StringSerializer('utf_8'),
    'value.serializer': avro_serializer
}

producer = SerializingProducer(producer_conf)

while True:
    event = {
        "event_id": str(uuid.uuid4()),
        "user": random.choice(["user1", "user2"]),
        "action": random.choice(["click", "scroll"]),
        "timestamp": int(time.time() * 1000),
        "company": random.choice(["google", "microsoft"]),
    }

    producer.produce(topic="clickstream", key=event["event_id"], value=event)
    print("Sent:", event)

    producer.poll(0)
    time.sleep(1)
