from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from init_db import SessionLocal, CheckIn, Venue 
from pydantic import BaseModel
from utils import calculate_midpoint
from maps import fetch_nearby_places
from recommender import score_and_rank_venues
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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
def get_recommendations(request: MeetupRequest, db: Session = Depends(get_db)):
    # Step 1: Geometry math
    midpoint = calculate_midpoint(
        request.user_a_lat, request.user_a_lon, 
        request.user_b_lat, request.user_b_lon
    )
    
    # Step 2: Fetch raw data
    raw_venues = fetch_nearby_places(
        midpoint["latitude"], 
        midpoint["longitude"]
    )
    
    # Step 3: Run the AI Ranking Engine
    # Note: Hardcoding user IDs for now; usually these come from Auth or the Request
    ranked_recommendations = score_and_rank_venues(
        google_results=raw_venues,
        user_a_id="test_user_01", 
        user_b_id="test_user_02",
        db=db
    )
    
    return {
        "midpoint": midpoint,
        "recommendations": ranked_recommendations
    }