from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import hashlib
import json

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load("saved_model.pkl")

class InputData(BaseModel):
    lag_1: float
    lag_2: float
    ma_3: float
    rainfall: float
    temperature: float
    month: int


@app.post("/predict")
def predict(data: InputData):

    input_df = pd.DataFrame([[ 
        data.lag_1,
        data.lag_2,
        data.ma_3,
        data.rainfall,
        data.temperature,
        data.month
    ]], columns=[
        "lag_1",
        "lag_2",
        "ma_3",
        "rainfall",
        "temperature",
        "month"
    ])

    try:
        prediction = model.predict(input_df)[0]
    except Exception as e:
        return {"error": str(e)}

    change_percent = ((prediction - data.lag_1) / data.lag_1) * 100
    
    # Use absolute value to catch both large increases AND decreases
    abs_change = abs(change_percent)

    if abs_change > 10:
        risk = "HIGH"      # Large volatility (±10%+)
    elif abs_change > 5:
        risk = "MEDIUM"    # Moderate volatility (±5-10%)
    else:
        risk = "LOW"       # Low volatility (±0-5%)

    # ✅ TEMPORARY: Generate hash locally without blockchain
    # This creates the hash but doesn't store it on Ethereum
    data_string = json.dumps(data.dict())
    data_hash = hashlib.sha256(data_string.encode()).hexdigest()
    
    # Mock transaction hash for testing
    mock_tx_hash = "0x" + hashlib.sha256((data_hash + "mock").encode()).hexdigest()[:64]

    return {
        "predicted_price": round(prediction, 2),
        "percent_change": round(change_percent, 2),
        "risk": risk,
        "blockchain_hash": data_hash,
        "transaction_hash": mock_tx_hash,
        "note": "⚠️ Running in TEST MODE - blockchain disabled"
    }