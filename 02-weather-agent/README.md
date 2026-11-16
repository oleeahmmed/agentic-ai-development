# Phase 3 — Weather Agent (সহজ গাইড)

> **লক্ষ্য:** LLM-কে "হাত" দেওয়া — এবং পরিষ্কারভাবে দেখা:
> লুপ কীভাবে টুল বাছাই করে, আর মেমোরিতে তথ্য কীভাবে জমে।
> **সময়:** ২–৩ দিন, দিনে ৩০–৬০ মিনিট।

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

আগের ফেজে মিতু কথা বলতে পারত, মনে রাখত — কিন্তু আবহাওয়া জিজ্ঞেস করলে **বানিয়ে** বলত। কারণ তার নিজের চোখ-হাত নেই।

এবার আমরা মিতুকে দুটো **টুল** দেব:

- `get_weather` — এখনকার আবহাওয়া
- `get_forecast` — আগামী ৩ দিনের পূর্বাভাস

খেয়াল করুন: LLM নিজে ইন্টারনেটে যায় না। **টুল চলে আপনার কম্পিউটারে।** মডেল শুধু বলে:

> "আমি `get_weather` চাই, ইনপুট `Dhaka`।"

তারপর আপনার কোড টুলটা চালায়, ফলাফল আবার মডেলকে দেয়। এটাই **function calling**।

---

## এই ফোল্ডারে কী আছে

| ফাইল | কাজ |
|---|---|
| `tools.py` | ২টি টুল + মডেলের জন্য তাদের বর্ণনা |
| `01_test_tools.py` | LLM ছাড়া টুল পরীক্ষা |
| `prompts/system.md` | সহকারীর নিয়ম |
| `02_agent_loop.py` | নিজের লেখা agent loop |

> Open-Meteo API ফ্রি, কোনো key লাগে না। ইন্টারনেট থাকলেই হবে।

---

## টুলের ৩টি অংশ

| অংশ | কে ব্যবহার করে |
|---|---|
| `TOOLS` — নাম, কাজ, ইনপুটের বর্ণনা | **মডেল** পড়ে, বোঝে কোন টুল কখন লাগবে |
| `get_weather(...)` এরকম আসল function | **আপনার কম্পিউটার** চালায় |
| `run_tool(name, args)` | নাম দেখে সঠিক function ডাকে |

মডেল কোড চালাতে পারে না। সে শুধু বলে **কোন টুল, কোন ইনপুট**। চালানোর দায়িত্ব আমাদের।

---

# পাঠ ১ — `tools.py`

**কোথায়:** `02-weather-agent/tools.py`

```python
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
```

এই ফাইলটা চালালে কিছুই হবে না — এখানে `print` নেই। এটা টুলের **ভাণ্ডার**।

### কোন অংশ কী কাজ করে

| অংশ | কাজ |
|---|---|
| `CITY_URL` | শহরের নাম → অক্ষাংশ/দ্রাঘিমাংশ |
| `WEATHER_URL` | সেই জায়গার আবহাওয়া |
| `TOOLS` | মডেলের জন্য টুলের তালিকা — **মডেল এই বর্ণনাই পড়ে** |
| `"description"` | কখন কোন টুল লাগবে তা এখানেই লেখা |
| `"required": ["city"]` | `city` ছাড়া টুল চলবে না |
| `find_city(city)` | নাম দিয়ে শহর খোঁজা; না পেলে `None` |
| `get_weather(city)` | এখনকার তাপমাত্রা, বাতাস, বৃষ্টি |
| `get_forecast(city)` | ৩ দিনের সর্বোচ্চ/সর্বনিম্ন তাপমাত্রা, বৃষ্টির সম্ভাবনা |
| `run_tool(name, args)` | নাম দেখে সঠিক function ডাকে |
| `**args` | dict-কে function-এর ইনপুটে ভেঙে দেয় |
| `try / except` | ভুল ইনপুটে এজেন্ট থেমে যায় না, মডেলকে error জানায় |

> `trust_env=False` কেন? কম্পিউটারের ভাঙা proxy সেটিং এড়াতে (Phase 1-এ দেখেছেন)।

---

# পাঠ ২ — টুল পরীক্ষা: `01_test_tools.py`

LLM-কে দেওয়ার আগে টুল ঠিক আছে কি না নিজে দেখুন।

**কোথায়:** `02-weather-agent/01_test_tools.py`

```python
import sys

from tools import get_forecast, get_weather

sys.stdout.reconfigure(encoding="utf-8")

print("১. ঢাকার এখনকার আবহাওয়া")
print(get_weather("Dhaka"))

print("\n২. চট্টগ্রামের ৩ দিনের পূর্বাভাস")
print(get_forecast("Chattogram"))

print("\n৩. ভুল শহর")
print(get_weather("Xyzzyville"))
```

**চালান:**

```bash
python 02-weather-agent/01_test_tools.py
```

**ফলাফল (তাপমাত্রা ও তারিখ বদলাবে):**

```
১. ঢাকার এখনকার আবহাওয়া
Dhaka: এখন 25.4°C, বাতাস 1.7 km/h, বৃষ্টি 0.0 mm

২. চট্টগ্রামের ৩ দিনের পূর্বাভাস
2026-11-16: সর্বোচ্চ 29.1°C, সর্বনিম্ন 20.2°C, বৃষ্টির সম্ভাবনা 0%
2026-11-17: সর্বোচ্চ 30.1°C, সর্বনিম্ন 20.1°C, বৃষ্টির সম্ভাবনা 0%
2026-11-18: সর্বোচ্চ 26.8°C, সর্বনিম্ন 21.3°C, বৃষ্টির সম্ভাবনা 38%

৩. ভুল শহর
Xyzzyville শহর পাওয়া যায়নি।
```

### কোন অংশ কী কাজ করে

| অংশ | কাজ |
|---|---|
| `from tools import ...` | পাশের `tools.py` থেকে function আনা |
| `get_weather("Dhaka")` | সরাসরি function ডাকা — LLM নেই |
| `get_forecast("Chattogram")` | শহরের ৩ দিনের পূর্বাভাস |
| `Xyzzyville` | কাল্পনিক শহর — ভদ্রভাবে ব্যর্থ হয় |

> **নিয়ম:** টুল আগে আলাদা করে পরীক্ষা করুন। টুল ভাঙা থাকলে LLM-কে দোষ দিয়ে লাভ নেই।

---

# পাঠ ৩ — `prompts/system.md`

**কোথায়:** `02-weather-agent/prompts/system.md`

```markdown
# আবহাওয়া সহকারী

তুমি Little Office Ltd.-এর আবহাওয়া সহকারী।

## নিয়ম

- আবহাওয়ার প্রশ্নে সবসময় টুল ব্যবহার করো। অনুমান করো না।
- শহরের নাম ইংরেজিতে দাও (ঢাকা → Dhaka)।
- এখনকার আবহাওয়া চাইলে `get_weather`, কয়েক দিনের চাইলে `get_forecast`।
- টুল ব্যর্থ হলে সত্যি বলো। বানিয়ে উত্তর দেবে না।
- সংক্ষেপে বাংলায় উত্তর দাও।
```

দুইটা লাইন বিশেষভাবে খেয়াল করুন:

- **"শহরের নাম ইংরেজিতে"** — Open-Meteo বাংলা লিখে খোঁজে না। `Dhaka` দিলে ঠিক, `ঢাকা` দিলে "শহর পাওয়া যায়নি"।
- **"সবসময় টুল ব্যবহার করো"** — নইলে মডেল নিজের পুরোনো জানা থেকে অনুমান করে দিতে পারে।

---

# পাঠ ৪ — agent loop: `02_agent_loop.py`

এটাই এই ফেজের আসল শিক্ষা। কোনো ফ্রেমওয়ার্ক নেই — শুধু একটা `while` আর একটা `for`।

**কোথায়:** `02-weather-agent/02_agent_loop.py`

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

model = os.getenv("LLM_MODEL")

if not os.getenv("LLM_API_KEY") or not model:
    print("00-setup/.env ফাইলে LLM_API_KEY আর LLM_MODEL দিন।")
    sys.exit()

system_prompt = (base / "prompts" / "system.md").read_text(encoding="utf-8")

client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL"),
)

messages = [{"role": "system", "content": system_prompt}]

print("আবহাওয়া এজেন্ট। mem = মেমোরি দেখো, exit = বন্ধ")

while True:
    question = input("\nতুমি: ").strip()

    if question == "exit":
        break

    if question == "mem":
        for number, item in enumerate(messages, 1):
            role = item["role"] if isinstance(item, dict) else item.role
            print(number, role)
        continue

    if not question:
        continue

    messages.append({"role": "user", "content": question})
    answer = None

    for step in range(1, 5):
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOLS,
        )
        message = response.choices[0].message
        messages.append(message)

        if not message.tool_calls:
            answer = message.content
            break

        for call in message.tool_calls:
            name = call.function.name
            args = json.loads(call.function.arguments or "{}")
            result = run_tool(name, args)

            print(f"[ধাপ {step}] মডেল বাছাই করল: {name} {args}")
            print(f"[ধাপ {step}] টুলের ফল: {result}")

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": result,
                }
            )

    print("এজেন্ট:", answer or "৪ ধাপেও উত্তর পাওয়া যায়নি।")
    print(f"[মেমোরি] এখন {len(messages)}টি মেসেজ জমেছে")

print("বন্ধ হলো।")
```

**চালান:**

```bash
python 02-weather-agent/02_agent_loop.py
```

**এভাবে কথা বলুন:**

```
আবহাওয়া এজেন্ট। mem = মেমোরি দেখো, exit = বন্ধ

তুমি: আজ ঢাকার আবহাওয়া কেমন?
[ধাপ 1] মডেল বাছাই করল: get_weather {'city': 'Dhaka'}
[ধাপ 1] টুলের ফল: Dhaka: এখন 25.4°C, বাতাস 1.7 km/h, বৃষ্টি 0.0 mm
এজেন্ট: ঢাকায় এখন ২৫.৪°C, বাতাস ১.৭ কিমি/ঘণ্টা, বৃষ্টি নেই।
[মেমোরি] এখন 5টি মেসেজ জমেছে

তুমি: আগামীকাল চট্টগ্রামে বৃষ্টি হবে?
[ধাপ 1] মডেল বাছাই করল: get_forecast {'city': 'Chattogram'}
[ধাপ 1] টুলের ফল: 2026-11-16: সর্বোচ্চ 29.1°C, ...
এজেন্ট: আগামীকাল চট্টগ্রামে বৃষ্টির সম্ভাবনা ০%।
[মেমোরি] এখন 9টি মেসেজ জমেছে
```

---

## লুপ কীভাবে টুল বাছাই করে

1. আপনার প্রশ্ন `messages`-এ যোগ হয়।
2. মডেল **`TOOLS`-এর বর্ণনা পড়ে** সিদ্ধান্ত নেয় — উত্তর দেব, নাকি টুল লাগবে।
3. টুল লাগলে মডেল বলে: কোন টুল, কোন ইনপুট। (`message.tool_calls`)
4. আপনার কোড `run_tool(...)` চালায়, ফলাফল `role: "tool"` হিসেবে `messages`-এ যায়।
5. মডেল আবার ডাকা হয় — এবার ফলাফল পেয়েছে, তাই উত্তর দেয়।

| মডেল কী চায় | কোন টুল | কোথা থেকে বোঝে |
|---|---|---|
| "এখন কেমন?" | `get_weather` | description: "**এখনকার** আবহাওয়া" |
| "আগামীকাল/৩ দিন" | `get_forecast` | description: "**আগামী ৩ দিনের**" |
| আবহাওয়া নয় এমন কথা | কিছুই না | টুলের বর্ণনার সাথে মেলে না |

টুল লাগলে ২–৫ ধাপ ঘোরে। `range(1, 5)` মানে **সর্বোচ্চ ৪ ধাপ** — যাতে ভুল হলে অনন্তকাল না ঘোরে।

---

## মেমোরি কীভাবে জমে

এই ফেজে **মেমোরি = `messages` লিস্ট**। প্রতিটি ধাপে নতুন জিনিস যোগ হয়।

প্রথম প্রশ্নের পরে লিস্টে থাকে ৫টি মেসেজ:

| # | role | কী আছে |
|---|---|---|
| 1 | `system` | সহকারীর নিয়ম (`system.md`) |
| 2 | `user` | "আজ ঢাকার আবহাওয়া কেমন?" |
| 3 | `assistant` | "আমি `get_weather` চাই, ইনপুট Dhaka" |
| 4 | `tool` | "Dhaka: এখন 25.4°C..." |
| 5 | `assistant` | "ঢাকায় এখন ২৫.৪°C..." |

দ্বিতীয় প্রশ্নের পরে ৯টি — আগের ৫টি + নতুন ৪টি:

| # | role | কী আছে |
|---|---|---|
| 6 | `user` | "আগামীকাল চট্টগ্রামে বৃষ্টি হবে?" |
| 7 | `assistant` | "আমি `get_forecast` চাই..." |
| 8 | `tool` | "2026-11-16: সর্বোচ্চ 29.1°C..." |
| 9 | `assistant` | "বৃষ্টির সম্ভাবনা ০%" |

**`mem` লিখে নিজে দেখুন:**

```
তুমি: mem
1 system
2 user
3 assistant
4 tool
5 assistant
6 user
7 assistant
8 tool
9 assistant
```

এই লিস্টটাই প্রতিবার পুরোটা মডেলকে পাঠানো হয় — তাই সে আগের কথা মনে রাখতে পারে।

> **সীমা:** `exit` করলে লিস্ট মুছে যায়। পরের ফেজে (Memory Friend) এটা ফাইলে সেভ করা শিখবেন।

---

## কোন অংশ কী কাজ করে

| অংশ | কাজ |
|---|---|
| `messages = [...]` | এজেন্টের মেমোরি (কথোপকথনের খাতা) |
| `question == "mem"` | মেমোরিতে কী কী আছে দেখানো |
| `for step in range(1, 5)` | এক প্রশ্নে সর্বোচ্চ ৪ ধাপ |
| `tools=TOOLS` | মডেলকে টুলগুলোর তালিকা দেখানো |
| `message.tool_calls` | মডেল টুল চাইলে তথ্য থাকে; না চাইলে খালি |
| `if not message.tool_calls` | টুল নেই = চূড়ান্ত উত্তর |
| `messages.append(message)` | মডেলের উত্তর/টুল-অনুরোধ খাতায় রাখা |
| `call.function.name` | কোন টুল চাইছে |
| `json.loads(...)` | ইনপুটের লেখা → dict |
| `run_tool(name, args)` | আসল function চালানো |
| `"role": "tool"` | "এই ফলাফল তোমার ওই টুল-কলের উত্তর" |
| `"tool_call_id": call.id` | কোন কলের ফলাফল তা মেলানো |
| `answer or "..."` | উত্তর না এলে ব্যর্থতার বার্তা |
| `len(messages)` | মেমোরিতে কত মেসেজ জমেছে |

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

**খেয়াল করুন:** ২৫.৪°C সংখ্যাটা এসেছে Open-Meteo থেকে, আপনার কোড দিয়ে। মডেল শুধু সেটাকে বাংলায় সাজিয়ে দিয়েছে।

---

# পরীক্ষা — ৪টি প্রশ্ন

`02_agent_loop.py` চালিয়ে একে একে জিজ্ঞেস করুন:

| # | প্রশ্ন | প্রত্যাশা |
|---|---|---|
| 1 | আজ ঢাকার আবহাওয়া কেমন? | `get_weather` ডাকে |
| 2 | আগামীকাল চট্টগ্রামে বৃষ্টি হবে? | `get_forecast` ডাকে |
| 3 | Xyzzyville-এ আবহাওয়া কেমন? | "শহর পাওয়া যায়নি" — বানিয়ে বলে না |
| 4 | তুমি কে? | টুল ছাড়াই নিজের পরিচয় দেয় |

প্রতিটির পরে `mem` লিখে দেখুন মেসেজ কত বাড়ল।

> টুলের ইনপুট হুবহু মিলবে না সব সময়। মূল কথা: **সঠিক টুল, সঠিক শহর**।

---

## ভালো টুলের ৩টি নিয়ম

1. **ছোট ও একটি কাজ** — `get_weather_and_news` নয়; আলাদা টুল।
2. **পরিষ্কার নাম ও বর্ণনা** — মডেল বর্ণনা পড়েই টুল বাছে।
3. **ইনপুট বিশ্বাস করবেন না** — ভুল ইনপুটে error ফেরত দিন, যাতে মডেল ঠিক করতে পারে।

---

## সমস্যা হলে

| যা দেখছেন | সমাধান |
|---|---|
| `ModuleNotFoundError: httpx` | `.venv` চালু করুন, `pip install -r 00-setup/requirements.txt` |
| `401` / `404` | `.env`-এর key, base URL, model নাম দেখুন |
| `429` | ফ্রি মডেল ব্যস্ত — কিছুক্ষণ পরে চেষ্টা করুন |
| টুল ডাকেই না, বানিয়ে বলে | `prompts/system.md`-এর নিয়ম দেখুন; মডেল বদলে চেষ্টা করুন |
| "... শহর পাওয়া যায়নি" | ইংরেজি নাম দিন (Dhaka, Sylhet) |
| ইন্টারনেট নেই | `ConnectError` আসবে — সংযোগ ঠিক করে আবার চালান |

---

## শেষ চেকলিস্ট

- [ ] `01_test_tools.py` চালিয়ে ৩টি ফলাফল দেখেছেন
- [ ] `TOOLS` বর্ণনা আর আসল function-এর পার্থক্য বলতে পারেন
- [ ] `02_agent_loop.py` চালিয়ে `[ধাপ 1]` লগ দেখেছেন
- [ ] `mem` লিখে মেমোরির মেসেজ লিস্ট দেখেছেন
- [ ] বলতে পারেন — এক প্রশ্নের পরে ৫টি মেসেজ কেন হয়
- [ ] `tool_call_id` কেন লাগে বলতে পারেন
- [ ] ৪টি প্রশ্নের পরীক্ষা করেছেন

---

## পরের ধাপ

Phase 4 — **Memory Friend** (ফোল্ডার: [`03-memory-friend`](../03-memory-friend/README.md))।
এখন মেমোরি শুধু প্রোগ্রাম চলার সময় থাকে। পরের ফেজে প্রোগ্রাম বন্ধ করেও নাম-পছন্দ মনে রাখবে।
