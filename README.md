# SmartMeet

Restart the backend:

Step 1:

`cd backend`

Step 2: Activate the virtual environment

`source venv/bin/activate`

Step 3: running the [main.py](http://main.py) file

`uvicorn main:app --reload`

Step 4: Ctrl + C for quitting the service

### Step 1: Connect with database

`docker exec -it meetup_db psql -U postgres -d meetup_db`

### Step 2: Insert (when seeing the meetup_db # prompt)

We have 2 models for now:

- checkins: to save the place that users have checked in for content-based recommendation.
    
    `checkins` is one of the most important tables. Without this, my app is just a Google Map. 
    
    - It will see the User Preferences: If User A checks in at “Pastry Tea Shop” 5 times and User B checks in at “Starbucks” 10 times, the app will see the pattern.
    - Collaborative Filtering: recommend the place of similar group of users. The app will recommend the coffee place in Seattle for a user although they have never been there.
    - 
- venues: to cache the recommended places. While we using Google Place APIs provided by Google Console to find new spot, you don’t want to call the API every time you find the place for that specific area, because it is expensive and time-consuming.
    - Caching: You find a coffee spot in Bellevue area, you cache the result here. The next time the user looks in this area, your app check the cache table first.
    - **Source of Truth:** It stores the "Geospatial" data (Latitude/Longitude) which allows PostGIS to calculate distances.
    - **Metadata:** It holds the "Vibe" or "Rating" of a place so you can filter results (e.g., "Only show cafes with a 4.0+ rating").

`INSERT INTO checkins (user_id, venue_id, venue_name, timestamp) VALUES ('uyentran', 'venue123', 'Story Coffee', NOW());`

### Step 3: Verify that the row is added to the table `checkins`

`SELECT * FROM checkins;`

Step 4: Exit the insert mode

`\q`

