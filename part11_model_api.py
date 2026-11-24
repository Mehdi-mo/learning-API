from contextlib import asynccontextmanager

import joblib 
import pandas as pd 
from fastapi import FastAPI
from pydantic import BaseModel, Field
import os

ml = {}

@asynccontextmanager
async def lifespan(app : FastAPI):
    ml['model'] = joblib.load('models/model.joblib')
    yield
    ml.clear()

app = FastAPI(title="Exam Pass API", lifespan=lifespan)

class StudentIn(BaseModel):
    hours_studied : float = Field(ge=0)
    attendance : float = Field(ge=0, le=100)

class PredictionOut(BaseModel):
    pass_probability : float
    decision : str


THRESHOLD = float(os.environ.get("THRESHOLD", "0.5"))

def score(students : list[StudentIn]) -> list[dict]:
    X = pd.DataFrame([s.model_dump() for s in students])
    probs = ml['model'].predict_proba(X)[:, 1]
    return [
        {
            "pass_probability": round(float(p), 4),
            "decision": "likely pass" if p >= THRESHOLD else "likely fail"
        }
        for p in probs
    ]

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": "model" in ml}

@app.post("/predict", response_model=PredictionOut)
def predict(student : StudentIn):
    return score([student])[0]

@app.post("/predict/batch", response_model=list[PredictionOut])
def predict_batch(students : list[StudentIn]):
    return score(students)


