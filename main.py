import requests
import json

url = "https://api.open-meteo.com/v1/forecast?latitude=23.2599&longitude=77.4126&current=temperature_2m,relative_humidity_2m,wind_speed_10m"

response = requests.get(url)

data = response.json()

temperature = data["current"]["temperature_2m"]
humidity = data["current"]["relative_humidity_2m"]
wind_speed = data["current"]["wind_speed_10m"]

print("Temperature:", temperature)
print("Humidity:", humidity)
print("Wind Speed:", wind_speed)

with open("raw_data.json", "w") as file:
    json.dump(data,file,indent=4)