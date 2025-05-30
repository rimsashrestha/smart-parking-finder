
#src/recommend.py
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from xgboost import XGBClassifier
from datetime import datetime
import os

def load_and_prepare_data():
    df = pd.read_csv('data/parking_data.csv')

    # Drop rows missing essential geographic or identifying info
    df = df.dropna(subset=['longitude', 'latitude', 'street_name', 'street_num', 'analysis_neighborhood'])

    # Simulate a timestamp (since this dataset is static)
    df['timestamp'] = pd.to_datetime('2025-05-27 20:00:00') + pd.to_timedelta(np.random.randint(0, 3600, size=len(df)), unit='s')

    # Simulate occupancy (0 or 1) based on arbitrary logic or randomness
    df['occupied'] = np.random.choice([0, 1], size=len(df))

    # Feature engineering: hour, day of week, is_weekend
    df['hour'] = df['timestamp'].dt.hour
    df['dayofweek'] = df['timestamp'].dt.dayofweek
    df['is_weekend'] = df['dayofweek'].apply(lambda x: 1 if x >= 5 else 0)

    return df

def build_pipeline():
    numeric_features = ['hour', 'dayofweek', 'is_weekend', 'street_num']
    categorical_features = ['street_name']

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ]
    )

    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor)
    ])

    return pipeline

def train_and_save_model():
    df = load_and_prepare_data()
    pipeline = build_pipeline()

    X = df[['hour', 'dayofweek', 'is_weekend', 'street_num', 'street_name']]
    y = df['occupied']

    X_transformed = pipeline.fit_transform(X)
    model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    model.fit(X_transformed, y)

    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/xgb_model.joblib')
    joblib.dump(pipeline, 'models/pipeline.joblib')
    print("✅ Model and pipeline saved successfully.")

def load_model_and_pipeline():
    model_path = 'models/xgb_model.joblib'
    pipeline_path = 'models/pipeline.joblib'

    if not os.path.exists(model_path) or not os.path.exists(pipeline_path):
        print("❗ Model files not found. Training new model...")
        train_and_save_model()

    model = joblib.load(model_path)
    pipeline = joblib.load(pipeline_path)
    return model, pipeline

def predict_occupancy(model, pipeline, new_data):
    df = pd.DataFrame(new_data)

    # Simulate time-based features
    df['hour'] = datetime.now().hour
    df['dayofweek'] = datetime.now().weekday()
    df['is_weekend'] = int(df['dayofweek'].iloc[0] in [5, 6])

    X = df[['hour', 'dayofweek', 'is_weekend', 'street_num', 'street_name']]
    X_transformed = pipeline.transform(X)

    preds = model.predict(X_transformed)
    return preds

# Run this to test and train if needed
if __name__ == "__main__":
    train_and_save_model()

