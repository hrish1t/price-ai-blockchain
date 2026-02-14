import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

# ---------------------------
# 1️⃣ Load datasets
# ---------------------------

price_df = pd.read_csv("data/prices.csv")
weather_df = pd.read_csv("data/weather.csv")

# Remove accidental spaces
price_df.columns = price_df.columns.str.strip()
weather_df.columns = weather_df.columns.str.strip()

# Convert date column properly
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
df = df[df["crop"] == "onion"]
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
df = df[~df["price"].isna()]

# 4️⃣ Feature Engineering

df["lag_1"] = df["price"].shift(1)
df["lag_2"] = df["price"].shift(2)
df["ma_3"] = df["price"].rolling(3).mean()
df["month"] = df["date"].dt.month

df = df.dropna()

# 5️⃣ Define features
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

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# Split data into train and test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model on training data
model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

# Evaluate model
predictions = model.predict(X_test)
print("R2 Score:", r2_score(y_test, predictions))


model.fit(X, y)

# ---------------------------
# 6️⃣ Save Model
# ---------------------------

joblib.dump(model, "saved_model.pkl")

print("✅ Model trained and saved successfully.")
