import httpx

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "শহরের এখনকার তাপমাত্রা, বাতাস ও বৃষ্টি দেখে।",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "ইংরেজিতে শহরের নাম"},
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_forecast",
            "description": "আগামী কয়েক দিনের তাপমাত্রা ও বৃষ্টির সম্ভাবনা দেখে।",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "ইংরেজিতে শহরের নাম"},
                    "days": {
                        "type": "integer",
                        "description": "১ = আজ, ২ = আজ ও আগামীকাল; সর্বোচ্চ ৭",
                    },
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "convert_temperature",
            "description": "সেলসিয়াসকে ফারেনহাইটে বা উল্টোটায় বদলায়।",
            "parameters": {
                "type": "object",
                "properties": {
                    "value": {"type": "number", "description": "তাপমাত্রার মান"},
                    "unit": {"type": "string", "description": "C অথবা F"},
                },
                "required": ["value", "unit"],
            },
        },
    },
]


def find_city(city):
    response = httpx.get(
        GEO_URL,
        params={"name": city, "count": 1, "language": "en"},
        timeout=10,
        trust_env=False,
    )
    results = response.json().get("results")

    if not results:
        return None

    return results[0]


def get_current_weather(city):
    place = find_city(city)

    if place is None:
        return f"'{city}' শহরটি পাওয়া যায়নি।"

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
    current = response.json()["current"]

    return (
        f"{place['name']} ({place.get('country', '')}): এখন "
        f"{current['temperature_2m']}°C, বাতাস {current['wind_speed_10m']} km/h, "
        f"বৃষ্টি {current['precipitation']} mm"
    )


def get_forecast(city, days=3):
    place = find_city(city)

    if place is None:
        return f"'{city}' শহরটি পাওয়া যায়নি।"

    days = int(days)
    if days < 1:
        days = 1
    if days > 7:
        days = 7

    response = httpx.get(
        WEATHER_URL,
        params={
            "latitude": place["latitude"],
            "longitude": place["longitude"],
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
            "forecast_days": days,
            "timezone": "auto",
        },
        timeout=10,
        trust_env=False,
    )
    daily = response.json()["daily"]

    labels = ["আজ", "আগামীকাল", "পরশু"]
    lines = []

    for i in range(len(daily["time"])):
        label = labels[i] if i < len(labels) else f"{i} দিন পরে"
        lines.append(
            f"{label} ({daily['time'][i]}): "
            f"সর্বোচ্চ {daily['temperature_2m_max'][i]}°C, "
            f"সর্বনিম্ন {daily['temperature_2m_min'][i]}°C, "
            f"বৃষ্টির সম্ভাবনা {daily['precipitation_probability_max'][i]}%"
        )

    return "\n".join(lines)


def convert_temperature(value, unit):
    value = float(value)
    unit = str(unit).lower()

    if unit.startswith("c"):
        return f"{value}°C = {value * 9 / 5 + 32:.1f}°F"

    if unit.startswith("f"):
        return f"{value}°F = {(value - 32) * 5 / 9:.1f}°C"

    return "unit হবে C অথবা F।"


def run_tool(name, args):
    try:
        if name == "get_current_weather":
            return get_current_weather(**args)

        if name == "get_forecast":
            return get_forecast(**args)

        if name == "convert_temperature":
            return convert_temperature(**args)

        return f"'{name}' নামে কোনো টুল নেই।"
    except Exception as error:
        return f"টুল চালাতে সমস্যা: {error}"
