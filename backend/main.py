from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from init_db import SessionLocal, CheckIn, Venue 
from pydantic import BaseModel
from .utils import calculate_midpoint
from .maps import fetch_nearby_places

app = FastAPI()

# --- Pydantic Models (Data validation for the API) ---
class CheckInCreate(BaseModel):
    user_id: str
    venue_id: str
    venue_name: str

class MeetupRequest(BaseModel):
    user_a_lat: float
    user_a_lon: float
    user_b_lat: float
    user_b_lon: float
# --- Database Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "Meetup API is running!"}
@app.post("/v1/checkin")
def user_checkin(data: CheckInCreate, db = Depends(get_db)):
    # save a user's checkin to a specific database
    new_checkin = CheckIn(user_id=data.user_id, venue_id=data.venue_id, venue_name=data.venue_name)

    try:
        db.add(new_checkin)
        db.commit()
        db.refresh(new_checkin)
        return {"status": "success", "checkin_id": new_checkin.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/v1/my-history/{user_id}")
def get_my_history(user_id: str, db = Depends(get_db)):
    history = db.query(CheckIn).filter(CheckIn.user_id == user_id).all()
    return history

@app.post("/v1/calculate-meetup")
def get_recommendations(request: MeetupRequest):
    # 1. Calculate the center point
    midpoint = calculate_midpoint(
        request.user_a_lat, request.user_a_lon, 
        request.user_b_lat, request.user_b_lon
    )
    
    # 2. Get real venues from Google
    venues = fetch_nearby_places(
        midpoint["latitude"], 
        midpoint["longitude"]
    )
    
    # 3. Clean up the data to return just what we need
    recommendations = []
    for place in venues[:5]: # Top 5 results
        recommendations.append({
            "name": place.get("name"),
            "address": place.get("vicinity"),
            "rating": place.get("rating"),
            "location": place.get("geometry", {}).get("location")
        })
        
    return {
        "midpoint": midpoint,
        "recommendations": recommendations
    }