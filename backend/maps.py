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