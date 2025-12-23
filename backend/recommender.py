from sqlalchemy.orm import Session
from init_db import CheckIn

def score_and_rank_venues(google_results, user_a_id, user_b_id, db: Session):
    scored_list = []
    for place in google_results:
        place_id = place.get("place_id")
        base_score = place.get("rating", 0)
        boost = 0 
        tags = []

        a_visits = db.query(CheckIn).filter(CheckIn.user_id == user_a_id, CheckIn.venue_id == place_id).count()
        b_visits = db.query(CheckIn).filter(CheckIn.user_id == user_b_id, CheckIn.venue_id == place_id).count()

        if a_visits > 0:
            boost += 2
            tags.append("User A's favorite")
        if b_visits > 0:
            boost += 2
            tags.append("User B's favorite")
        if a_visits > 0 and b_visits > 0:
            boost += 3
            tags.append("Mututal favourite")
        # 3. Compile the record
        scored_list.append({
            "name": place.get("name"),
            "place_id": place_id,
            "address": place.get("vicinity"),
            "final_score": round(base_score + boost, 2),
            "tags": tags,
            "google_rating": base_score
        })

    # Fixed: Sort outside the loop and use sorted() correctly
    scored_list.sort(key=lambda x: x["final_score"], reverse=True)
    return scored_list
