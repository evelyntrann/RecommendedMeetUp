from geopy.point import Point
from geopy.distance import distance, geodesic

def calculate_midpoint(lat1, lon1, lat2, lon2):
    """
    Calculates the geographic midpoint between two coordinates.
    """
    # Create Point objects
    p1 = Point(lat1, lon1)
    p2 = Point(lat2, lon2)
    
    # Calculate the distance to find the halfway bearing
    d = distance(p1, p2)
    half_dist = d.km / 2
    
    # Calculate midpoint using a geodesic path
    # We move from p1 towards p2 exactly half the distance
    # This is more accurate than (lat1+lat2)/2
    midpoint = geodesic(kilometers=half_dist).destination(p1, bearing=geodesic().inverse(p1, p2))
    
    return {
        "latitude": midpoint.latitude,
        "longitude": midpoint.longitude
    }

# Quick test if you run this file directly
if __name__ == "__main__":
    # Example: Seattle to Bellevue
    seattle = (47.6062, -122.3321)
    bellevue = (47.6101, -122.2015)
    
    mid = calculate_midpoint(seattle[0], seattle[1], bellevue[0], bellevue[1])
    print(f"Midpoint: {mid}")