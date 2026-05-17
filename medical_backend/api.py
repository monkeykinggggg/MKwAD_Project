from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Medical Backend API")


engine = create_engine('sqlite:///medical.db', connect_args={"check_same_thread": False})
# database session - preventing it from reloading every flush and commit
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind=engine)
Base = declarative_base()

# database structure
class PatientResults(Base):
    __tablename__ = "patients_results"
    patient_id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer)
    sex = Column(Integer)
    chest_pain = Column(Integer)
    resting_blood = Column(Integer)
    serum_cholesterol = Column(Integer)
    fasting_blood_sugar = Column(Integer)
    electrocardiography = Column(Integer)
    maximum_heart_rate = Column(Integer)
    angina = Column(Integer)
    oldpeak_ST = Column(Float)
    slope_ST = Column(Float)
    major_vessel_number = Column(Integer)
    thal = Column(Integer)

Base.metadata.create_all(engine)


# validation model for fastapi
class PatientResultsCreate(BaseModel):
    age: int
    sex: int
    chest_pain: int
    resting_blood: int
    serum_cholesterol: int
    fasting_blood_sugar: int
    electrocardiography: int
    maximum_heart_rate: int
    angina: int
    oldpeak_ST: float
    slope_ST: float
    major_vessel_number: int
    thal: int


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

get_db()

# endpoints
@app.get("/")
def health():
    return "Medical Backend API"
