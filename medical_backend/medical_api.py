import base64
import math
from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from pydantic import BaseModel, ConfigDict
import os
import csv
from contextlib import asynccontextmanager
from typing import List
import requests
import tenseal as ts

COMPUTATIONAL_URL = "http://localhost:8002"

engine = create_engine('sqlite:///medical.db', connect_args={"check_same_thread": False})
# database session - preventing it from reloading every flush and commit
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind=engine)
Base = declarative_base()


he_context = ts.context(
    ts.SCHEME_TYPE.CKKS,
    poly_modulus_degree=8192,
    coeff_mod_bit_sizes=[60, 40, 40, 60]
)
he_context.global_scale = 2**40
# Galois keys are required for the sum() operation on vectors
he_context.generate_galois_keys()


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
        
        # adding logic for sharing HE context with computational server
        print("Generating and sharing public HE context...")
        public_context = he_context.copy()
        public_context.make_context_public() # Strips the secret key!
        pub_b64 = base64.b64encode(public_context.serialize()).decode('utf-8')
        requests.post(
            f"{COMPUTATIONAL_URL}/init-context", 
            json={"context": pub_b64}
        )
        print("Public context successfully shared with computational server.")
    except requests.exceptions.RequestException as e:
        print(f"WARNING: Could not connect to computational server: {e}")    
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
    new_patient = PatientResults(**patient.dict())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient

@app.get("/sayhello")
def say_hello():
    res = requests.get(COMPUTATIONAL_URL)
    if res.status_code == 200:
        print("Communication with computational server initialized")
        return {
            "status": "Success",
            "message": res.json(),
        }
    else:
        return {
            "status": "Failed",
            "message": "Failed to reach computational server",
        }

@app.get("/analyze/{metric}/{operation}")
def analyze_metric(metric: str, operation: str, request: Request, db: Session = Depends(get_db)):
    valid_columns = PatientResults.__table__.columns.keys()
    valid_operations = ["mean", "variance", "std_dev"]
    
    if metric not in valid_columns:
        raise HTTPException(status_code=400, detail=f"Invalid metric.")
    if operation not in valid_operations:
        raise HTTPException(status_code=400, detail=f"Invalid operation. Choose 'mean', 'variance', or 'std_dev'.")
        
    query = db.query(getattr(PatientResults, metric))
    filters_applied = {}
    for key, value in request.query_params.items():
        if not value.strip():
            continue
        try:
            val_float = float(value)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Filter value for '{key}' must be a number.")
        if key.endswith('_min'):
            col_name = key[:-4]
            if col_name in valid_columns:
                query = query.filter(getattr(PatientResults, col_name) >= val_float)
                filters_applied[key] = val_float
                
        elif key.endswith('_max'):
            col_name = key[:-4]
            if col_name in valid_columns:
                query = query.filter(getattr(PatientResults, col_name) <= val_float)
                filters_applied[key] = val_float
                
        elif key in valid_columns:
            query = query.filter(getattr(PatientResults, key) == val_float)
            filters_applied[key] = val_float
    results = query.all()
    raw_data = [float(row[0]) for row in results if row[0] is not None]
    if not raw_data:
        raise HTTPException(status_code=404, detail="No data found.")

    count = len(raw_data)
    enc_vector = ts.ckks_vector(he_context, raw_data)
    ser_data = base64.b64encode(enc_vector.serialize()).decode('utf-8')

    try:
        operation_endpoint = operation if operation != "std_dev" else "variance"
        response = requests.post(
            f"{COMPUTATIONAL_URL}/{operation_endpoint}",
            json={"data": ser_data, "count": count}
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Computational server error: {e}")

    result_b64 = response.json().get("result")
    result_bytes = base64.b64decode(result_b64)
    result_enc = ts.ckks_vector_from(he_context, result_bytes)
    decrypted_result = result_enc.decrypt()
    final_value = decrypted_result[0]

    response_payload = {
        "status": "Success",
        "metric_analyzed": metric,
        "rows_counted": count,
        "filters_applied": filters_applied,
        f"result_{operation}": final_value if operation != "std_dev" else math.sqrt(final_value)
    }
    return response_payload