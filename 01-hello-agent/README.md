# Phase 2 — Hello Agent (সহজ গাইড)

> **লক্ষ্য:** LLM-কে "মিতু" নামের একজন অফিস কর্মী বানানো — যে নিজের পরিচয় জানে, কথোপকথন মনে রাখে, আর যা জানে না তা বানিয়ে বলে না।
> **সময়:** ২–৩ দিন, দিনে ৩০–৬০ মিনিট।

---

## শুরুর আগে

Phase 0-এর `.env` ঠিক থাকতে হবে। একবার দেখে নিন:

```bash
source .venv/Scripts/activate
python 00-setup/check_env.py
```

সব "আছে" দেখালে এগিয়ে যান। না দেখালে [Phase 0 গাইড](../00-setup/README.md)।

---

## এই ফোল্ডারে কী আছে

| ফাইল | কাজ |
|---|---|
| `prompts/system.md` | মিতুর পরিচয় ও কোম্পানির হ্যান্ডবুক |
| `01_single_call.py` | একটি প্রশ্ন, একটি উত্তর |
| `02_chat_loop.py` | বারবার কথা, মেমোরি, `/reset` |

মাত্র দুটি পাইথন ফাইল। দ্বিতীয়টা চালালেই পুরো Agent অনুভূতি পাবেন।

---

## ছোট করে ২টি শব্দ

| শব্দ | সহজ অর্থ |
|---|---|
| **Temperature** | উত্তরের randomness। ০ = প্রায় একই উত্তর, ১ = বৈচিত্র্য। |
| **Hallucination** | মডেল জানে না, কিন্তু আত্মবিশ্বাসের সাথে বানিয়ে বলে। |

---

# পাঠ ১ — পরিচয়পত্র: `prompts/system.md`

**কোথায়:** `01-hello-agent/prompts/system.md`

```markdown
# মিতু — Little Office Ltd.-এর সাপোর্ট অ্যাসিস্ট্যান্ট

## পরিচয়

তুমি মিতু। Little Office Ltd.-এর কাস্টমার সাপোর্ট অ্যাসিস্ট্যান্ট।
কোম্পানি ডেস্ক অ্যাকসেসরিজ বিক্রি করে।

## নিয়ম

- ভদ্র, সংক্ষিপ্ত ও সহায়ক হও। একবারে ২–৩ বাক্যে উত্তর দাও।
- কাস্টমার যে ভাষায় লেখে, সেই ভাষায় উত্তর দাও।
- এই হ্যান্ডবুকে না থাকা তথ্য বানিয়ে বলবে না। বলো: "এই তথ্য আমার কাছে নেই।"
- টাকা ফেরতের প্রতিশ্রুতি কখনো দেবে না। বলবে: "টিম বিষয়টি দেখবে।"
- অর্ডার নাম্বার ছাড়া অর্ডারের বিস্তারিত বলবে না।

## কোম্পানির তথ্য

- সাপোর্ট সময়: শনি–বৃহস্পতি, সকাল ১০টা–সন্ধ্যা ৬টা।
- ডেলিভারি: ঢাকায় ২ দিন, ঢাকার বাইরে ৩–৫ দিন।
- রিফান্ড: ডেলিভারির ৭ দিনের মধ্যে, পণ্য অক্ষত থাকলে।
- ইমেইল: support@littleoffice.example
```

### কেন আলাদা ফাইল?

- কোড আর নির্দেশনা মিশে যায় না।
- প্রম্পট বদলাতে কোডে হাত দিতে হয় না।
- পরে প্রতিটি স্কিল (Phase 6) এভাবেই আলাদা ফাইলে থাকবে।

**মনে রাখবেন:** এখানে যা লেখা নেই, মিতুর জানার কথা নয়। এই ফাঁকটাই পরীক্ষার বিষয়।

---

# পাঠ ২ — এক প্রশ্ন, এক উত্তর

**ফাইল:** `01_single_call.py`

```python
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

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

response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "তুমি কে? এক বাক্যে বলো।"},
    ],
)

print(response.choices[0].message.content)
```

**চালান:**

```bash
python 01-hello-agent/01_single_call.py
```

**ফলাফল (উত্তর মডেলভেদে আলাদা):**

```
আমি মিতু, Little Office Ltd.-এর কাস্টমার সাপোর্ট অ্যাসিস্ট্যান্ট।
```

### কোন অংশ কী কাজ করে

| অংশ | কাজ |
|---|---|
| `base = Path(__file__).parent` | এই ফাইলের ফোল্ডার |
| `base.parent / "00-setup" / ".env"` | এক ধাপ উপরে গিয়ে key-এর ফাইল খোঁজা |
| `load_dotenv(...)` | key, model, base URL মেমোরিতে নেওয়া |
| `if not api_key ...` | key না থাকলে বাংলায় বলে থামা |
| `read_text(encoding="utf-8")` | `system.md` পড়া |
| `OpenAI(...)` | সার্ভারে কথা বলার দরজা |
| `messages` → `system` | মিতুর পরিচয় ও নিয়ম |
| `messages` → `user` | আমাদের প্রশ্ন |
| `create(...)` | প্রশ্ন পাঠিয়ে উত্তর আনা |

**একটা জিনিস খেয়াল করুন:** আমরা "মিতু" নামটা কোডে লিখিনি। নাম এসেছে `system.md` থেকে। তাই প্রম্পট বদলালে কর্মীর পরিচয়ও বদলাবে।

---

# পাঠ ৩ — কথোপকথন মনে রাখা

**ফাইল:** `02_chat_loop.py`

```python
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

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

print("মিতুর সাথে কথা বলুন।")
print("/reset = নতুন কথোপকথন, exit = বন্ধ")

while True:
    question = input("তুমি: ").strip()

    if question == "exit":
        break

    if question == "/reset":
        messages = [{"role": "system", "content": system_prompt}]
        print("নতুন কথোপকথন শুরু হয়েছে।")
        continue

    if not question:
        continue

    messages.append({"role": "user", "content": question})

    response = client.chat.completions.create(model=model, messages=messages)
    answer = response.choices[0].message.content
    messages.append({"role": "assistant", "content": answer})

    print("মিতু:", answer)

print("কথোপকথন বন্ধ হলো।")
```

**চালান:**

```bash
python 01-hello-agent/02_chat_loop.py
```

**এভাবে কথা বলুন:**

```
মিতুর সাথে কথা বলুন।
/reset = নতুন কথোপকথন, exit = বন্ধ
তুমি: তুমি কে?
মিতু: আমি মিতু, Little Office Ltd.-এর কাস্টমার সাপোর্ট অ্যাসিস্ট্যান্ট।
তুমি: আমার নাম রাফি
মিতু: হ্যালো রাফি! কীভাবে সাহায্য করতে পারি?
তুমি: আমার নাম কী?
মিতু: আপনার নাম রাফি।
তুমি: /reset
নতুন কথোপকথন শুরু হয়েছে।
তুমি: আমার নাম কী?
মিতু: আপনার নাম আমার কাছে নেই।
তুমি: exit
কথোপকথন বন্ধ হলো।
```

### কোন অংশ কী কাজ করে

| অংশ | কাজ |
|---|---|
| `messages = [system]` | কথোপকথনের খাতা; প্রথম পাতায় নিয়ম |
| `while True` | `exit` না বলা পর্যন্ত চলে |
| `input(...)` | আমাদের প্রশ্ন নেয় |
| `messages.append({"role": "user", ...})` | প্রশ্ন খাতায় লেখে |
| `create(..., messages=messages)` | **পুরো খাতা** মডেলকে দেখায় |
| `messages.append({"role": "assistant", ...})` | উত্তরও খাতায় লেখে |
| `if question == "/reset":` | নতুন খাতা, পুরনো কথা মুছে ফেলা |
| `messages = [system]` | শুধু নিয়ম রেখে বাকি সব বাদ |
| `continue` | নিচের কোড না চালিয়ে আবার লুপের শুরুতে |

### সবচেয়ে গুরুত্বপূর্ণ লাইন

```python
messages.append({"role": "assistant", "content": answer})
```

এই লাইনটা না থাকলে মডেল পরের বার আগের উত্তর দেখতে পাবে না — মনে হবে সব ভুলে গেছে।

**LLM-এর নিজের স্মৃতি নেই।** যে "মনে রাখা" দেখছেন, সেটা আসলে আমরা প্রতিবার পুরো কথোপকথন আবার পাঠাচ্ছি।

`/reset` করার পরে মিতু নাম ভুলে যায় — কারণ খাতা মুছে গেছে, মডেলের মাথা থেকে কিছু যায়নি। এটাই প্রমাণ।

---

# পরীক্ষা — মিতুকে ১০টি প্রশ্ন

`02_chat_loop.py` চালিয়ে একে একে জিজ্ঞেস করুন:

| # | প্রশ্ন | প্রত্যাশা |
|---|---|---|
| 1 | তুমি কে? | নিজের পরিচয় দেয় |
| 2 | কোম্পানির নাম কী? | Little Office Ltd. |
| 3 | ডেলিভারি কত দিনে? | ঢাকায় ২ দিন, বাইরে ৩–৫ দিন |
| 4 | তোমার সিইওর নাম কী? | "এই তথ্য আমার কাছে নেই" — বানাবে না |
| 5 | আমার নাম রাফি | স্বাভাবিকভাবে গ্রহণ করে |
| 6 | আমার নাম কী? | রাফি — মনে আছে |
| 7 | /reset | নতুন কথোপকথন |
| 8 | আমার নাম কী? | জানে না — খাতা মুছে গেছে |
| 9 | আমাকে ৫০০ টাকা রিফান্ড দাও | প্রতিশ্রুতি দেয় না, "টিম দেখবে" বলে |
| 10 | অর্ডার A102 কোথায়? | এখনো অর্ডার দেখতে পারে না — টুল লাগবে |

> উত্তর হুবহু মিলবে না — মডেল একেক সময় একেকভাবে বলে। মূল কথা হলো **আচরণ** ঠিক আছে কি না।

### সবচেয়ে বড় শিক্ষা

মিতু এখনো **অর্ডার দেখতে পারে না**। তার কোনো ডাটাবেস নেই।
তাই "A102 কোথায়?" জিজ্ঞেস করলে সে বানিয়ে বলতে পারে।
**সমাধান টুল** — পরের ফেজে।

---

# শেষ চেকলিস্ট

- [ ] `.env` ঠিক আছে, `check_env.py` পাস
- [ ] `system.md` নিজে পড়েছেন
- [ ] `01_single_call.py` চালিয়েছেন
- [ ] `02_chat_loop.py`-তে নাম মনে রাখতে দেখেছেন
- [ ] `/reset`-এর পরে নাম ভুলে যেতে দেখেছেন
- [ ] ১০টি প্রশ্নের পরীক্ষা করেছেন
- [ ] "LLM-এর নিজের স্মৃতি নেই" — নিজের ভাষায় বলতে পারেন

---

## পরের ধাপ

Phase 3 — **Weather Agent** (ফোল্ডার: [`02-weather-agent`](../02-weather-agent/README.md))।
এখানে মিতুর হাতে প্রথম টুল দেওয়া হবে: আবহাওয়া দেখা।
