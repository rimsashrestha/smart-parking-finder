# src/produce_stream.py

import json
import random
import time
from kafka import KafkaProducer
from datetime import datetime
from recommend import load_model_and_pipeline, predict_occupancy
import pandas as pd

# Sample parking location data (you can extend this list or read from a CSV)
sample_spots = [
    {"post_id": "542-00070", "street_name": "LARKIN ST", "street_num": 7, "latitude": 37.778034, "longitude": -122.416539, "analysis_neighborhood": "Tenderloin"},
    {"post_id": "542-00071", "street_name": "MISSION ST", "street_num": 10, "latitude": 37.789012, "longitude": -122.401234, "analysis_neighborhood": "SoMa"},
    {"post_id": "542-00072", "street_name": "BROADWAY", "street_num": 200, "latitude": 37.798765, "longitude": -122.408765, "analysis_neighborhood": "North Beach"},
]

# Load model and pipeline
model, pipeline = load_model_and_pipeline()

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("🚀 Starting real-time parking data stream...")

try:
    while True:
        for spot in sample_spots:
            data = {
                "post_id": spot["post_id"],
                "street_name": spot["street_name"],
                "street_num": spot["street_num"],
                "latitude": spot["latitude"],
                "longitude": spot["longitude"],
                "analysis_neighborhood": spot["analysis_neighborhood"],
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            # Use model to predict occupancy
            prediction = predict_occupancy(model, pipeline, [data])[0]
            data["occupied"] = int(prediction)

            # Add time-based features for Kafka consumers
            dt_now = datetime.now()
            data["hour"] = dt_now.hour
            data["dayofweek"] = dt_now.weekday()
            data["is_weekend"] = int(dt_now.weekday() in [5, 6])

            producer.send('parking_predictions', value=data)
            print(f"✅ Sent: {data}")

            time.sleep(1)

except KeyboardInterrupt:
    print("🛑 Stream interrupted by user.")

