# Phase 3 — Weather Agent (সহজ গাইড)

> **লক্ষ্য:** LLM-এর হাতে "হাত" দেওয়া — যেন সে নিজে টুল চালিয়ে সত্য তথ্য এনে উত্তর দেয়।
> **সময়:** ৩–৫ দিন, দিনে ৩০–৬০ মিনিট।

---

## শুরুর আগে

Phase 0-এর `.env` ঠিক থাকতে হবে। একবার দেখে নিন:

```bash
source .venv/Scripts/activate
python 00-setup/check_env.py
```

সব "আছে" দেখালে এগিয়ে যান।

---

## গল্প: মিতুর হাতে এখন হাত

আগের ফেজে মিতু কথা বলতে পারত, মনে রাখত, কিন্তু **অর্ডার A102 কোথায়** জিজ্ঞেস করলে বানিয়ে বলত। কারণ তার চোখ নেই, হাত নেই।

Weather Agent-এ আমরা মিতুকে প্রথম **টুল** দেব — আবহাওয়া দেখার হাত।

খেয়াল করুন: LLM নিজে ইন্টারনেটে যায় না। **টুলটা চলে আপনার কম্পিউটারে।** LLM শুধু বলে:

> "আমি `get_current_weather` টুলটা চাই, ইনপুট `Dhaka`।"

তারপর আপনার কোড সেটা চালায়, ফলাফল আবার LLM-কে দেয়। এটাই **function calling**।

---

## এই ফোল্ডারে কী আছে

| ফাইল | কাজ |
|---|---|
| `prompts/system.md` | আবহাওয়া সহকারীর নিয়ম |
| `tools.py` | ৩টি টুলের কোড ও বর্ণনা |
| `01_test_tools.py` | LLM ছাড়া টুলগুলো পরীক্ষা |
| `02_agent_loop.py` | নিজের লেখা agent loop |

> Open-Meteo API ফ্রি, কোনো key লাগে না। ইন্টারনেট থাকলেই হবে।

---

## টুলের ৩টি অংশ

| অংশ | কে ব্যবহার করে |
|---|---|
| `TOOLS` — টুলের নাম, কাজ, ইনপুটের বর্ণনা | **মডেল** পড়ে, বোঝে কোন টুল কখন লাগবে |
| `get_current_weather(...)` এরকম function | **আপনার কম্পিউটার** চালায় |
| `run_tool(name, args)` | নাম দেখে সঠিক function ডাকে |

মডেল কোড চালাতে পারে না। সে শুধু **কোন টুল, কোন ইনপুট** চায় তা বলে। চালানোর দায়িত্ব আমাদের।

---

# পাঠ ১ — `tools.py`

**কোথায়:** `02-weather-agent/tools.py`

```python
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
```

এই ফাইলটা চালালে কিছুই হবে না — কারণ এখানে print নেই। এটা টুলের **ভাণ্ডার**।

### কোন অংশ কী কাজ করে

| অংশ | কাজ |
|---|---|
| `GEO_URL` | শহরের নাম → অক্ষাংশ/দ্রাঘিমাংশ (Open-Meteo geocoding) |
| `WEATHER_URL` | সেই জায়গার আবহাওয়া |
| `TOOLS` | মডেলের জন্য টুলের তালিকা (নাম, কাজ, ইনপুট) |
| `"required": ["city"]` | `city` ছাড়া টুল চলবে না |
| `find_city(city)` | নাম দিয়ে শহর খোঁজা; না পেলে `None` |
| `get_current_weather(city)` | এখনকার তাপমাত্রা, বাতাস, বৃষ্টি |
| `get_forecast(city, days)` | কয়েক দিনের পূর্বাভাস; `days` ১–৭-এ সীমিত |
| `labels = ["আজ", "আগামীকাল", "পরশু"]` | মডেলকে তারিখ বুঝতে সুবিধা |
| `convert_temperature(value, unit)` | °C ↔ °F |
| `run_tool(name, args)` | নাম দেখে সঠিক function ডাকে |
| `**args` | dict-কে function-এর ইনপুটে ভেঙে দেয় |
| `try / except` | ভুল ইনপুটে এজেন্ট থেমে যায় না, মডেলকে error জানায় |

> `trust_env=False` কেন? Phase 1-এ দেখেছেন — কম্পিউটারের ভাঙা proxy সেটিং এড়াতে।

---

# পাঠ ২ — টুল পরীক্ষা: `01_test_tools.py`

LLM-কে দেওয়ার আগে টুল ঠিক আছে কি না নিজে দেখুন।

**ফাইল:** `01_test_tools.py`

```python
import sys

from tools import get_current_weather, get_forecast, convert_temperature

sys.stdout.reconfigure(encoding="utf-8")

print("১. এখনকার আবহাওয়া")
print(get_current_weather("Dhaka"))
print()

print("২. ৩ দিনের পূর্বাভাস")
print(get_forecast("Chattogram", 3))
print()

print("৩. তাপমাত্রা রূপান্তর")
print(convert_temperature(30, "C"))
print()

print("৪. ভুল শহর")
print(get_current_weather("Xyzzyville"))
```

**চালান:**

```bash
python 02-weather-agent/01_test_tools.py
```

**ফলাফল (তাপমাত্রা ও তারিখ বদলাবে):**

```
১. এখনকার আবহাওয়া
Dhaka (Bangladesh): এখন 22.2°C, বাতাস 6.9 km/h, বৃষ্টি 0.0 mm

২. ৩ দিনের পূর্বাভাস
আজ (2026-11-14): সর্বোচ্চ 29.6°C, সর্বনিম্ন 21.1°C, বৃষ্টির সম্ভাবনা 0%
আগামীকাল (2026-11-15): সর্বোচ্চ 29.1°C, সর্বনিম্ন 19.8°C, বৃষ্টির সম্ভাবনা 0%
পরশু (2026-11-16): সর্বোচ্চ 29.3°C, সর্বনিম্ন 20.4°C, বৃষ্টির সম্ভাবনা 0%

৩. তাপমাত্রা রূপান্তর
30.0°C = 86.0°F

৪. ভুল শহর
'Xyzzyville' শহরটি পাওয়া যায়নি।
```

### কোন অংশ কী কাজ করে

| অংশ | কাজ |
|---|---|
| `from tools import ...` | পাশের `tools.py` থেকে function আনা |
| `get_current_weather("Dhaka")` | সরাসরি function ডাকা — LLM নেই |
| `get_forecast("Chattogram", 3)` | শহর + কত দিন |
| `convert_temperature(30, "C")` | ৩০°C → ফারেনহাইট |
| `Xyzzyville` | কাল্পনিক শহর — ভদ্রভাবে ব্যর্থ হয় |

> **নিয়ম:** টুল আগে আলাদা করে পরীক্ষা করুন। টুল ভাঙা থাকলে LLM-কে দোষ দিয়ে লাভ নেই।

---

# পাঠ ৩ — `prompts/system.md`

**কোথায়:** `02-weather-agent/prompts/system.md`

```markdown
# আবহাওয়া সহকারী

তুমি Little Office Ltd.-এর আবহাওয়া সহকারী।

## নিয়ম

- আবহাওয়ার উত্তর দিতে সবসময় টুল ব্যবহার করো। নিজের জানা থেকে অনুমান করো না।
- শহরের নাম ইংরেজিতে দাও (ঢাকা → Dhaka, চট্টগ্রাম → Chattogram, সিলেট → Sylhet)।
- টুল ব্যর্থ হলে সত্যি বলো। বানিয়ে উত্তর দেবে না।
- সংক্ষেপে বাংলায় উত্তর দাও।
```

দুইটা লাইন বিশেষভাবে খেয়াল করুন:

- **"ইংরেজিতে শহরের নাম"** — Open-Meteo বাংলা লেখা চিনতে পারে না। `চট্টগ্রাম` দিলে "শহর পাওয়া যায়নি" আসে, কিন্তু `Chattogram` দিলে ঠিকঠাক।
- **"সবসময় টুল ব্যবহার করো"** — নইলে মডেল নিজের পুরোনো জানা থেকে অনুমান করে দিতে পারে।

---

# পাঠ ৪ — agent loop: `02_agent_loop.py`

এটাই এই ফেজের আসল শিক্ষা। কোনো ফ্রেমওয়ার্ক নেই — শুধু একটা `while` আর একটা `for`।

**ফাইল:** `02_agent_loop.py`

```python
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from tools import TOOLS, run_tool

sys.stdout.reconfigure(encoding="utf-8")

base = Path(__file__).parent
load_dotenv(base.parent / "00-setup" / ".env")

api_key = os.getenv("LLM_API_KEY")
model = os.getenv("LLM_MODEL")

if not api_key or not model:
    print("00-setup/.env ফাইলে LLM_API_KEY আর LLM_MODEL দিন।")
    sys.exit()

system_prompt = (base / "prompts" / "system.md").read_text(encoding="utf-8")

client = OpenAI(api_key=api_key, base_url=os.getenv("LLM_BASE_URL"))

messages = [{"role": "system", "content": system_prompt}]

print("আবহাওয়া এজেন্ট। exit = বন্ধ")

while True:
    question = input("তুমি: ").strip()

    if question == "exit":
        break

    if not question:
        continue

    messages.append({"role": "user", "content": question})

    for step in range(5):
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOLS,
        )
        message = response.choices[0].message
        messages.append(message)

        if not message.tool_calls:
            print("এজেন্ট:", message.content)
            break

        for call in message.tool_calls:
            name = call.function.name
            args = json.loads(call.function.arguments or "{}")
            result = run_tool(name, args)

            print("  [টুল]", name, args)
            print("  [ফলাফল]", result)

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": result,
                }
            )
    else:
        print("এজেন্ট: ৫ ধাপেও উত্তর মিলল না।")

print("বন্ধ হলো।")
```

**চালান:**

```bash
python 02-weather-agent/02_agent_loop.py
```

**এভাবে কথা বলুন:**

```
আবহাওয়া এজেন্ট। exit = বন্ধ
তুমি: আজ ঢাকার আবহাওয়া কেমন?
  [টুল] get_current_weather {'city': 'Dhaka'}
  [ফলাফল] Dhaka (Bangladesh): এখন 22.2°C, বাতাস 6.9 km/h, বৃষ্টি 0.0 mm
এজেন্ট: ঢাকায় এখন ২২.২°C তাপমাত্রা, বাতাস ৬.৯ কিমি/ঘন্টা এবং বৃষ্টি নেই (০.০ মিমি)।
তুমি: ৩০ ডিগ্রি সেলসিয়াস ফারেনহাইটে কত?
  [টুল] convert_temperature {'value': 30, 'unit': 'C'}
  [ফলাফল] 30.0°C = 86.0°F
এজেন্ট: ৩০°C = ৮৬°F
তুমি: exit
বন্ধ হলো।
```

### লুপটা ৫ ধাপে

1. আপনার প্রশ্ন `messages`-এ যোগ হয়।
2. **মডেল দেখে:** উত্তর দেব, নাকি টুল লাগবে?
3. টুল লাগলে মডেল বলে — কোন টুল, কোন ইনপুট।
4. আপনার কোড টুল চালায়, ফলাফল `role: "tool"` হিসেবে `messages`-এ যায়।
5. মডেল আবার দেখে — এবার ফলাফল পেয়েছে, তাই উত্তর দেয়।

টুল লাগলে ২–৫ আবার ঘোরে। `range(5)` মানে **সর্বোচ্চ ৫ ধাপ** — যাতে ভুল হলে অনন্তকাল না ঘোরে।

### কোন অংশ কী কাজ করে

| অংশ | কাজ |
|---|---|
| `from tools import TOOLS, run_tool` | টুলের তালিকা ও চালানোর function |
| `for step in range(5)` | এক প্রশ্নে সর্বোচ্চ ৫ ধাপ |
| `tools=TOOLS` | মডেলকে টুলগুলোর তালিকা দেখানো |
| `message.tool_calls` | মডেল টুল চাইলে এখানে তথ্য থাকে; না চাইলে খালি |
| `if not message.tool_calls:` | টুল নেই = চূড়ান্ত উত্তর |
| `messages.append(message)` | মডেলের উত্তর/টুল-অনুরোধ খাতায় রাখা |
| `call.function.name` | কোন টুল চাইছে |
| `json.loads(...)` | ইনপুটের লেখা → dict |
| `run_tool(name, args)` | আসল function চালানো |
| `"role": "tool"` | "এই ফলাফল তোমার ওই টুল-কলের উত্তর" |
| `"tool_call_id": call.id` | কোন কলের ফলাফল তা মেলানো |
| `for ... else` | ৫ ধাপ শেষেও উত্তর না এলে বার্তা |
| `break` | চূড়ান্ত উত্তর পেলে ভিতরের লুপ শেষ |

### সবচেয়ে গুরুত্বপূর্ণ লাইন

```python
messages.append(
    {
        "role": "tool",
        "tool_call_id": call.id,
        "content": result,
    }
)
```

`tool_call_id` না দিলে মডেল বুঝবে না কোন ফলাফল কোন অনুরোধের। তখন সে হয় ভুল উত্তর দেবে, নয় আবার টুল চাইবে।

**খেয়াল করুন:** মডেল কিন্তু নিজে থেকে আবহাওয়া জানে না। ২২.২°C সংখ্যাটা এসেছে Open-Meteo থেকে, আপনার কোড দিয়ে। মডেল শুধু সেটাকে বাংলায় সাজিয়ে দিয়েছে।

---

# পরীক্ষা — ৫টি প্রশ্ন

`02_agent_loop.py` চালিয়ে একে একে জিজ্ঞেস করুন:

| # | প্রশ্ন | প্রত্যাশা |
|---|---|---|
| 1 | আজ ঢাকার আবহাওয়া কেমন? | `get_current_weather` ডাকে, সত্য তাপমাত্রা বলে |
| 2 | আগামীকাল চট্টগ্রামে বৃষ্টি হবে? | `get_forecast` ডাকে, বৃষ্টির সম্ভাবনা বলে |
| 3 | ৩০ ডিগ্রি সেলসিয়াস ফারেনহাইটে কত? | `convert_temperature` ডাকে, ৮৬°F বলে |
| 4 | Xyzzyville-এ আবহাওয়া কেমন? | "শহর পাওয়া যায়নি" — বানিয়ে বলে না |
| 5 | তুমি কে? | টুল ছাড়াই নিজের পরিচয় দেয় |

> টুলের ইনপুট হুবহু মিলবে না সব সময় — যেমন মডেল `days: 2` দিতে পারে `3`-এর বদলে। মূল কথা হলো **সঠিক টুল, সঠিক শহর**।

### একটা ছোট পরীক্ষা

প্রশ্ন করুন: **"আজ ঢাকায় বৃষ্টি হবে?"**

প্রথমে মডেল `get_current_weather` ডাকতে পারে। কিন্তু "আজ সারাদিন" জানতে `get_forecast` লাগে। মডেল হয়তো দুটোই ডাকবে। এতে ভয় নেই — লুপ ৫ ধাপ পর্যন্ত সইবে।

---

## hallucination গেল কোথায়?

Phase 2-এ মিতু "Little Office Ltd. নেই" জেনেও ভদ্র উত্তর দিয়েছিল। কারণ তার কাছে তথ্য ছিল না।

এখন আবহাওয়ার প্রশ্নে তথ্য আসে **বাইরের API থেকে**, তাই বানানোর সুযোগ কম। তবে সম্পূর্ণ নিশ্চিন্ত নয়:

- শহরের নাম ভুল হলে টুল ব্যর্থ হয় — তখন মডেলকে সত্যি বলতে হয়।
- ফ্রি মডেল কখনো টুল না ডেকে অনুমান করে দিতে পারে। এজন্য `system.md`-এ স্পষ্ট নিয়ম লিখেছি।
- ভবিষ্যতে উত্তর **যাচাই** করবেন কীভাবে — শিখবেন Phase 9-এ।

---

## ভালো টুলের ৩টি নিয়ম

1. **ছোট ও একটি কাজ** — `get_weather_and_news_and_email` নয়; আলাদা টুল।
2. **পরিষ্কার নাম ও বর্ণনা** — মডেল বর্ণনা পড়েই সিদ্ধান্ত নেয়।
3. **ইনপুট বিশ্বাস করবেন না** — `days=99` এলেও ৭-এ কেটে দিন; error হলে মডেলকে জানান।

---

## সমস্যা হলে

| যা দেখছেন | সমাধান |
|---|---|
| `ModuleNotFoundError: httpx` | `.venv` চালু করুন, `pip install -r 00-setup/requirements.txt` |
| `401` / `404` | `.env`-এর key, base URL, model নাম দেখুন |
| `429` | ফ্রি মডেল ব্যস্ত — কিছুক্ষণ পরে চেষ্টা করুন |
| টুল ডাকেই না, বানিয়ে বলে | `prompts/system.md`-এর নিয়ম দেখুন; মডেল বদলে চেষ্টা করুন |
| `'...' শহরটি পাওয়া যায়নি` | ইংরেজি নাম দিন (Dhaka, Sylhet) |
| ইন্টারনেট নেই | `ConnectError` আসবে — সংযোগ ঠিক করে আবার চালান |

---

## শেষ চেকলিস্ট

- [ ] `01_test_tools.py` চালিয়ে ৪টি ফলাফল দেখেছেন
- [ ] `tools.py`-এর `TOOLS` আর function-এর পার্থক্য বলতে পারেন
- [ ] `02_agent_loop.py` চালিয়ে টুল কল লগ দেখেছেন
- [ ] ৫টি প্রশ্নের পরীক্ষা করেছেন
- [ ] ভুয়া শহরে বানিয়ে উত্তর দেয় না — নিশ্চিত হয়েছেন
- [ ] `tool_call_id` কেন লাগে বলতে পারেন
- [ ] loop-এর প্রতিটি লাইন নিজে ব্যাখ্যা করতে পারেন

---

## পরের ধাপ

Phase 4 — **Memory Friend** (ফোল্ডার: [`03-memory-friend`](../03-memory-friend/README.md))।
এখন মিতু শুধু চলতি কথোপকথন মনে রাখে। পরের ফেজে প্রোগ্রাম বন্ধ করেও নাম-পছন্দ মনে রাখবে।
