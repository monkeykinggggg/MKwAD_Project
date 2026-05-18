from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Computational Server")


class EncryptedPayload(BaseModel):
    data: list[float]

@app.get("/")
def read_root():
    return "Hello! I'm computational server!"

@app.post("/mean")
def compute_mean(payload: EncryptedPayload):
    print("Received data for computation")
    fake_encrypted_mean = sum(payload.data) / len(payload.data)
    return {"result": fake_encrypted_mean}

@app.post("/stdev")
def compute_stdev(payload: EncryptedPayload):
    pass

@app.post("/corr")
def compute_stdev(payload: EncryptedPayload):
    pass
