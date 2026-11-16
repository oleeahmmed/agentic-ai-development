import httpx

CITY_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "একটি শহরের এখনকার আবহাওয়া দেখে।",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "ইংরেজিতে শহরের নাম, যেমন Dhaka"},
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_forecast",
            "description": "একটি শহরের আগামী ৩ দিনের আবহাওয়া দেখে।",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "ইংরেজিতে শহরের নাম, যেমন Dhaka"},
                },
                "required": ["city"],
            },
        },
    },
]


def find_city(city):
    response = httpx.get(
        CITY_URL,
        params={"name": city, "count": 1},
        timeout=10,
        trust_env=False,
    )
    places = response.json().get("results")
    return places[0] if places else None


def get_weather(city):
    place = find_city(city)

    if place is None:
        return f"{city} শহর পাওয়া যায়নি।"

    response = httpx.get(
        WEATHER_URL,
        params={
            "latitude": place["latitude"],
            "longitude": place["longitude"],
            "current": "temperature_2m,wind_speed_10m,precipitation",
            "timezone": "auto",
        },
        timeout=10,
        trust_env=False,
    )
    now = response.json()["current"]

    return (
        f"{place['name']}: এখন {now['temperature_2m']}°C, "
        f"বাতাস {now['wind_speed_10m']} km/h, বৃষ্টি {now['precipitation']} mm"
    )


def get_forecast(city):
    place = find_city(city)

    if place is None:
        return f"{city} শহর পাওয়া যায়নি।"

    response = httpx.get(
        WEATHER_URL,
        params={
            "latitude": place["latitude"],
            "longitude": place["longitude"],
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
            "forecast_days": 3,
            "timezone": "auto",
        },
        timeout=10,
        trust_env=False,
    )
    daily = response.json()["daily"]
    lines = []

    for i in range(3):
        lines.append(
            f"{daily['time'][i]}: সর্বোচ্চ {daily['temperature_2m_max'][i]}°C, "
            f"সর্বনিম্ন {daily['temperature_2m_min'][i]}°C, "
            f"বৃষ্টির সম্ভাবনা {daily['precipitation_probability_max'][i]}%"
        )

    return "\n".join(lines)


def run_tool(name, args):
    try:
        if name == "get_weather":
            return get_weather(**args)
        if name == "get_forecast":
            return get_forecast(**args)
        return f"{name} নামে কোনো টুল নেই।"
    except Exception as error:
        return f"টুল চালাতে সমস্যা: {error}"
