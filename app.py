from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import pandas as pd
import bentoml

# Définir le modèle de données
class BuildingItem(BaseModel):
    YearBuilt: int
    LargestPropertyUseType: str
    PropertyGFATotal: float

# Charger le modèle BentoML
bento_model = bentoml.sklearn.get("building_energy_model:latest")
runner = bento_model.to_runner()  # on garde Runner, mais sans start/stop

app = FastAPI(title="Building Energy Predictor")

@app.post("/predict")
async def predict(buildings: List[BuildingItem]):
    df = pd.DataFrame([b.dict() for b in buildings])
    # Utiliser la méthode async_run du runner
    preds = await runner.predict.async_run(df)
    return float(preds[0])  # renvoyer la première valeur directement
