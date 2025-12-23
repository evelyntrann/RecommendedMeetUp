from pathlib import Path
import os
import requests
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

if not GOOGLE_MAPS_API_KEY:
    raise RuntimeError("GOOGLE_MAPS_API_KEY not loaded")

def fetch_nearby_places(lat, lon, radius=2000, place_type="cafe"):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lon}",
        "radius": radius,
        "type": place_type,
        "key": GOOGLE_MAPS_API_KEY, 
    }

    response = requests.get(url, params=params)
    data = response.json()

    print("Google Places status:", data.get("status"))
    if "error_message" in data:
        print("Google error:", data["error_message"])

    return data.get("results", [])

def get_coords_from_address(address: str):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": GOOGLE_MAPS_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    print("===== GEOCODE DEBUG =====")
    print("Address:", address)
    print("HTTP status:", response.status_code)
    print("Google status:", data.get("status"))
    print("Error message:", data.get("error_message"))
    print("========================")

    if data.get("status") != "OK":
        return None, None

    location = data["results"][0]["geometry"]["location"]
    return location["lat"], location["lng"]




