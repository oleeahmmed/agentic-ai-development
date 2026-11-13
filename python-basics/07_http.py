import httpx

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 23.81,
    "longitude": 90.41,
    "current": "temperature_2m",
}

response = httpx.get(url, params=params, timeout=10, trust_env=False)

print("HTTP status:", response.status_code)

data = response.json()
print("ঢাকার তাপমাত্রা:", data["current"]["temperature_2m"], "°C")
