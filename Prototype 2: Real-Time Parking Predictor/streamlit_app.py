# # streamlit_app.py

# import streamlit as st
# from kafka import KafkaConsumer
# from geopy.distance import geodesic
# from datetime import datetime, timedelta
# from streamlit_folium import st_folium
# import folium
# import threading
# import json
# import time
# import math

# # Global cache to store live predictions
# parking_cache = []

# # Background Kafka consumer
# def consume_kafka():
#     consumer = KafkaConsumer(
#         'parking_predictions',
#         bootstrap_servers='localhost:9092',
#         value_deserializer=lambda m: json.loads(m.decode('utf-8')),
#         auto_offset_reset='latest',
#         enable_auto_commit=True
#     )
#     for message in consumer:
#         data = message.value
#         try:
#             data['timestamp'] = datetime.strptime(data['timestamp'], "%Y-%m-%d %H:%M:%S")
#         except:
#             continue
#         global parking_cache
#         parking_cache = [d for d in parking_cache if d['post_id'] != data['post_id']]
#         parking_cache.append(data)

# # Start Kafka thread only once
# if "kafka_started" not in st.session_state:
#     threading.Thread(target=consume_kafka, daemon=True).start()
#     st.session_state.kafka_started = True

# # Utility to find nearest available spots
# def get_top_spots(user_lat, user_lon, top_n):
#     now = datetime.now()
#     recent = [
#         d for d in parking_cache
#         if d['occupied'] == 0 and isinstance(d.get('timestamp'), datetime)
#         and (now - d['timestamp']) < timedelta(hours=24)
#     ]
#     for d in recent:
#         d['distance'] = geodesic((user_lat, user_lon), (d['latitude'], d['longitude'])).meters
#     return sorted(recent, key=lambda x: x['distance'])[:top_n]

# # Streamlit App UI
# st.set_page_config(page_title="Smart Parking", layout="wide")

# st.sidebar.title("🔍 Your Location")
# latitude = st.sidebar.number_input("Latitude", value=37.79, step=0.0001, format="%.5f")
# longitude = st.sidebar.number_input("Longitude", value=-122.41, step=0.0001, format="%.5f")
# top_n = st.sidebar.slider("How many spots to show?", 1, 10, 3)

# st.markdown("## 🚗 Smart Parking Spot Recommender")

# top_spots = get_top_spots(latitude, longitude, top_n)

# if not top_spots:
#     st.error("No available spots found in the past 24 hours.")
# else:
#     st.success(f"Top {len(top_spots)} spots near ({latitude}, {longitude}):")

#     m = folium.Map(location=[latitude, longitude], zoom_start=14)
#     folium.Marker(location=[latitude, longitude], tooltip="📍 You are here", icon=folium.Icon(color='blue')).add_to(m)

#     for i, spot in enumerate(top_spots, 1):
#         drive_time = math.ceil(spot["distance"] / 500)  # 500m per min
#         popup = f"{i}. {spot['street_name']} #{spot['street_num']}<br>{round(spot['distance'],1)}m — ~{drive_time} min drive"
#         folium.Marker(
#             location=[spot["latitude"], spot["longitude"]],
#             popup=popup,
#             icon=folium.Icon(color="green" if drive_time < 5 else "orange")
#         ).add_to(m)

#     st_folium(m, width=800, height=500)

#     st.markdown("---")
#     st.markdown("### 📋 Spot Details")
#     for i, s in enumerate(top_spots, 1):
#         drive_time = math.ceil(s["distance"] / 500)
#         day_type = "Weekend" if s.get("is_weekend") else "Weekday"
#         st.markdown(
#             f"""
#             **{i}. {s['street_name']} #{s['street_num']} ({s['analysis_neighborhood']})**
#             - 🕓 Last Updated: {s['timestamp'].strftime('%Y-%m-%d %H:%M:%S')} — {day_type}
#             - 📏 Distance: {round(s['distance'], 1)} meters (~{drive_time} min drive)
#             """
#         )

# streamlit_app.py

# import streamlit as st
# from streamlit_folium import st_folium
# import folium
# from kafka import KafkaConsumer
# import json
# from datetime import datetime, timedelta
# from geopy.distance import geodesic
# import math

# # -----------------------------
# # Global cache of parking spots
# # -----------------------------
# parking_cache = []

# # -----------------------------
# # Kafka consumer loader (non-cached to avoid lambda pickle issues)
# # -----------------------------
# def load_consumer():
#     return KafkaConsumer(
#         'parking_predictions',
#         bootstrap_servers='localhost:9092',
#         value_deserializer=lambda m: json.loads(m.decode('utf-8')),
#         auto_offset_reset='latest',
#         enable_auto_commit=True
#     )

# # -----------------------------
# # Load messages into parking_cache
# # -----------------------------
# def fetch_parking_data(consumer, max_messages=50):
#     global parking_cache
#     count = 0
#     for message in consumer:
#         data = message.value
#         try:
#             data['timestamp'] = datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S')
#         except Exception:
#             continue
#         parking_cache = [d for d in parking_cache if d['post_id'] != data['post_id']]
#         parking_cache.append(data)
#         count += 1
#         if count >= max_messages:
#             break

# # -----------------------------
# # Find nearest available parking spots
# # -----------------------------
# def find_nearest_available(user_lat, user_lon, top_n=5):
#     now = datetime.now()
#     recent_data = [
#         d for d in parking_cache
#         if d['occupied'] == 0 and isinstance(d.get('timestamp'), datetime)
#         and (now - d['timestamp']) < timedelta(hours=24)
#     ]

#     for d in recent_data:
#         d['distance'] = geodesic((user_lat, user_lon), (d['latitude'], d['longitude'])).meters

#     sorted_spots = sorted(recent_data, key=lambda x: x['distance'])
#     return sorted_spots[:top_n]

# # -----------------------------
# # Streamlit UI Setup
# # -----------------------------
# st.set_page_config(page_title="Smart Parking Recommender", layout="wide")

# st.title("🚗 Smart Parking Finder")
# st.markdown("Use the map to select your current location.")

# # Map UI
# default_location = [37.7942, -122.4063]
# m = folium.Map(location=default_location, zoom_start=14)
# folium.Marker(location=default_location, tooltip="Default Center").add_to(m)

# # Make map interactive
# output = st_folium(
#     m,
#     width=700,
#     height=500,
#     returned_objects=["last_clicked"],
#     key="map"
# )

# coords = output.get("last_clicked") or output.get("center")
# if coords is None:
#     st.warning("📍 Please click on the map to select your location.")
#     st.stop()

# user_lat, user_lon = coords["lat"], coords["lng"]
# st.markdown(f"📍 **Current Location**: `{user_lat:.5f}, {user_lon:.5f}`")

# top_n = st.slider("How many nearby spots to show?", 1, 10, 3)

# # Load Kafka data
# st.info("📡 Fetching latest parking data from Kafka...")
# consumer = load_consumer()
# fetch_parking_data(consumer)

# # Show recommendations
# st.subheader("🅿️ Nearby Available Parking Spots")
# top_spots = find_nearest_available(user_lat, user_lon, top_n)

# if not top_spots:
#     st.error("❌ No available spots found in the past 24 hours.")
# else:
#     for i, spot in enumerate(top_spots, 1):
#         drive_time_min = math.ceil(spot['distance'] / 500)  # ~30km/h speed
#         weekday = "Weekend" if spot.get('is_weekend') else "Weekday"
#         st.markdown(f"""
#         **{i}.** 📍 `{spot['street_name']} #{spot['street_num']}` ({spot['analysis_neighborhood']})  
#         🕓 Last Updated: `{spot['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}` — *{weekday}*  
#         📏 Distance: `{round(spot['distance'], 1)} meters` (~{drive_time_min} min drive)
#         """)

# streamlit_app.py

import streamlit as st
import pandas as pd
from geopy.distance import geodesic
from datetime import datetime
import folium
from streamlit_folium import st_folium

# Load latest Kafka predictions
@st.cache_data(ttl=30)
def load_recent_data():
    try:
        df = pd.read_csv("data/recent_predictions.csv", parse_dates=["timestamp"])
        df.dropna(subset=["latitude", "longitude", "occupied"], inplace=True)
        df = df[df["occupied"] == 0]  # Only show unoccupied spots
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df
    except Exception as e:
        st.error(f"Failed to load predictions: {e}")
        return pd.DataFrame()

# Calculate distance and rank
def get_top_nearest_spots(df, user_lat, user_lon, top_n=5):
    df["distance_meters"] = df.apply(
        lambda row: geodesic((user_lat, user_lon), (row["latitude"], row["longitude"])).meters,
        axis=1,
    )
    df = df.sort_values(by="distance_meters").head(top_n)
    return df

# Streamlit UI
st.set_page_config(page_title="Smart Parking Finder", layout="centered")
st.title("🚗 Smart Parking Availability")

st.markdown("Enter your location to find nearby available parking spots:")

col1, col2 = st.columns(2)
with col1:
    user_lat = st.number_input("Latitude", value=37.7942, format="%.6f")
with col2:
    user_lon = st.number_input("Longitude", value=-122.4063, format="%.6f")

if "search_clicked" not in st.session_state:
    st.session_state.search_clicked = False

if st.button("🔍 Find Parking Availability"):
    st.session_state.search_clicked = True

if st.session_state.search_clicked:
    df = load_recent_data()
    if df.empty:
        st.warning("No parking prediction data available. Try again soon.")
    else:
        nearest_spots = get_top_nearest_spots(df, user_lat, user_lon, top_n=5)
        if nearest_spots.empty:
            st.info("No available spots found nearby.")
        else:
            st.success("Top Available Parking Spots Near You:")
            for i, row in nearest_spots.iterrows():
                st.markdown(f"""
                **{i+1}.** 📍 `{row['street_name']} #{int(row['street_num'])}` — *{row['analysis_neighborhood']}*  
                🕓 Last Updated: `{row['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}`  
                📏 Distance: `{row['distance_meters']:.1f} meters` (~{int(row['distance_meters'] / 500) + 1} min drive)
                """)

            # Show locations on map
            with st.expander("🗺 Show Map"):
                m = folium.Map(location=[user_lat, user_lon], zoom_start=14)
                folium.Marker([user_lat, user_lon], popup="📍 You", icon=folium.Icon(color="blue")).add_to(m)
                for _, row in nearest_spots.iterrows():
                    folium.Marker(
                        [row["latitude"], row["longitude"]],
                        popup=f"{row['street_name']} #{int(row['street_num'])}",
                        icon=folium.Icon(color="green"),
                    ).add_to(m)
                st_folium(m, width=700, height=500)
