from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from blockchain import store_hash

app = FastAPI()

model = joblib.load("saved_model.pkl")

# ✅ Define InputData HERE (outside function)
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

    if change_percent > 10:
        risk = "HIGH"
    elif change_percent > 5:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    blockchain_result = store_hash(data.dict())


    return {
    "predicted_price": round(prediction, 2),
    "percent_change": round(change_percent, 2),
    "risk": risk,
    "blockchain_hash": blockchain_result["data_hash"],
    "transaction_hash": blockchain_result["transaction_hash"]
}

