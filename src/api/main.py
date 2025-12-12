from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import os

# Initialize the API
app = FastAPI(title="SentinelFlow API", description="Real-time Network Anomaly Detection System")

# Global variables to store our artifacts
model = None
scaler = None
encoder = None

# 1. Load the model on startup
@app.on_event("startup")
def load_artifacts():
    global model, scaler, encoder
    try:
        # Define paths relative to this file
        base_path = os.path.dirname(os.path.abspath(__file__))
        
        # FIXED PATHS: Only go up 2 levels (../../)
        model_path = os.path.join(base_path, '../../models/rf_model_v3.pkl')
        scaler_path = os.path.join(base_path, '../../models/scaler_v3.pkl')
        encoder_path = os.path.join(base_path, '../../models/label_encoder_v3.pkl')

        print(f"Loading model from: {model_path}")
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        encoder = joblib.load(encoder_path)
        print("✅ Production model v3 loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        raise e

# 2. Define the data format we expect (78 features)
class NetworkEvent(BaseModel):
    # We accept a list of 78 float values representing the network features
    features: list[float]

# 3. Create the prediction endpoint
@app.post("/predict")
def predict_anomaly(event: NetworkEvent):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        # Convert list to numpy array (1 row, 78 columns)
        input_data = np.array(event.features).reshape(1, -1)
        
        # Scale the data (CRITICAL: Must use the same scaler as training)
        scaled_data = scaler.transform(input_data)
        
        # Make prediction
        prediction_index = model.predict(scaled_data)[0]
        prediction_label = encoder.inverse_transform([prediction_index])[0]
        
        # Get confidence score (probability)
        probabilities = model.predict_proba(scaled_data)[0]
        confidence = float(np.max(probabilities))
        
        # Determine status
        status = "BENIGN" if prediction_label == "BENIGN" else "ATTACK"
        
        return {
            "status": status,
            "prediction": prediction_label,
            "confidence": f"{confidence * 100:.2f}%",
            "model_version": "v3"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/")
def root():
    return {"message": "SentinelFlow API is running"}