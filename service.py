import bentoml
from bentoml.io import JSON
import pandas as pd
from pydantic import BaseModel, Field, validator
from typing import List

# -----------------------------
# Définition du modèle Pydantic pour un bâtiment
# -----------------------------
class BuildingItem(BaseModel):
    YearBuilt: int = Field(..., example=2000)
    LargestPropertyUseType: str = Field(..., example="Office")
    PropertyGFATotal: float = Field(..., example=5000.0)
    City: str = Field(..., example="Seattle")
    State: str = Field(..., example="WA")
    Latitude: float = Field(..., example=47.6062)
    Longitude: float = Field(..., example=-122.3321)
    AgeBuilding: int = Field(..., example=25)
    DataYear: int = Field(..., example=2025)
    NumberofBuildings: int = Field(..., example=1)
    NumberofFloors: int = Field(..., example=10)
    PrimaryPropertyType: str = Field(..., example="Office")
    BuildingType: str = Field(..., example="HighRise")
    PropertyGFAParking: float = Field(..., example=500)
    LargestPropertyUseTypeGFA: float = Field(..., example=4000)
    SecondLargestPropertyUseType: str = Field(..., example="Retail")
    SecondLargestPropertyUseTypeGFA: float = Field(..., example=500)
    ThirdLargestPropertyUseType: str = Field(..., example="Storage")
    ThirdLargestPropertyUseTypeGFA: float = Field(..., example=500)
    ListOfAllPropertyUseTypes: str = Field(..., example="Office, Retail, Storage")
    PropertyGFABuildings: float = Field(..., example=5000)  # sera renommé
    YearsENERGYSTARCertified: int = Field(..., example=5)
    PropertyGFATotal_log1p: float = Field(..., example=8.5)

    @validator("YearBuilt")
    def validate_year(cls, v):
        if v < 1800 or v > 2025:
            raise ValueError("YearBuilt incohérent")
        return v

    @validator("PropertyGFATotal")
    def validate_gfa(cls, v):
        if v <= 0:
            raise ValueError("PropertyGFATotal doit être positif")
        return v

# -----------------------------
# Classe Pydantic pour contenir la liste de bâtiments
# -----------------------------
class BuildingList(BaseModel):
    buildings: List[BuildingItem]

# -----------------------------
# Charger le modèle depuis BentoML
# -----------------------------
model = bentoml.sklearn.get("building_energy_model:latest")
runner = model.to_runner()

# -----------------------------
# Définir le service BentoML
# -----------------------------
svc = bentoml.Service(name="building_energy_predictor", runners=[runner])

# -----------------------------
# Endpoint JSON
# -----------------------------
@svc.api(input=JSON(pydantic_model=BuildingList), output=JSON())
def predict(data: BuildingList):
    try:
        # Convertir la liste d'objets validés en DataFrame
        df = pd.DataFrame([b.dict() for b in data.buildings])

        # Renommer la colonne pour correspondre au modèle entraîné
        if "PropertyGFABuildings" in df.columns:
            df.rename(columns={"PropertyGFABuildings": "PropertyGFABuilding(s)"}, inplace=True)

        # Faire la prédiction
        preds = runner.run(df)
        return {"prediction": preds.tolist()}
    except Exception as e:
        return {"error": f"Internal Server Error: {str(e)}"}

