import os
from dotenv import load_dotenv
from maps import fetch_nearby_places

load_dotenv()

# test with San Francisco
lat = 37.7749
lon = -122.4194

print(f"Testing Google Places API for location: {lat}, {lon}")
print("=" * 50)

results = fetch_nearby_places(lat, lon, radius=2000, place_type="cafe")

if results:
    print(f"Found {len(results)} places!")
    for place in results: # You need this loop!
        print("-" * 20)
        print(f"   Name: {place.get('name')}")
        print(f"   Address: {place.get('vicinity', 'N/A')}")
        print(f"   Rating: {place.get('rating', 'N/A')}")

else:
    print("No result found or error occurred.")
