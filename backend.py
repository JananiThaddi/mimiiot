from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field 
from typing import Optional
import time

app = FastAPI(title="Mini IoT Backend")

# ✅ CORS for dev: allow all (safe for local testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LAST_READING = None

class Reading(BaseModel):
    deviceId: str = Field(..., examples=["dev-001"])
    temp_c: float = Field(..., examples=[28.6])
    humidity: Optional[float] = Field(None, examples=[60.0])
    ts: Optional[float] = Field(None, description="Unix time; server fills if missing")

def simple_predict(temp_c: float) -> dict:
    label = "hot" if temp_c > 30 else "normal"
    score = 0.9 if label == "hot" else 0.8
    return {"label": label, "score": score}

@app.post("/ingest")
def ingest(reading: Reading):
    global LAST_READING
    payload = reading.dict()
    if payload.get("ts") is None:
        payload["ts"] = time.time()
    LAST_READING = payload
    return {"ok": True}

@app.get("/latest")
def latest():
    if LAST_READING is None:
        return JSONResponse({"error": "no data yet"}, status_code=404)
    return LAST_READING

@app.get("/predict")
def predict():
    if LAST_READING is None:
        return JSONResponse({"error": "no data yet"}, status_code=404)
    pred = simple_predict(LAST_READING["temp_c"])
    return {"deviceId": LAST_READING["deviceId"], "prediction": pred}
