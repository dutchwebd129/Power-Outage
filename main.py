from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json
import os


import pandas as pd
import numpy as np
import joblib


app = FastAPI()


# -----------------------------
# STATIC + TEMPLATES
# -----------------------------
templates = Jinja2Templates(directory="templates")



app.mount("/static", StaticFiles(directory="static"), name="static")

# -----------------------------
# CORS
# -----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# LOAD MODEL
# -----------------------------

model = joblib.load("model.pkl")





# -----------------------------
# EMAIL MODEL
# -----------------------------

class UserEmail(BaseModel):
    email: str


# -----------------------------
# LANDING PAGE
# -----------------------------

@app.get("/")
def landing_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# -----------------------------
# DASHBOARD PAGE
# -----------------------------

@app.get("/dashboard")
def dashboard(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html"
    )


# -----------------------------
# REGISTER EMAIL
# -----------------------------

@app.post("/register")
async def register(request: Request):

    data = await request.json()
    email = data.get("email")

    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except:
        users = []

    if email not in users:
        users.append(email)

    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

    return {"success": True}
# -----------------------------
# PREDICTION ENDPOINT
# -----------------------------

@app.post("/predict")
def predict(data: dict):

    date = pd.to_datetime(data["date"])

    day = date.day
    month = date.month

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

    generator_map = {
        "Inactive": 0,
        "Active": 1
    }

    weather_map = {
        "Sunny": 0,
        "Cloudy": 1,
        "Rainy": 2,
        "Stormy": 3
    }

    building_map = {
        "ILAB": 0,
        "CBT": 1,
        "Mosque": 2,
        "International Hostel Female": 3,
        "International Hostel Male": 4,
        "LR 11": 5,
        "LR 12": 6,
        "LR 13": 7,
        "LR 14": 8,
        "LR 15": 9,
        "LR 16": 10
    }

    features = np.array([[

        time_map[data["time_block"]],
        building_map[data["building"]],
        weather_map[data["weather_condition"]],
        data["temperature_c"],
        data["humidity_percent"],
        data["rainfall_mm"],
        data["wind_speed_kmh"],
        data["transformer_load_percent"],
        data["grid_voltage"],
        generator_map[data["generator_status"]],
        data["fuel_level_percent"],
        maintenance_map[data["maintenance_status"]],
        occupancy_map[data["occupancy_level"]],
        data["previous_outages_7days"],
        day,
        month
    ]])

    prediction = model.predict(features)[0]

    probabilities = model.predict_proba(features)[0]

    confidence = round(max(probabilities) * 100, 2)

    risk_map = {
        0: "Low",
        1: "Medium",
        2: "High",
        3: "Critical"
    }

    return {
        "predicted_risk": risk_map[int(prediction)],
        "confidence": confidence
    }