from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from blockchain import store_hash

app = FastAPI()

# Load ML model
model = joblib.load("saved_model.pkl")

# Define input schema
class InputData(BaseModel):
    lag_1: float
    lag_2: float
    ma_3: float
    rainfall: float
    temperature: float
    month: int


@app.post("/predict")
def predict(data: InputData):

    # Create dataframe
    input_df = pd.DataFrame([[ 
        data.lag_1,
        data.lag_7,
        data.ma_7,
        data.rainfall,
        data.temperature,
        data.month
    ]], columns=[
        "lag_1",
        "lag_7",
        "ma_7",
        "rainfall",
        "temperature",
        "month"
    ])

    # Predict price
    prediction = model.predict(input_df)[0]

    # Calculate % change
    change_percent = ((prediction - data.lag_1) / data.lag_1) * 100

    if change_percent > 10:
        risk = "HIGH"
    elif change_percent > 5:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    # Store hash on blockchain
    blockchain_result = store_hash(data.dict())

    return {
        "predicted_price": round(prediction, 2),
        "percent_change": round(change_percent, 2),
        "risk": risk,
        "blockchain_hash": blockchain_result["data_hash"],
        "transaction_hash": blockchain_result["transaction_hash"]
    }
