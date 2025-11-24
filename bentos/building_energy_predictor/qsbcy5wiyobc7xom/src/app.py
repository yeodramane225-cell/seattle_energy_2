from fastapi import FastAPI
from pydantic import BaseModel, Field, validator
from typing import List
import pandas as pd
import bentoml

class BuildingItem(BaseModel):
    YearBuilt: int = Field(..., example=2000)
    LargestPropertyUseType: str = Field(..., example="Office")
    PropertyGFATotal: float = Field(..., example=5000.0)

    @validator("YearBuilt")
    def year_valid(cls, v):
        if v < 1800 or v > 2025:
            raise ValueError("YearBuilt incohérent")
        return v

    @validator("PropertyGFATotal")
    def gfa_positive(cls, v):
        if v <= 0:
            raise ValueError("PropertyGFATotal doit être positif")
        return v

# Charger le modèle BentoML et créer un runner
bento_model = bentoml.sklearn.get("building_energy_model:latest")
runner = bento_model.to_runner()

app = FastAPI(title="Building Energy Predictor")

@app.on_event("startup")
async def startup_event():
    await runner.start()

@app.on_event("shutdown")
async def shutdown_event():
    await runner.stop()

@app.post("/predict")
async def predict(buildings: List[BuildingItem]):
    df = pd.DataFrame([b.dict() for b in buildings])
    # Utiliser le runner pour la prédiction
    preds = await runner.predict.async_run(df)
    return {"prediction": preds.tolist()}
