from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from pydantic import BaseModel, ConfigDict
import os
import csv
from contextlib import asynccontextmanager
from typing import List

from sqlalchemy.testing.pickleable import User

engine = create_engine('sqlite:///medical.db', connect_args={"check_same_thread": False})
# database session - preventing it from reloading every flush and commit
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind=engine)
Base = declarative_base()

# database structure
class PatientResults(Base):
    __tablename__ = "patients_results"
    patient_id = Column(Integer, primary_key=True, index=True)  # gets automatically added and incremented
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
    target = Column(Integer)

Base.metadata.create_all(engine)


# validation model for fastapi - pydantic model
class PatientResultsReponse(BaseModel):
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
    target: int

    model_config = ConfigDict(from_attributes=True)


def seed_database_from_csv(db: Session, filepath: str = "heart.csv"):
    if not os.path.exists(filepath):
        print(f"File'{filepath}' not found.")
        return

    if db.query(PatientResults).first() is not None:
        print("Database contains data. Skipping CSV seeding.")
        return

    with open(filepath, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            patient = PatientResults(
                age=int(row['age']),
                sex=int(row['sex']),
                chest_pain=int(row['cp']),
                resting_blood=int(row['trestbps']),
                serum_cholesterol=int(row['chol']),
                fasting_blood_sugar=int(row['fbs']),
                electrocardiography=int(row['restecg']),
                maximum_heart_rate=int(row['thalach']),
                angina=int(row['exang']),
                oldpeak_ST=float(row['oldpeak']),
                slope_ST=int(row['slope']),
                major_vessel_number=int(row['ca']),
                thal=int(row['thal']),
                target=int(row['target'])
            )
            db.add(patient)
        db.commit()
    print("Database seeding complete!")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # uvicorn runs this code first. It will NOT accept any web
    # traffic until this code finishes completely.
    print("Server is waking up. Doing initialization now...")
    db = SessionLocal()
    try:
        seed_database_from_csv(db)
    finally:
        db.close()
    # The 'yield' pauses this function. FastAPI takes over here
    # and starts accepting HTTP requests from your React frontend.
    yield
    # When you stop uvicorn (e.g., pressing Ctrl+C or Choreo
    # restarting the container), the function unpauses and runs
    # this cleanup code before finally dying.
    print("Server is shutting down. Cleaning up database (for development).")
    engine.dispose()
    db_path = "medical.db"
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed database '{db_path}'.")

app = FastAPI(title="Medical Backend API", lifespan=lifespan)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# endpoints
@app.get("/")
def health():
    return "Medical Backend API"

@app.get("/patients", response_model=List[PatientResultsReponse])
def get_patients(db: Session = Depends(get_db)):
    patients = db.query(PatientResults).all()
    return patients

@app.get("/patients/count")
def get_patients(db: Session = Depends(get_db)):
    nmbr_of_patients = db.query(PatientResults).count()
    return {"count": nmbr_of_patients}

@app.get("/patients/{patient_id}", response_model=PatientResultsReponse)
def get_patient(patient_id:int, db:Session = Depends(get_db)):
    patient = db.query(PatientResults).filter(PatientResults.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.post("/patients", response_model=PatientResultsReponse)
def create_patient(patient:PatientResultsReponse, db:Session = Depends(get_db)):
    patient = db.query(PatientResults).filter(PatientResults.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient
