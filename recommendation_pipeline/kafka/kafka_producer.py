import json
import random
import time
from kafka import KafkaProducer
from faker import Faker

fake = Faker()
KAFKA_BROKER = "localhost:9092"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

def generate_user_event():
    return {
        "user_id": fake.uuid4(),
        "product_id": fake.uuid4(),
        "event_type": random.choice(["click", "view", "purchase"]),
        "timestamp": int(time.time()),
        "metadata": {"device": random.choice(["mobile", "desktop", "tablet"])},
    }

def generate_search_event():
    return {
        "user_id": fake.uuid4(),
        "search_query": fake.word(),
        "timestamp": int(time.time()),
    }

def produce_events(n=100):
    for _ in range(n):
        producer.send("user_activity", generate_user_event())
        producer.send("search_events", generate_search_event())
        time.sleep(random.uniform(0.1, 1.0))

if __name__ == "__main__":
    produce_events()
