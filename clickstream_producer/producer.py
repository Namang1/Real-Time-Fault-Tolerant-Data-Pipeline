from kafka import KafkaProducer
import json
import time
import random
import uuid

producer = KafkaProducer(
    bootstrap_servers='localhost:29092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    key_serializer=lambda v: str(v).encode('utf-8'),
    acks='all',
    enable_idempotence=True  # ensures no duplicates
)

users = ['user1', 'user2', 'user3']

def generate_event():
    return {
        "event_id": str(uuid.uuid4()),
        "user": random.choice(users),
        "action": random.choice(['click', 'view', 'scroll']),
        "timestamp": int(time.time() * 1000)
    }

while True:
    event = generate_event()
    producer.send(
        topic='clickstream',
        key=event['event_id'],
        value=event
    )
    print("Sent:", event)
    time.sleep(1)
