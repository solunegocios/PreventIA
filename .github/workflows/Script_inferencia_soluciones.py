import json
import joblib
import pandas as pd
from azureml.core.model import Model

def init():
    global model
    # Cargar el modelo registrado
    model_path = Model.get_model_path('modelo_final_preventa')
    model = joblib.load(model_path)

def run(raw_data):
    data = json.loads(raw_data)
    df = pd.DataFrame.from_dict(data)
    predictions = model.predict(df)
    return json.dumps({"predictions": predictions.tolist()})
