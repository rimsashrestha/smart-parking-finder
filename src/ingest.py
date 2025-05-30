# src/ingest.py

import pandas as pd
import os

def load_sf_parking_data():
    print("Downloading parking data from SF Open Data...")
    url = "https://data.sfgov.org/resource/8vzz-qzz9.csv"
    try:
        df = pd.read_csv(url)
    except Exception as e:
        print(f" Error fetching data: {e}")
        return None

    # Filter useful columns
    cols = ['post_id', 'street_name', 'street_num', 'latitude', 'longitude', 'analysis_neighborhood']
    df = df[cols].dropna()
    df['latitude'] = df['latitude'].astype(float)
    df['longitude'] = df['longitude'].astype(float)
    print(f"Retrieved {len(df)} valid parking meter records")
    return df

def save_data(df, path="data/parking_inventory.csv"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Saved dataset to {path}")

if __name__ == "__main__":
    df = load_sf_parking_data()
    if df is not None:
        save_data(df)


