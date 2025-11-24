from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import joblib

# Exemple de pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('regressor', LinearRegression())
])

# Sauvegarde le pipeline dans un fichier .pkl
joblib.dump(pipeline, 'pipeline_building_energy.pkl')
print("Pipeline scikit-learn sauvegardé correctement !")
