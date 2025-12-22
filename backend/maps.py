from json import load
import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEYS = os.getenc("GOOGLE_MAPS_API_KEY")

def fetch_nearby_places(lat, lon, radius=2000, place_type="coffee_shop"):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json" 
    params = {
        "location": f"{lat},{lon}",
        "radius": radius,
        "type": place_type,
        "key": API_KEYS
    }   

    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json().get("results", [])
        return results
    else:
        print(f"Error: {response.status_code}")
        return []