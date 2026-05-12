
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# ----------------------------
# LOAD DATA
# ----------------------------
df = pd.read_csv("synthetic_outage_dataset.csv")

# ----------------------------
# DATE FEATURE ENGINEERING
# ----------------------------
df["date"] = pd.to_datetime(df["date"])
df["day"] = df["date"].dt.day
df["month"] = df["date"].dt.month
df = df.drop("date", axis=1)

# ----------------------------
# ORDINAL ENCODING (HAS ORDER)
# ----------------------------
time_map = {
    "12AM-3AM": 0,
    "3AM-6AM": 1,
    "6AM-9AM": 2,
    "9AM-12PM": 3,
    "12PM-3PM": 4,
    "3PM-6PM": 5,
    "6PM-9PM": 6,
    "9PM-12AM": 7
}

occupancy_map = {
    "Low": 0,
    "Medium": 1,
    "High": 2
}

maintenance_map = {
    "Poor": 0,
    "Fair": 1,
    "Good": 2
}

df["time_block"] = df["time_block"].map(time_map)
df["occupancy_level"] = df["occupancy_level"].map(occupancy_map)
df["maintenance_status"] = df["maintenance_status"].map(maintenance_map)

# ----------------------------
# LABEL ENCODING (NO ORDER / MANY VALUES)
# ----------------------------
df["building"] = df["building"].astype("category").cat.codes

# ----------------------------
# ONE-HOT ENCODING (NO ORDER)
# ----------------------------
weather_map = {
    "Sunny": 0,
    "Cloudy": 1,
    "Rainy": 2,
    "Stormy": 3
}

df["weather_condition"] = df["weather_condition"].map(weather_map)

# ----------------------------
# TARGET ENCODING (OUTAGE RISK)
# ----------------------------

risk_map = {
    "Low": 0,
    "Medium": 1,
    "High": 2,
    "Critical": 3
}

df["outage_risk_level"] = df["outage_risk_level"].map(risk_map)

inverse_risk_map = {v: k for k, v in risk_map.items()}
print(inverse_risk_map)

# ----------------------------
# FIX generator_status
# ----------------------------
df["generator_status"] = df["generator_status"].map({
    "Inactive": 0,
    "Active": 1
})

# ----------------------------
# TARGET VARIABLE
# ----------------------------
df["outage_risk_level"] = df["outage_risk_level"].astype("category").cat.codes

# ----------------------------
# SPLIT DATA
# ----------------------------
X = df.drop("outage_risk_level", axis=1)
y = df["outage_risk_level"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


print(df["outage_risk_level"].unique())
# ----------------------------
# TRAIN MODEL
# ----------------------------
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

# ----------------------------
# EVALUATE
# ----------------------------
accuracy = model.score(X_test, y_test)
print("Model Accuracy:", accuracy)

# ----------------------------
# SAVE MODEL
# ----------------------------
joblib.dump(model, "model.pkl")

print("Model trained and saved successfully!")

print(X.columns)
