# Smart Parking Finder - ML Enhanced

**Overview**

This project is a machine learning-powered parking spot finder for San Francisco that predicts parking availability in real-time. It combines:
* Live parking meter data from SF OpenData
* Realistic occupancy simulation
* Neural network predictions
* Interactive mapping
  
The system helps drivers find available parking spots near their destination, saving time and reducing congestion.


**Key Features**

Smart Parking Prediction
* Real-time availability: Predicts parking spot availability for any given time and neighborhood
* Machine learning model: Uses a neural network trained on simulated occupancy patterns
* Dynamic thresholds: Adapts predictions based on local conditions

  
Interactive Mapping
* Visualizes all available parking spots
* Shows walking distance to destination
* Color-codes spots by distance (green = closest)

Realistic Simulation
* Models hourly and weekly parking patterns
* Incorporates local events impacting parking
* Guarantees some availability in all areas


**How It Works**
1. Data Collection: Fetches all SF parking meter locations from the city's open data portal
2. Occupancy Simulation: Creates realistic parking patterns based on:
* Time of day
* Day of week
* Neighborhood characteristics
* Local events
3. Machine Learning: Trains a neural network to predict spot availability
4. Recommendation Engine: Finds the closest available spots to your destination
5. Visualization: Displays results on an interactive map

  
**Requirements**
* Python 3.7+
* PySpark
* TensorFlow 2.x
* Geopy
* Folium
* Pandas
* NumPy

  
**Installation**

1. Clone the repository:
```
git clone https://github.com/yourusername/smart-parking-finder.git

cd smart-parking-finder
```
2. Install dependencies:
```
pip install -r requirements.txt
```
3. Set up Spark (if running locally):

Download Spark from https://spark.apache.org/downloads.html

Set SPARK_HOME environment variable

**Usage**

Interactive Mode

Run the Jupyter notebook or Python script and use the interactive widget to:

1. Select a neighborhood

2. Choose date and time

3. Enter destination coordinates

4. Click "Find Parking"

**Programmatic Use**
```
from parking_finder import comprehensive_parking_search_ml_fixed
# Search for parking in the Mission district
results = comprehensive_parking_search_ml_fixed(
    neighborhood="Mission",
    search_date="2025-05-28",
    search_hour=14,
    dest_lat=37.7599,
    dest_lon=-122.4148
)
```
**Sample Output**

The system will:

1. Display statistics about parking availability
2. Recommend the top 10 closest available spots
3. Generate an interactive HTML map showing:
* Available parking spots
* Your destination
* Walking radius

  
**Limitations**

* Currently uses simulated rather than real-time occupancy data
* Model accuracy depends on quality of simulation
* Limited to San Francisco parking meters

  
**Future Enhancements**
* Integrate real-time parking sensor data
* Add historical patterns for better predictions
* Include pricing information
* Mobile app integration



