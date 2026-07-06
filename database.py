"""
Handles all database setup and configuration for the weight management agent.
Uses SQLite (no installation required) with SQLAlchemy ORM.
Tables are auto-created on first run via init_db().
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# --- Connection Setup ---
# Engine points to the SQLite file, SessionLocal is the factory for DB sessions,
# and Base is the parent class all models inherit from.
DATABASE_URL = "sqlite:///./weight.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# --- Database Model ---

class UserGoal(Base):
    # Stores user profile and goals
    __tablename__ = "user_goals"

    id = Column(Integer, primary_key=True, index=True)
    height = Column(Float)          # Height in cm (for BMI calculation)
    target_weight = Column(Float)   # Target weight in kg
    created_at = Column(DateTime, default=datetime.now)

class WeightLog(Base):
    # Daily weight records
    __tablename__ = "weight_logs"

    id = Column(Integer, primary_key=True, index=True)
    weight = Column(Float)          # Weight in kg
    date = Column(DateTime, default=datetime.now)

class FoodLog(Base):
    # Food intake records
    __tablename__ = "food_logs"

    id = Column(Integer, primary_key=True, index=True)
    food_name = Column(String)      # e.g. 雞腿便當, 拿鐵
    calories = Column(Float)        # Calories (kcal)
    meal_type = Column(String)      # breakfast, lunch, dinner, snack
    date = Column(DateTime, default=datetime.now)

class ExerciseLog(Base):
    # Exercise records
    __tablename__ = "exercise_logs"

    id = Column(Integer, primary_key=True, index=True)
    exercise_name = Column(String)  # e.g. 跑步, 重訓, 游泳
    duration_minutes = Column(Integer)  # Duration in minutes
    calories_burned = Column(Float)     # Estimated calories burned (kcal)
    date = Column(DateTime, default=datetime.now)

# --- Initialization ---
# Creates all tables if they don't exist. Safe to call on every startup.
def init_db():
    Base.metadata.create_all(bind=engine) 
