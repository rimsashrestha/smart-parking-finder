#src/ simulate.py
import pandas as pd
import numpy as np

def simulate_occupancy(df, start_date, end_date):
    """
    Simulates occupancy per meter per hour between two dates.
    Returns a long-format DataFrame with simulated occupancy.
    """
    timestamps = pd.date_range(start=start_date, end=end_date, freq='H')
    sim_df = df.assign(key=1).merge(pd.DataFrame({'timestamp': timestamps, 'key': 1}), on='key').drop('key', axis=1)

    def simulate(row):
        hour = row['timestamp'].hour
        if 8 <= hour < 10 or 16 <= hour < 18:
            return np.random.binomial(1, 0.9)  # Rush hour
        elif 10 <= hour < 16:
            return np.random.binomial(1, 0.6)  # Daytime
        elif 18 <= hour < 22:
            return np.random.binomial(1, 0.4)  # Evening
        else:
            return np.random.binomial(1, 0.2)  # Night

    sim_df['occupied'] = sim_df.apply(simulate, axis=1)
    sim_df['hour'] = sim_df['timestamp'].dt.hour
    sim_df['dayofweek'] = sim_df['timestamp'].dt.dayofweek
    sim_df['is_weekend'] = sim_df['dayofweek'].isin([5, 6]).astype(int)
    return sim_df


def save_simulation(sim_df, path="data/simulated_occupancy.csv"):
    sim_df.to_csv(path, index=False)
    print(f" Simulated occupancy data saved to {path}")


if __name__ == "__main__":
    df = pd.read_csv("data/parking_inventory.csv")
    sim_df = simulate_occupancy(df, "2024-05-01", "2024-05-07")
    save_simulation(sim_df)
