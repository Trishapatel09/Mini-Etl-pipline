# IMPORTS

import requests
import json
import pandas as pd
import sqlite3

# EXTRACT - Fetch data from API

url = "https://api.open-meteo.com/v1/forecast?latitude=23.2599&longitude=77.4126&current=temperature_2m,relative_humidity_2m,wind_speed_10m"

response = requests.get(url)

data = response.json()

# Save raw API data as JSON

with open("raw_data.json", "w") as file:
    json.dump(data, file, indent=4)


# Read raw JSON data

try:
    with open("raw_data.json", "r") as file:
        data = json.load(file)

except FileNotFoundError:
    print("raw_data.json file not found")
    exit()

except json.JSONDecodeError:
    print("Invalid JSON data")
    exit()


# TRANSFORM - Clean the data

current_data = data["current"]

clean_data = {
    "time": current_data["time"],
    "temperature": current_data["temperature_2m"],
    "humidity": current_data["relative_humidity_2m"],
    "wind_speed": current_data["wind_speed_10m"]
}


# Convert cleaned data into DataFrame

df = pd.DataFrame([clean_data])


# VALIDATE - Check data quality

print("Missing values:")
print(df.isnull().sum())

print("Duplicate rows:")
print(df.duplicated().sum())

print("Data types:")
print(df.dtypes)

print("Humidity valid:")
print(df["humidity"].between(0, 100).all())


# LOAD - Store data in SQLite

try:
    connection = sqlite3.connect("weather.db")

    df.to_sql(
        "weather_data",
        connection,
        if_exists="replace",
        index=False
    )

except sqlite3.Error:
    print("Database error occurred")
    exit()


# VERIFY - Check stored data

cursor = connection.cursor()

cursor.execute("SELECT * FROM weather_data")

rows = cursor.fetchall()

print("Stored data:")
print(rows)

connection.close()