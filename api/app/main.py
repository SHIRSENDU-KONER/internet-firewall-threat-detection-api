from fastapi import FastAPI, Request
from pydantic import BaseModel
import numpy as np
import pandas as pd
import joblib 
import os
import json

# ---------- Data Model ----------
class PredictionInput(BaseModel):
    features: dict  # key-value pairs for column names and values


# ---------- FastAPI Setup ----------
app = FastAPI(title="XGBoost Model Prediction API")

model = None

# ---------- Load model and metadata ----------
@app.on_event("startup")
async def load_model():
    global model, model_columns

    model_path = "./api/models/final_model.pkl"

    try:
        model = joblib.load(model_path)
        print(f"Model loaded from {model_path}")
    except Exception as e:
        print(f"❌ Error loading model: {e}")

    try:
        model_columns = model.get_booster().feature_names
        print(f"Feature order loaded from {model_columns}")
    except Exception as e:
        print(f"❌ Error loading feature list: {e}")


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "model_loaded": model is not None,
        "model_columns": model_columns is not None
    }


# ---------- Preprocessing ----------
def preprocess(data: dict) -> pd.DataFrame:
    """
    Convert input JSON to DataFrame, align columns, and apply any preprocessing.
    """
    # payload = json.loads(data)  # Ensure data is a dictionary
    payload = data  # Assuming data is already a dictionary
    df = pd.DataFrame([payload])  # Single row
    # df = df[model_columns]

    df['bytes_per_sec'] = df['bytes'] / (df['elapsed_time_(sec)'] + 1e-6)  # Avoid division by zero
    df['bytes_ratio'] = df['bytes_sent'] / (df['bytes_received'] + 1)
    df['packets_ratio'] = df['pkts_sent'] / (df['pkts_received'] + 1)

    df['burst_transfer'] = np.where(df['bytes_per_sec'] > df['bytes_per_sec'].quantile(0.99), 1, 0)
    df['low_activity'] = np.where((df['bytes'] < 100) & (df['elapsed_time_(sec)'] > 10), 1, 0)
    df['high_activity'] = np.where((df['bytes'] > 10000) & (df['elapsed_time_(sec)'] < 5), 1, 0)

    ## remove columns that are not in the model
    df = df[model_columns]  # Ensure columns match model's expected input
    return df


# ---------- Prediction ----------
@app.post("/predict")
async def predict(data: PredictionInput):
    if model is None:
        return {"error": "Model not loaded. Please check the server logs."}, 500

    try:
        df = preprocess(data.features)
        df['prediction'] = model.predict(df)
        prediction = df['prediction'].values
        print(f"Prediction: {prediction}")
        
        category_mapping = {0: 'allow', 1: 'deny', 2: 'drop', 3: 'reset-both'}

        # Map codes back to original labels
        prediction_label = [category_mapping[code] for code in prediction][0]

        # probabilities = model.predict_proba(input_df)
        probabilities = model.predict_proba(df)
        return {
            "prediction": prediction_label,
            # "probabilities": probabilities.tolist()
        }
    except Exception as e:
        return {"error": f"Prediction failed: {e}"}, 500


# ---------- Run Locally ----------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
