#src/consume_predict
import json
import pandas as pd
from kafka import KafkaConsumer
import joblib
from sklearn.ensemble import RandomForestClassifier

# Load model
model = joblib.load("models/random_forest_model.pkl")
FEATURES = ['hour', 'dayofweek', 'is_weekend', 'latitude', 'longitude']

# Kafka consumer
consumer = KafkaConsumer(
    'parking-updates',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print(" Listening for real-time parking updates...")

for message in consumer:
    record = message.value

    # Prepare features for prediction
    try:
        X = pd.DataFrame([record])[FEATURES]
        prediction = model.predict(X)[0]
        prob = model.predict_proba(X)[0][1]

        print(f"📍 Spot {record['post_id']} predicted occupied: {prediction} (Prob={prob:.2f})")

        if prob < 0.3:
            print(f"✅ ALERT: High chance of free spot at {record['street_name']} #{record['street_num']}")

    except Exception as e:
        print(f" !! Error processing record: {e}")
