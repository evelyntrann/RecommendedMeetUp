from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import datetime

# Connection to your Docker container
DATABASE_URL = "postgresql://postgres:password@127.0.0.1:5433/meetup_db"  # Changed port to 5433

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# New 2.0 way to define the Base class
class Base(DeclarativeBase):
    pass

# 1. Check-in Table
class CheckIn(Base):
    __tablename__ = "checkins"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    venue_id = Column(String)
    venue_name = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# 2. Venue Table
class Venue(Base):
    __tablename__ = "venues"
    id = Column(Integer, primary_key=True, index=True)
    google_place_id = Column(String, unique=True)
    name = Column(String)
    lat = Column(Float)
    lng = Column(Float)
    rating = Column(Float)

def init_db():
    Base.metadata.create_all(engine)
    print("Tables created successfully in PostGIS!")

if __name__ == "__main__":
    init_db()