
# src/shap_explain.py

import pandas as pd
import shap
import joblib
import matplotlib.pyplot as plt

# Load the same feature columns used in prediction
FEATURES = ['hour', 'dayofweek', 'is_weekend', 'latitude', 'longitude']

def load_data(path='data/simulated_occupancy.csv'):
    """Load the simulated dataset used for model training."""
    df = pd.read_csv(path)
    return df[FEATURES], df['occupied']

def load_model(path='models/random_forest_model.pkl'):
    """Load the trained model from disk."""
    return joblib.load(path)

def explain_model(model, X):
    print("⚡ Running SHAP explainability...")
    explainer = shap.Explainer(model, X)

    # Sample a small subset to speed up and avoid memory/accuracy errors
    X_sample = X.sample(2000, random_state=42)

    shap_values = explainer(X_sample, check_additivity=False)  # <-- Disable strict check
    shap.summary_plot(shap_values, X_sample, feature_names=FEATURES)
    plt.tight_layout()
    plt.savefig("outputs/shap_summary_plot.png")
    print(" SHAP plot saved to outputs/shap_summary_plot.png")


if __name__ == "__main__":
    X, y = load_data()
    model = load_model()
    explain_model(model, X)
