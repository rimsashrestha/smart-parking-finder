
# src/produce_stream.py (updated to use recommend.py for predictions)
#-------- working version-----------#
# from recommend import load_model_and_pipeline, predict_occupancy

# from kafka import KafkaProducer
# import json
# import pandas as pd
# import time
# import random
# from datetime import datetime


# # Load model and pipeline once
# model, pipeline = load_model_and_pipeline()

# # Load static metadata of parking spots
# metadata = pd.read_csv("data/processed_parking_metadata.csv")

# # Kafka producer setup
# producer = KafkaProducer(
#     bootstrap_servers='localhost:9092',
#     value_serializer=lambda v: json.dumps(v).encode('utf-8')
# )

# print("🚀 Sending smart predictions to Kafka...")

# while True:
#     # Randomly pick a spot
#     spot = metadata.sample(1).iloc[0]

#     # Build input features
#     now = datetime.now()
#     hour = now.hour
#     dayofweek = now.weekday()
#     is_weekend = int(dayofweek >= 5)

#     features = pd.DataFrame([{
#         'hour': hour,
#         'dayofweek': dayofweek,
#         'is_weekend': is_weekend,
#         'latitude': spot['latitude'],
#         'longitude': spot['longitude'],
#         'post_id': spot['post_id'],
#         'analysis_neighborhood': spot['analysis_neighborhood'],
#         'street_name': spot['street_name'],
#         'street_num': spot['street_num']
#     }])

#     # Predict using your model
#     occupied = predict_occupancy(model, pipeline, features)

#     # Build Kafka message
#     payload = features.iloc[0].to_dict()
#     payload['timestamp'] = now.strftime('%Y-%m-%d %H:%M:%S')
#     payload['occupied'] = int(occupied)

#     # Send to Kafka
#     producer.send('parking_predictions', value=payload)
#     print(f"✅ Sent: {payload}")

#     time.sleep(1)
# #------------------------------------#

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

# # produce_stream.py
# import time
# import json
# import random
# from kafka import KafkaProducer
# from datetime import datetime
# import pandas as pd
# from recommend import load_model_and_pipeline
# from ingest import ingest_and_prepare

# producer = KafkaProducer(
#     bootstrap_servers='localhost:9092',
#     value_serializer=lambda v: json.dumps(v).encode('utf-8')
# )

# # Load model and pipeline
# model, pipeline = load_model_and_pipeline()

# # Load and prepare data
# df = ingest_and_prepare()

# print("\n🚀 Streaming started...")

# for i in range(len(df)):
#     row = df.iloc[i]

#     features = pd.DataFrame([{
#         'hour': row['hour'],
#         'dayofweek': row['dayofweek'],
#         'is_weekend': row['is_weekend'],
#     }])

#     # Apply pipeline (if needed)
#     features_transformed = pipeline.transform(features)
#     pred = model.predict(features_transformed)
#     occupied = int(pred[0] > 0.5)

#     message = {
#         'post_id': row['post_id'],
#         'street_name': row['street_name'],
#         'street_num': row['street_num'],
#         'latitude': row['latitude'],
#         'longitude': row['longitude'],
#         'analysis_neighborhood': row['analysis_neighborhood'],
#         'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#         'hour': row['hour'],
#         'dayofweek': row['dayofweek'],
#         'is_weekend': row['is_weekend'],
#         'occupied': occupied
#     }

#     producer.send('parking_predictions', value=message)
#     print(f"✅ Sent: {message}")

#     time.sleep(1)  # simulate real-time
