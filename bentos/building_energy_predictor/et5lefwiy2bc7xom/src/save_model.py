import bentoml
from sklearn.pipeline import Pipeline
import joblib  # si ton pipeline est sauvegardé dans un fichier

# Charger ton pipeline existant
pipeline = joblib.load("pipeline_building_energy.pkl")  # remplace par ton fichier réel

# Vérifier que c'est bien un pipeline
if not isinstance(pipeline, Pipeline):
    raise TypeError("L'objet pipeline n'est pas un sklearn.pipeline.Pipeline")

# Sauvegarder le pipeline dans BentoML
model_ref = bentoml.sklearn.save_model(
    name="building_energy_model",
    model=pipeline,
    signatures={"predict": {"batchable": True}}
)

print(f"Modèle sauvegardé : {model_ref}")
print("Chemin du modèle :", model_ref.path)
