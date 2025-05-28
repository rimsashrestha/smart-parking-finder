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

# src/ingest.py

# import pandas as pd
# from datetime import datetime
# import random

# def simulate_occupancy(row):
#     # Simulate occupancy: Mark even hours as free (0), odd hours as occupied (1)
#     return 0 if row['hour'] % 2 == 0 else 1

# def load_and_prepare_data(csv_path='data/parking_data.csv'):
#     df = pd.read_csv(csv_path)

#     # Drop rows with essential missing location or time-related data
#     df = df.dropna(subset=['latitude', 'longitude', 'data_as_of', 'street_name', 'street_num'])

#     # Convert timestamp string to datetime
#     df['data_as_of'] = pd.to_datetime(df['data_as_of'])

#     # Extract features
#     df['hour'] = df['data_as_of'].dt.hour
#     df['dayofweek'] = df['data_as_of'].dt.dayofweek
#     df['is_weekend'] = df['dayofweek'].apply(lambda x: 1 if x >= 5 else 0)

#     # Simulate target variable 'occupied'
#     df['occupied'] = df.apply(simulate_occupancy, axis=1)

#     # Rename columns to standard format
#     df = df.rename(columns={
#         'post_id': 'post_id',
#         'street_name': 'street_name',
#         'street_num': 'street_num',
#         'latitude': 'latitude',
#         'longitude': 'longitude',
#         'analysis_neighborhood': 'analysis_neighborhood'
#     })

#     # Fill NaNs in analysis_neighborhood for training
#     df['analysis_neighborhood'] = df['analysis_neighborhood'].fillna('Unknown')

#     return df
