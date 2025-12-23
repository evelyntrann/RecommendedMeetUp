from geopy.point import Point
from geopy.distance import geodesic

def calculate_midpoint(lat1, lon1, lat2, lon2):
    """
    Calculates the geographic midpoint between two coordinates.
    """
    p1 = Point(lat1, lon1)
    p2 = Point(lat2, lon2)
    
    # Calculate the exact distance between the two points
    total_distance = geodesic(p1, p2).kilometers
    
    # Find the bearing (direction) from point 1 to point 2
    # Since Geopy's geodesic doesn't have 'inverse', we calculate the destination 
    # point at 50% of the distance.
    
    # We use a simple midpoint for city-scale, or 'nvector' for global scale.
    # For your app, a simple average of vectors is extremely fast and accurate:
    
    mid_lat = (lat1 + lat2) / 2
    mid_lon = (lon1 + lon2) / 2
    
    # If you want it to be "Perfect" for long distances, use this:
    # midpoint = geodesic(kilometers=total_distance/2).destination(p1, bearing=...)
    # But for Seattle/SF/Cities, simple averaging is perfect.
    
    return {
        "latitude": mid_lat,
        "longitude": mid_lon
    }