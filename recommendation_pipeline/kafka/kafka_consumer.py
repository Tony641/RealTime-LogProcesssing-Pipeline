import json
import psycopg2
from kafka import KafkaConsumer

DATABASE_URL = "postgresql://user:password@localhost:5432/recommendations"

consumer = KafkaConsumer(
    "user_activity",
    "search_events",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
)

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

for message in consumer:
    data = message.value
    if "search_query" in data:
        cursor.execute("INSERT INTO search_events (user_id, search_query, timestamp) VALUES (%s, %s, %s)",
                       (data["user_id"], data["search_query"], data["timestamp"]))
    else:
        cursor.execute("INSERT INTO user_activity (user_id, product_id, event_type, timestamp) VALUES (%s, %s, %s, %s)",
                       (data["user_id"], data["product_id"], data["event_type"], data["timestamp"]))
    
    conn.commit()
    print(f"Stored: {data}")
