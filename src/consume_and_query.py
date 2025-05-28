# # src/consume_and_query.py
# from kafka import KafkaConsumer
# import json
# from geopy.distance import geodesic
# from datetime import datetime, timedelta
# import threading
# from colorama import Fore, Style, init
# import math

# # Initialize colorama
# init(autoreset=True)

# # Store recent predictions
# parking_cache = []

# def consume_kafka_messages():
#     consumer = KafkaConsumer(
#         'parking_predictions',
#         bootstrap_servers='localhost:9092',
#         value_deserializer=lambda m: json.loads(m.decode('utf-8')),
#         auto_offset_reset='latest',
#         enable_auto_commit=True
#     )

#     for message in consumer:
#         #print(f"Received message: {message.value}")
#         data = message.value
#         try:
#             # Convert timestamp string to datetime
#             data['timestamp'] = datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S')
#         except Exception as e:
#             print(f"⚠️ Bad timestamp format: {data.get('timestamp')}")
#             continue

#         # Replace previous prediction for this spot
#         global parking_cache
#         parking_cache = [d for d in parking_cache if d['post_id'] != data['post_id']]
#         parking_cache.append(data)

# def find_nearest_available(user_lat, user_lon, top_n=5):
#     now = datetime.now()

#     # Filter only available spots predicted within the last 24 hours
#     recent_data = [
#         d for d in parking_cache
#         if d['occupied'] == 0 and isinstance(d.get('timestamp'), datetime)
#         and (now - d['timestamp']) < timedelta(hours=24)
#     ]

#     if not recent_data:
#         print(Fore.RED + " No available spots found in the past 24 hours." + Style.RESET_ALL)
#         return []

#     # Compute distance and sort
#     for d in recent_data:
#         d['distance'] = geodesic((user_lat, user_lon), (d['latitude'], d['longitude'])).meters

#     sorted_spots = sorted(recent_data, key=lambda x: x['distance'])
#     return sorted_spots[:top_n]

# def print_top_spots(user_lat, user_lon, top_n=5):
#     top_spots = find_nearest_available(user_lat, user_lon, top_n=top_n)

#     if not top_spots:
#         print(Fore.RED + "❌ No available spots found nearby." + Style.RESET_ALL)
#         return

#     print(Fore.GREEN + "\n📌 Top Available Spots Near You:\n" + Style.RESET_ALL)
#     for i, spot in enumerate(top_spots, 1):
#         # Assuming average city driving speed ~30 km/h = 500 meters/min
#         drive_time_min = math.ceil(spot['distance'] / 500)
#         emoji = "🏖" if spot.get('is_weekend') else "🚗"

#         print(f"{i}. 📍 {spot['street_name']} #{spot['street_num']} ({spot['analysis_neighborhood']})")
#         print(f"   🕓 Last Updated: {spot['timestamp'].strftime('%Y-%m-%d %H:%M:%S')} {emoji}")
#         print(f"   📏 Distance: {round(spot['distance'], 1)} meters (~{drive_time_min} min drive)\n")

# # Start Kafka consumer thread
# threading.Thread(target=consume_kafka_messages, daemon=True).start()

# # Example CLI interaction
# if __name__ == "__main__":
#     import time
#     print("⏳ Waiting for data...")
#     time.sleep(10)  # Let the cache fill

#     user_lat = 37.7942
#     user_lon = -122.4063

#     print_top_spots(user_lat, user_lon)

#     import code
#     code.interact(local=locals())




# # src/consume_and_query.py
from kafka import KafkaConsumer
import json
from geopy.distance import geodesic
from datetime import datetime, timedelta
import threading
from colorama import Fore, Style, init
import math

# Initialize colorama
init(autoreset=True)

# Store recent predictions
parking_cache = []

def consume_kafka_messages():
    consumer = KafkaConsumer(
        'parking_predictions',
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='latest',
        enable_auto_commit=True
    )

    for message in consumer:
        # Uncomment for debugging:
        # print(f"Received message: {message.value}")
        data = message.value
        try:
            # Convert timestamp string to datetime
            data['timestamp'] = datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S')
        except Exception:
            print(f"⚠️ Bad timestamp format: {data.get('timestamp')}")
            continue

        # Replace previous prediction for this spot
        global parking_cache
        parking_cache = [d for d in parking_cache if d['post_id'] != data['post_id']]
        parking_cache.append(data)

def find_nearest_available(user_lat, user_lon, top_n=5):
    now = datetime.now()

    # Filter only available spots predicted within the last 24 hours
    recent_data = [
        d for d in parking_cache
        if d['occupied'] == 0 and isinstance(d.get('timestamp'), datetime)
        and (now - d['timestamp']) < timedelta(hours=24)
    ]

    if not recent_data:
        print(Fore.RED + " No available spots found in the past 24 hours." + Style.RESET_ALL)
        return []

    # Compute distance and sort
    for d in recent_data:
        d['distance'] = geodesic((user_lat, user_lon), (d['latitude'], d['longitude'])).meters

    sorted_spots = sorted(recent_data, key=lambda x: x['distance'])
    return sorted_spots[:top_n]

def print_top_spots(user_lat, user_lon, top_n=5):
    top_spots = find_nearest_available(user_lat, user_lon, top_n=top_n)

    if not top_spots:
        print(Fore.RED + "❌ No available spots found nearby." + Style.RESET_ALL)
        return

    # Replaced emoji in the heading to avoid UnicodeEncodeError
    print(Fore.GREEN + "\nTop Available Spots Near You:\n" + Style.RESET_ALL)
    
    for i, spot in enumerate(top_spots, 1):
        # Approximate driving speed ~30 km/h => 500 meters/min
        drive_time_min = math.ceil(spot['distance'] / 500)
        emoji = "Weekend" if spot.get('is_weekend') else "Weekday"

        print(f"{i}. 📍 {spot['street_name']} #{spot['street_num']} ({spot['analysis_neighborhood']})")
        print(f"   🕓 Last Updated: {spot['timestamp'].strftime('%Y-%m-%d %H:%M:%S')} — {emoji}")
        print(f"   📏 Distance: {round(spot['distance'], 1)} meters (~{drive_time_min} min drive)\n")

# Start Kafka consumer thread
threading.Thread(target=consume_kafka_messages, daemon=True).start()

# Example CLI interaction
if __name__ == "__main__":
    import time
    print("⏳ Waiting for data...")
    for i in range(15, 0, -1):
        print(f"⏳ {i} seconds...", end="\r")
        time.sleep(1)

    user_lat = 37.7942
    user_lon = -122.4063

    print_top_spots(user_lat, user_lon)

    import code
    code.interact(local=locals())

##---------after resaerch update----------#
