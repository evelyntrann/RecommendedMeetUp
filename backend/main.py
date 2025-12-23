from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from init_db import SessionLocal, CheckIn, Venue 
from pydantic import BaseModel
from utils import calculate_midpoint
from maps import fetch_nearby_places, get_coords_from_address
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
    user_a_address: str
    user_b_address: str

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
    lat_a, lon_a = get_coords_from_address(request.user_a_address)
    lat_b, lon_b = get_coords_from_address(request.user_b_address)

    print("User A address:", request.user_a_address)
    print("User A coords:", lat_a, lon_a)

    print("User B address:", request.user_b_address)
    print("User B coords:", lat_b, lon_b)

    if lat_a is None or lat_b is None:
        raise HTTPException(
            status_code=400,
            detail="Could not find one or both addresses"
        )

    midpoint = calculate_midpoint(
        lat_a, lon_a, lat_b, lon_b
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
        "user_a_coords": {"lat": lat_a, "lng": lon_a}, 
        "user_b_coords": {"lat": lat_b, "lng": lon_b},
        "midpoint": midpoint,
        "recommendations": ranked_recommendations
    }