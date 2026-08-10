# import requests
import json
import pandas as pd
import sqlite3

# url = "https://api.open-meteo.com/v1/forecast?latitude=23.2599&longitude=77.4126&current=temperature_2m,relative_humidity_2m,wind_speed_10m"

# response = requests.get(url)

# data = response.json()

# temperature = data["current"]["temperature_2m"]
# humidity = data["current"]["relative_humidity_2m"]
# wind_speed = data["current"]["wind_speed_10m"]

# print("Temperature:", temperature)
# print("Humidity:", humidity)
# print("Wind Speed:", wind_speed)

# with open("raw_data.json", "w") as file:
#     json.dump(data,file,indent=4)
    


with open("raw_data.json", "r") as file:
    data = json.load(file)

current_data = data["current"]
clean_data = {
    "time": current_data["time"],
    "temperature": current_data["temperature_2m"],
    "humidity": current_data["relative_humidity_2m"],
    "wind_speed": current_data["wind_speed_10m"]
}

print(clean_data)

df=pd.DataFrame([clean_data])

print(df)

connection = sqlite3.connect("weather.db")

df.to_sql("weather_data",connection , if_exists="replace", index= False)

cursor = connection.cursor()

# cursor.execute("""
# SELECT name FROM sqlite_master
# WHERE type='table';
# """)

# print(cursor.fetchall())

cursor.execute("SELECT * FROM weather_data")

rows = cursor.fetchall()

print(rows)

connection.close()