# Project: Smart Parking System — Real-Time Parking Intelligence in San Francisco

## Smart Parking Availability System

A real-time parking recommendation engine for San Francisco that:
- Streams synthetic parking data via Kafka
- Predicts spot availability using a machine learning model (XGBoost)
- Displays nearest available parking locations on an interactive Streamlit web app

---

## Overview
This system combines machine learning, real-time data streaming, and geospatial filtering to help users find unoccupied parking spots near their current location in San Francisco.

### Core Components
- **Kafka Producer**: Simulates live parking sensor data
- **Kafka Consumer**: Reads from the stream, applies ML predictions, and stores recent results
- **ML Model (XGBoost)**: Predicts occupancy of parking spots
- **Streamlit App**: Provides a user interface with live availability and map visuals

---

##  Project Structure
```
BigDataProject/
├── Prototype 1: Scalable Smart Parking Forecasting/
├── Prototype 2: Real-Time Parking Predictor/
│   ├── data/
│   │   ├── parking_inventory.csv
│   │   └── recent_predictions.csv
│   ├── models/
│   │   ├── xgb_model.joblib
│   │   └── pipeline.joblib
│   ├── outputs/
│   ├── src/
│   │   ├── ingest.py
│   │   ├── recommend.py
│   │   ├── produce_stream.py
│   │   ├── consume_and_query.py
│   │   └── write_predictions.py
│   ├── main.py
│   ├── requirements.txt
│   └── streamlit_app.py
└── README.md
```

---

## Installation

### Prerequisites
- Python 3.9 or later
- Apache Kafka (locally on `localhost:9092`)

### Setup Steps

1. Clone the repo
```
git clone https://github.com/jiyeonwoo/BigDataProject.git
cd BigDataProject
cd Prototype 2: Real-Time Parking Predictor
```
2. Create and activate virtual environment
```
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```
3. Install dependencies
```
pip install -r requirements.txt
```

### How to Run the System

1. Prepare ML Model
```
python src/recommend.py
```
2. Download & Clean Data
```
python src/ingest.py
```
3. Start Kafka Producer (Simulated Live Stream)
```
python src/produce_stream.py
```
4. Start Kafka Consumer (Prediction Logger)
```
python src/consume_and_query.py
#or
python src/write_predictions.py
```
5. Launch Streamlit Web App
```
streamlit run streamlit_app.py
```
## Features
- User inputs current latitude and longitude
- Filters recent_predictions.csv for unoccupied spots
- Calculates:
  - Geodesic distance to each spot
  - Approximate drive time (based on 30m/h)
- Displays:
  - Top 5 closest unoccupied spots
  - Interactive map with markers

## Example
User Location: Latitude = 37.7942, Longitude = -122.4063
1. 📍 LARKIN ST #7 (Tenderloin)
   
      Updated: 2025-05-27 22:55:49 — Weekday
   
      Distance: 728.5 meters (~2 min drive)

3. 📍 MISSION ST #10 (SoMa)
 
      Updated: 2025-05-27 22:55:47 — Weekday
   
      Distance: 1150.4 meters (~3 min drive)

## Future Improvements 
- Clickable location input on map
- Real-time traffic integration
- Scheduled cleanup of stale predictions
- Dockerized deployment for reproducibility

## Authors
This project was collaboratively developed for Big Data BAX 423.

| Name             | GitHub                                   |
|------------------|------------------------------------------|
| Rimsa Shrestha   | [@rimsashrestha](https://github.com/rimsashrestha) |
| Jiyeon (Jenna) Woo       | [@jiyeonwoo](https://github.com/jiyeonwoo) |
| Kaylyn Nguyen    |                               |
| Katrin Maliatski    |                               |
| Christina Zhu   |                               |
