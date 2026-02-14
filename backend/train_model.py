import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

# ---------------------------
# 1️⃣ Load datasets
# ---------------------------

price_df = pd.read_csv("data/prices.csv")
weather_df = pd.read_csv("data/weather.csv")

# Parse date column
price_df["date"] = pd.to_datetime(price_df["date"], dayfirst=True)
weather_df["date"] = pd.to_datetime(weather_df["date"], dayfirst=True)

# ---------------------------
# 2️⃣ Merge datasets
# ---------------------------

df = pd.merge(
    price_df,
    weather_df,
    on=["date", "crop", "state"],
    how="inner"
)

# Sort by date
df = df.sort_values("date")

# ---------------------------
# 3️⃣ Feature Engineering
# ---------------------------

# Lag features (previous month price)
df["lag_1"] = df["price"].shift(1)
df["lag_2"] = df["price"].shift(2)

# Rolling average (3-month moving average)
df["ma_3"] = df["price"].rolling(window=3).mean()

# Month feature (seasonality)
df["month"] = df["date"].dt.month

# Drop rows with NaN (due to lag & rolling)
df = df.dropna()

# ---------------------------
# 4️⃣ Define Features & Target
# ---------------------------

X = df[[
    "lag_1",
    "lag_2",
    "ma_3",
    "rainfall",
    "temperature",
    "month"
]]

y = df["price"]

# ---------------------------
# 5️⃣ Train Model
# ---------------------------

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X, y)

# ---------------------------
# 6️⃣ Save Model
# ---------------------------

joblib.dump(model, "saved_model.pkl")

print("✅ Model trained and saved successfully.")
