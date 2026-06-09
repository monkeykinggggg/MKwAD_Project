from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import tenseal as ts
import base64
from utils import compute_he_mean, compute_he_variance, compute_he_covariance

app = FastAPI(title="Computational Server")

he_context_storage = {}

class ContextPayload(BaseModel):
    context: str

class EncryptedPayload(BaseModel):
    data: str
    count: int
    
class BiEncryptedPayload(BaseModel):
    data_x: str
    data_y: str
    count: int

@app.get("/")
def read_root():
    return "Hello! I'm computational server!"

@app.post("/init-context")
def init_context(payload: ContextPayload):
    try:
        context_bytes = base64.b64decode(payload.context)
        context = ts.context_from(context_bytes)
        he_context_storage['public_context'] = context
        print("Successfully received and stored public HE context.")
        return {"status": "Success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to receive and load context: {e}")

@app.post("/mean")
def compute_mean_endpoint(payload: EncryptedPayload):
    if 'public_context' not in he_context_storage:
        raise HTTPException(status_code=400, detail="HE Context not initialized.")
    
    context = he_context_storage['public_context']
    vector_bytes = base64.b64decode(payload.data)
    
    enc_vector = ts.ckks_vector_from(context, vector_bytes)
    result_enc = compute_he_mean(enc_vector, payload.count)
    result_b64 = base64.b64encode(result_enc.serialize()).decode('utf-8')
    return {"result": result_b64}

@app.post("/variance")
def compute_variance_endpoint(payload: EncryptedPayload):
    if 'public_context' not in he_context_storage:
        raise HTTPException(status_code=400, detail="HE Context not initialized.")
    
    context = he_context_storage['public_context']
    vector_bytes = base64.b64decode(payload.data)
    
    enc_vector = ts.ckks_vector_from(context, vector_bytes)
    result_enc = compute_he_variance(enc_vector, payload.count)
    
    result_b64 = base64.b64encode(result_enc.serialize()).decode('utf-8')
    return {"result": result_b64}


@app.post("/covariance")
def compute_covariance_endpoint(payload: BiEncryptedPayload):
    if 'public_context' not in he_context_storage:
        raise HTTPException(status_code=400, detail="HE Context not initialized.")
    
    context = he_context_storage['public_context']
    vector_x = ts.ckks_vector_from(context, base64.b64decode(payload.data_x))
    vector_y = ts.ckks_vector_from(context, base64.b64decode(payload.data_y))
    result_enc = compute_he_covariance(vector_x, vector_y, payload.count)

    result_b64 = base64.b64encode(result_enc.serialize()).decode('utf-8')
    return {"result": result_b64}