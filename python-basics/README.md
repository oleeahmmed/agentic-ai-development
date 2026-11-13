# Phase 1 — Python বেসিক (সহজ গাইড)

> **লক্ষ্য:** Agent বানানোর জন্য যতটুকু Python দরকার, ঠিক ততটুকু।
> Django, machine learning, OOP-এর গভীর কথা — এখন লাগবে না।
> **সময়:** ২ সপ্তাহ, দিনে ৩০–৬০ মিনিট।

---

## কীভাবে পড়বেন

প্রতিটি পাঠে ৫টি ধাপ:

1. ফাইলটা খুলুন, কোডটা **নিজে হাতে লিখুন** (কপি-পেস্ট নয়)।
2. চালান।
3. আউটপুট মিলিয়ে দেখুন।
4. নিচের ব্যাখ্যা পড়ুন — কোন অংশ কী কাজ করে।
5. শেষের ছোট কাজটা করুন।

চালানোর নিয়ম (প্রথমে একবার venv চালু করুন):

```bash
source .venv/Scripts/activate
python python-basics/01_variables.py
```

শুধু ফাইলের নাম বদলাবেন — `02_...`, `03_...` ইত্যাদি।

---

## এই ফোল্ডারে কী আছে

| ফাইল | কী শেখাবে |
|---|---|
| `01_variables.py` | মান রাখা ও প্রিন্ট করা |
| `02_lists_dicts.py` | তালিকা ও কী-ভ্যালু (Agent-এ সবচেয়ে বেশি লাগে) |
| `03_conditions_loops.py` | শর্ত আর পুনরাবৃত্তি |
| `04_functions.py` | কাজের নাম দিয়ে ভাগ করা |
| `05_json_files.py` | ফাইলে ডেটা রাখা ও পড়া |
| `06_errors.py` | ভুল হলে থেমে না যাওয়া |
| `07_http.py` | ইন্টারনেট থেকে ডেটা আনা |
| `08_task_manager.py` | সব মিলিয়ে ছোট প্রজেক্ট |

---

# পাঠ ১ — ভেরিয়েবল

**ফাইল:** `python-basics/01_variables.py`

```python
name = "মিতু"
age = 25
city = "ঢাকা"

print("নাম:", name)
print("বয়স:", age)
print("শহর:", city)
print(f"{name}-এর বয়স {age} বছর, থাকে {city}-তে।")
```

**চালান:**

```bash
python python-basics/01_variables.py
```

**ফলাফল:**

```
নাম: মিতু
বয়স: 25
শহর: ঢাকা
মিতু-এর বয়স 25 বছর, থাকে ঢাকা-তে।
```

### কোন অংশ কী কাজ করে

| অংশ | কাজ |
|---|---|
| `name = "মিতু"` | `name` নামের বাক্সে "মিতু" রাখা |
| `age = 25` | সংখ্যা রাখা (কোটেশন নেই) |
| `"মিতু"` | লেখা/টেক্সট — string |
| `print(...)` | স্ক্রিনে দেখানো |
| `f"..."` | লেখার ভিতরে `{name}` বসিয়ে দেওয়া |

**ছোট কাজ:** `age` বদলে ৩০ করুন, আবার চালান।

---

# পাঠ ২ — list ও dict

**ফাইল:** `python-basics/02_lists_dicts.py`

> Agent-এ `messages` হলো list, আর `state`/টুলের ফলাফল প্রায়ই dict। তাই এই দুটো ভালো করে বুঝতে হবে।

```python
tasks = ["ইমেইল দেখা", "রিপোর্ট লেখা", "মিটিং"]

print("প্রথম কাজ:", tasks[0])
print("মোট কাজ:", len(tasks))

tasks.append("কাস্টমারকে উত্তর দেওয়া")
print("এখন কাজ:", tasks)

customer = {
    "name": "রাফি",
    "city": "চট্টগ্রাম",
    "orders": 3,
}

print("কাস্টমার:", customer["name"])
print("ফোন:", customer.get("phone", "নেই"))
```

**ফলাফল:**

```
প্রথম কাজ: ইমেইল দেখা
মোট কাজ: 3
এখন কাজ: ['ইমেইল দেখা', 'রিপোর্ট লেখা', 'মিটিং', 'কাস্টমারকে উত্তর দেওয়া']
কাস্টমার: রাফি
ফোন: নেই
```

### কোন অংশ কী কাজ করে

| অংশ | কাজ |
|---|---|
| `["...", "..."]` | list — ক্রমে সাজানো তালিকা |
| `tasks[0]` | প্রথম জিনিস (গণনা ০ থেকে শুরু) |
| `len(tasks)` | কতগুলো আছে |
| `tasks.append(...)` | শেষে নতুন জিনিস যোগ |
| `{ "name": "রাফি" }` | dict — নাম দিয়ে খোঁজা যায় |
| `customer["name"]` | "name" কী-এর মান |
| `.get("phone", "নেই")` | না থাকলে "নেই" — error হবে না |

**ছোট কাজ:** নিজের ৩টি কাজের list বানান; একটা `remove()` করুন; `len()` দিয়ে দেখুন।

---

# পাঠ ৩ — if ও for

**ফাইল:** `python-basics/03_conditions_loops.py`

```python
tasks = ["ইমেইল দেখা", "রিপোর্ট লেখা", "মিটিং"]

for task in tasks:
    print("কাজ:", task)

temperature = 32

if temperature > 30:
    print("আজ গরম")
else:
    print("আজ ঠান্ডা")

for number in range(1, 4):
    print("সংখ্যা:", number)
```

**ফলাফল:**

```
কাজ: ইমেইল দেখা
কাজ: রিপোর্ট লেখা
কাজ: মিটিং
আজ গরম
সংখ্যা: 1
সংখ্যা: 2
সংখ্যা: 3
```

### কোন অংশ কী কাজ করে

| অংশ | কাজ |
|---|---|
| `for task in tasks:` | তালিকার প্রতিটি জিনিস নিয়ে একবার করে ঘোরা |
| `if ...:` | শর্ত সত্য হলে ভিতরের কাজ |
| `else:` | শর্ত মিথ্যা হলে |
| `temperature > 30` | তুলনা — সত্য (`True`) বা মিথ্যা (`False`) |
| `range(1, 4)` | ১, ২, ৩ (৪ আসে না) |
| ভিতরের ৪টি ফাঁকা জায়গা | Python-এ এই ফাঁকা জায়গা (indent) বাধ্যতামূলক |

**ছোট কাজ:** `range(1, 6)` করে ১ থেকে ৫ প্রিন্ট করুন।

---

# পাঠ ৪ — function

**ফাইল:** `python-basics/04_functions.py`

```python
def greet(name):
    return f"হ্যালো {name}"

def add(a, b):
    return a + b

def is_hot(temperature):
    return temperature > 30

print(greet("মিতু"))
print(add(2, 3))
print("গরম?", is_hot(32))
```

**ফলাফল:**

```
হ্যালো মিতু
5
গরম? True
```

### কোন অংশ কী কাজ করে

| অংশ | কাজ |
|---|---|
| `def greet(name):` | `greet` নামে কাজ বানানো; `name` হলো ইনপুট |
| `return` | ফলাফল ফেরত দেওয়া |
| `greet("মিতু")` | কাজটা চালানো |
| `add(2, 3)` | দুই ইনপুট নিয়ে যোগ |
| `is_hot(32)` | সত্য/মিথ্যা ফেরত দেয় |

**print বনাম return:** `print` শুধু দেখায়; `return` ফলাফল ফেরত দেয়, যাতে অন্য জায়গায় ব্যবহার করা যায়। Agent-এর টুলে `return` লাগবে।

**ছোট কাজ:** `multiply(a, b)` নামে একটি function বানান।

---

# পাঠ ৫ — JSON ফাইল

**ফাইল:** `python-basics/05_json_files.py`

> JSON হলো ডেটা রাখার সাধারণ ফরম্যাট। LLM-এর `messages`, Agent-এর `state`, টুলের ফলাফল — সবই প্রায় এই আকারের।

```python
import json
from pathlib import Path

file = Path(__file__).parent / "customer.json"

customer = {
    "name": "রাফি",
    "city": "চট্টগ্রাম",
    "orders": 3,
}

text = json.dumps(customer, ensure_ascii=False, indent=2)
file.write_text(text, encoding="utf-8")

text = file.read_text(encoding="utf-8")
data = json.loads(text)

print(data)
print("নাম:", data["name"])
```

**ফলাফল:**

```
{'name': 'রাফি', 'city': 'চট্টগ্রাম', 'orders': 3}
নাম: রাফি
```

একই ফোল্ডারে `customer.json` ফাইল তৈরি হবে। খুলে দেখুন।

### কোন অংশ কী কাজ করে

| অংশ | কাজ |
|---|---|
| `import json` | JSON পড়া/লেখার টুল |
| `Path(__file__).parent` | এই পাইথন ফাইলের ফোল্ডার |
| `json.dumps(...)` | dict → লেখা (JSON) |
| `ensure_ascii=False` | বাংলা অক্ষর ঠিক রাখা |
| `file.write_text(...)` | ফাইলে লেখা |
| `file.read_text(...)` | ফাইল পড়া |
| `json.loads(...)` | লেখা → dict |

**ছোট কাজ:** `customer`-এ নিজের নাম আর শহর বসিয়ে আবার চালান; `customer.json` খুলে দেখুন।

---

# পাঠ ৬ — try/except

**ফাইল:** `python-basics/06_errors.py`

```python
try:
    number = int("আমি সংখ্যা নই")
    print(number)
except ValueError:
    print("এটা সংখ্যা নয়।")

customer = {"name": "রাফি"}

print(customer.get("phone", "ফোন নম্বর নেই"))
```

**ফলাফল:**

```
এটা সংখ্যা নয়।
ফোন নম্বর নেই
```

### কোন অংশ কী কাজ করে

| অংশ | কাজ |
|---|---|
| `try:` | "এটা চেষ্টা করো" |
| `except ValueError:` | নির্দিষ্ট ভুল হলে এখানে আসো |
| `int("...")` | লেখাকে সংখ্যায় বদলায়; না পারলে `ValueError` |
| `.get("phone", "...")` | কী না থাকলে error নয়, বিকল্প দেয় |

**কেন দরকার:** Agent-এর টুল ভুল ইনপুট পেলেও এজেন্ট যেন থেমে না যায়, বরং মডেলকে বোঝায় "এটা হয়নি, অন্যভাবে চেষ্টা করো"।

**ছোট কাজ:** `customer["phone"]` দিয়ে সরাসরি খোঁজার চেষ্টা করুন — কী error হয় দেখুন।

---

# পাঠ ৭ — ইন্টারনেট থেকে ডেটা

**ফাইল:** `python-basics/07_http.py`

> এখানেই প্রথম বাইরের জগতের সাথে কথা। Phase 3-এ এটাই টুল হবে।

```python
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
```

**ফলাফল (তাপমাত্রা বদলাবে):**

```
HTTP status: 200
ঢাকার তাপমাত্রা: 22.2 °C
```

ইন্টারনেট না থাকলে error আসবে — তখন পরের পাঠে যান, পরে আবার চেষ্টা করুন।

### কোন অংশ কী কাজ করে

| অংশ | কাজ |
|---|---|
| `httpx.get(url, ...)` | ওয়েবসাইটে অনুরোধ পাঠানো |
| `params` | লিংকের সাথে যুক্ত প্রশ্নের মান (অক্ষাংশ/দ্রাঘিমাংশ) |
| `status_code` | 200 = ঠিক আছে, 404 = নেই, 500 = সার্ভারে সমস্যা |
| `response.json()` | আসা উত্তরকে dict-এ বদলানো |
| `data["current"]["temperature_2m"]` | ভিতরের নির্দিষ্ট মান |
| `trust_env=False` | কম্পিউটারের ভাঙা proxy সেটিং এড়িয়ে সরাসরি কল |

**ছোট কাজ:** চট্টগ্রামের জন্য `latitude=22.35`, `longitude=91.78` বসিয়ে চালান।

---

# পাঠ ৮ — মিনি প্রজেক্ট: Task Manager

**ফাইল:** `python-basics/08_task_manager.py`

এতদিনের সব একসাথে — list, dict, loop, input, file, JSON।

```python
import json
from pathlib import Path

file = Path(__file__).parent / "tasks.json"

if file.exists():
    tasks = json.loads(file.read_text(encoding="utf-8"))
else:
    tasks = []

while True:
    command = input("কমান্ড (add / list / exit): ").strip()

    if command == "add":
        task = input("নতুন কাজ: ").strip()
        if task:
            tasks.append(task)
            text = json.dumps(tasks, ensure_ascii=False, indent=2)
            file.write_text(text, encoding="utf-8")
            print("সেভ হয়েছে।")
        else:
            print("খালি কাজ সেভ হবে না।")

    elif command == "list":
        if tasks:
            for number, task in enumerate(tasks, start=1):
                print(number, "-", task)
        else:
            print("কোনো কাজ নেই।")

    elif command == "exit":
        break

    else:
        print("add, list বা exit লিখুন।")
```

**চালান:**

```bash
python python-basics/08_task_manager.py
```

**এভাবে ব্যবহার করুন:**

```
কমান্ড (add / list / exit): add
নতুন কাজ: কাস্টমারকে ইমেইল
সেভ হয়েছে।
কমান্ড (add / list / exit): list
1 - কাস্টমারকে ইমেইল
কমান্ড (add / list / exit): exit
```

আবার চালালে আগের কাজগুলো থাকবে — কারণ `tasks.json`-এ সেভ হয়েছে।

### কোন অংশ কী কাজ করে

| অংশ | কাজ |
|---|---|
| `if file.exists()` | আগের সেভ আছে কি না |
| `while True:` | যতক্ষণ `break` না হয়, ঘুরতে থাকে |
| `input(...)` | ইউজারের কাছ থেকে লেখা নেয় |
| `.strip()` | দুই পাশের ফাঁকা জায়গা মুছে দেয় |
| `enumerate(..., start=1)` | ১, ২, ৩ নম্বরসহ দেখায় |
| `break` | লুপ থামায় |
| `file.write_text(...)` | প্রতিবার সেভ করে |

এটাই একটি ছোট Agent-এর কাঠামো: **ইনপুট নাও → সিদ্ধান্ত নাও → কাজ করো → সেভ করো → আবার**।

---

## ৫টি অনুশীলন

1. `02`-এ নিজের ৩টি কাজের list বানান, একটা `remove()` করুন।
2. `03`-এ `range` দিয়ে ১ থেকে ৫ প্রিন্ট করুন।
3. `04`-এ `multiply(a, b)` function বানান।
4. `05`-এ নিজের নাম-শহর JSON-এ সেভ করে আবার পড়ুন।
5. `08`-এ `count` কমান্ড যোগ করুন — মোট কত কাজ আছে দেখাবে।

---

## শেষ চেকলিস্ট

- [ ] ৮টি ফাইল নিজে লিখেছেন (কপি নয়)
- [ ] ৮টিই চালিয়েছেন
- [ ] list আর dict-এর পার্থক্য বলতে পারেন
- [ ] `return` আর `print`-এর পার্থক্য বলতে পারেন
- [ ] JSON ফাইলে লিখে আবার পড়তে পারেন
- [ ] `try/except` কেন লাগে বলতে পারেন
- [ ] একটা API থেকে ডেটা এনেছেন
- [ ] Task Manager-এ কাজ যোগ করে আবার চালিয়ে দেখেছেন

---

## পরের ধাপ

Phase 2 — **Hello Agent** (ফোল্ডার: [`01-hello-agent`](../01-hello-agent/README.md))।
এখানে Python আর LLM জোড়া লাগবে: পার্সোনা, কথোপকথন মনে রাখা, `/reset`।

> Phase 0-এর `.env` এখনো বাকি। Phase 2-এ যাওয়ার আগে key বসিয়ে `hello_llm.py` একবার চালিয়ে নিন — [গাইড](../00-setup/README.md)।
