import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

# -----------------------------
# CONFIG
# -----------------------------

NUM_ROWS = 10000

buildings = [
    "ILAB",
    "CBT",
    "Mosque",
    "International Hostel Female",
    "International Hostel Male",
    "LR 11",
    "LR 12",
    "LR 13",
    "LR 14",
    "LR 15",
    "LR 16",
]

time_blocks = [
    "12AM-3AM",
    "3AM-6AM",
    "6AM-9AM",
    "9AM-12PM",
    "12PM-3PM",
    "3PM-6PM",
    "6PM-9PM",
    "9PM-12AM"
]

weather_conditions = [
    "Sunny",
    "Cloudy",
    "Rainy",
    "Stormy"
]

maintenance_levels = [
    "Good",
    "Fair",
    "Poor"
]

occupancy_levels = [
    "Low",
    "Medium",
    "High"
]

# -----------------------------
# GENERATE DATA
# -----------------------------

data = []

start_date = datetime(2025, 1, 1)

for i in range(NUM_ROWS):

    date = start_date + timedelta(days=random.randint(0, 365))

    building = random.choice(buildings)

    time_block = random.choice(time_blocks)

    weather = random.choice(weather_conditions)

    # Weather-related values
    if weather == "Sunny":
        temperature = round(random.uniform(28, 38), 1)
        humidity = random.randint(30, 55)
        rainfall = 0
        wind_speed = random.randint(5, 15)

    elif weather == "Cloudy":
        temperature = round(random.uniform(24, 32), 1)
        humidity = random.randint(45, 70)
        rainfall = round(random.uniform(0, 5), 1)
        wind_speed = random.randint(8, 18)

    elif weather == "Rainy":
        temperature = round(random.uniform(20, 28), 1)
        humidity = random.randint(70, 90)
        rainfall = round(random.uniform(5, 20), 1)
        wind_speed = random.randint(10, 25)

    else:  # Stormy
        temperature = round(random.uniform(18, 26), 1)
        humidity = random.randint(80, 100)
        rainfall = round(random.uniform(15, 40), 1)
        wind_speed = random.randint(20, 45)

    # Electrical features
    transformer_load = random.randint(30, 100)

    grid_voltage = round(random.uniform(180, 240), 1)

    fuel_level = random.randint(10, 100)

    maintenance = random.choice(maintenance_levels)

    occupancy = random.choice(occupancy_levels)

    previous_outages = random.randint(0, 10)

    # Generator logic
    if fuel_level < 20:
        generator_status = "Inactive"
    else:
        generator_status = "Active"

    # -----------------------------
    # RISK LOGIC
    # -----------------------------


    risk_score = 0

    if weather == "Stormy":
        risk_score += 2

    if transformer_load > 95:
        risk_score += 3

    if grid_voltage < 185:
        risk_score += 3



    if maintenance == "Poor":
        risk_score += 1

    if fuel_level < 20:
        risk_score += 1

    if previous_outages > 5:
        risk_score += 1

    # -----------------------------
    # DETERMINE RISK LEVEL
    # -----------------------------

    if risk_score <= 2:
        outage_risk_level = "Low"

    elif risk_score <= 4:
        outage_risk_level = "Medium"

    elif risk_score <= 6:
        outage_risk_level = "High"

    else:
        outage_risk_level = "Critical"

    # -----------------------------
    # SAVE ROW
    # -----------------------------

    data.append([
        date.strftime("%Y-%m-%d"),
        time_block,
        building,
        weather,
        temperature,
        humidity,
        rainfall,
        wind_speed,
        transformer_load,
        grid_voltage,
        generator_status,
        fuel_level,
        maintenance,
        occupancy,
        previous_outages,
        outage_risk_level
    ])

# -----------------------------
# CREATE DATAFRAME
# -----------------------------

columns = [
    "date",
    "time_block",
    "building",
    "weather_condition",
    "temperature_c",
    "humidity_percent",
    "rainfall_mm",
    "wind_speed_kmh",
    "transformer_load_percent",
    "grid_voltage",
    "generator_status",
    "fuel_level_percent",
    "maintenance_status",
    "occupancy_level",
    "previous_outages_7days",
    "outage_risk_level"
]

df = pd.DataFrame(data, columns=columns)

# -----------------------------
# SAVE CSV
# -----------------------------

df.to_csv("synthetic_outage_dataset.csv", index=False)

print("Dataset generated successfully!")
print(df.head())
print(df["outage_risk_level"].value_counts())