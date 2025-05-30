#src/predict.py
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pandas as pd
import joblib
import os

def train_rf_model(df):
    """
    Train a Random Forest Classifier to predict occupancy.
    Returns the trained model and feature list.
    """
    features = ['hour', 'dayofweek', 'is_weekend', 'latitude', 'longitude']
    X = df[features]
    y = df['occupied']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    print("\n Random Forest Classification Report:")
    print(classification_report(y_test, y_pred))

    return model, features

# Run model training and save
if __name__ == "__main__":
    df = pd.read_csv("data/simulated_occupancy.csv")
    model, features = train_rf_model(df)

    # Save model
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/random_forest_model.pkl")
    print("Model saved to models/random_forest_model.pkl")
