import pandas as pd
import json
from kafka import KafkaConsumer
from datetime import datetime
import os
import threading

# Path to write CSV
os.makedirs("data", exist_ok=True)
PREDICTIONS_PATH = "data/recent_predictions.csv"
parking_cache = []

def consume_and_write():
    consumer = KafkaConsumer(
        'parking_predictions',
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='latest',
        enable_auto_commit=True
    )

    for message in consumer:
        data = message.value
        try:
            data['timestamp'] = datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print(f"⚠️ Skipping bad timestamp: {data.get('timestamp')} - {e}")
            continue

        # Update parking cache
        global parking_cache
        parking_cache = [d for d in parking_cache if d['post_id'] != data['post_id']]
        parking_cache.append(data)

        # Save updated cache to CSV
        pd.DataFrame(parking_cache).to_csv(PREDICTIONS_PATH, index=False)
        print(f"✅ Saved {len(parking_cache)} predictions to {PREDICTIONS_PATH}")

if __name__ == "__main__":
    print("📡 Listening to Kafka and writing predictions to CSV...")
    threading.Thread(target=consume_and_write, daemon=True).start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user.")
