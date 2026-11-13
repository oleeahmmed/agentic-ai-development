# Phase 0 — একদম শুরু (সহজ গাইড)

> **লক্ষ্য:** কম্পিউটার থেকে LLM-কে একটা প্রশ্ন করা, আর তার উত্তর দেখা।
> **সময়:** ২০–৩০ মিনিট।

---

## এই ফোল্ডারে কী আছে

| ফাইল | কাজ |
|---|---|
| `check_env.py` | সব ঠিক আছে কি না দেখে |
| `hello_llm.py` | LLM-কে প্রথম প্রশ্ন করে |
| `.env.example` | সেটিংসের নমুনা |
| `requirements.txt` | যে ৩টি প্যাকেজ লাগবে |

আর এই `README.md` — যেটা আপনি এখন পড়ছেন।

---

## ধাপ ১ — টার্মিনাল খুলুন

Git Bash খুলুন। তারপর প্রজেক্ট ফোল্ডারে যান:

```bash
cd ~/Desktop/ai-agent
```

---

## ধাপ ২ — Python আছে কি না দেখুন

```bash
python --version
```

`Python 3.11` বা তার চেয়ে বড় হলেই চলবে।
(এখন আছে `Python 3.14.10`।)

---

## ধাপ ৩ — আলাদা বাক্স বানান (একবারই)

```bash
python -m venv .venv
source .venv/Scripts/activate
```

ভালো করে দেখুন — প্রম্পটের আগে `(.venv)` এসেছে কি না:

```
(.venv) olee@PC MINGW64 ~/Desktop/ai-agent
```

এলে বুঝবেন ভিতরে আছেন। নতুন টার্মিনাল খুললে আবার `source` লাইনটা চালাতে হবে।

> **কেন?** `.venv` হলো আলাদা বাক্স। এখানে প্যাকেজ রাখলে আপনার অন্য প্রজেক্ট নষ্ট হবে না।

---

## ধাপ ৪ — প্যাকেজ ইনস্টল

```bash
pip install -r 00-setup/requirements.txt
```

তিনটি প্যাকেজ আসবে:

| প্যাকেজ | কাজ |
|---|---|
| `openai` | LLM-এর সাথে কথা বলা |
| `python-dotenv` | `.env` ফাইল পড়া |
| `httpx` | ইন্টারনেটে অনুরোধ পাঠানো (পরে লাগবে) |

---

## ধাপ ৫ — API key নিন

সবচেয়ে সহজ: **OpenRouter**

1. https://openrouter.ai খুলুন
2. Sign up করুন
3. Credits-এ অল্প টাকা ঢালুন (৫ ডলার অনেকদিন চলবে)
4. Keys → Create Key
5. `sk-or-v1-...` দিয়ে শুরু হওয়া key কপি করুন

> key হলো আপনার টাকার চাবি। কাউকে দেবেন না, screenshot নেবেন না, git-এ দেবেন না।

---

## ধাপ ৬ — `.env` ফাইল বানান

```bash
cp 00-setup/.env.example 00-setup/.env
code 00-setup/.env
```

ফাইলটা খুলে ঠিক এই তিনটি লাইন রাখুন (বাকিগুলো `#` দিয়ে শুরু, ওগুলো দরকার নেই):

```env
LLM_API_KEY=sk-or-v1-আপনার-আসল-কি
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=openai/gpt-4.1-mini
```

| লাইন | কাজ |
|---|---|
| `LLM_API_KEY` | আপনার পরিচয়পত্র |
| `LLM_BASE_URL` | কোন সার্ভারে যাবে |
| `LLM_MODEL` | কোন মডেল উত্তর দেবে |

> `.env` ফাইলের নাম যেন ঠিক `.env` হয়। Notepad-এ সেভ করলে `.env.txt` হয়ে যেতে পারে — "All files" বেছে সেভ করুন।

---

## ধাপ ৭ — প্রথম ফাইল: `check_env.py`

**কোথায়:** `00-setup/check_env.py`

**পুরো কোড:**

```python
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")

env_file = Path(__file__).parent / ".env"
load_dotenv(env_file)

print("Python:", sys.version.split()[0])
print(".env ফাইল:", "আছে" if env_file.exists() else "নেই")
print("LLM_API_KEY:", "আছে" if os.getenv("LLM_API_KEY") else "নেই")
print("LLM_BASE_URL:", os.getenv("LLM_BASE_URL", "নেই"))
print("LLM_MODEL:", os.getenv("LLM_MODEL", "নেই"))
print()

if os.getenv("LLM_API_KEY") and os.getenv("LLM_MODEL"):
    print("সব ঠিক আছে। এখন চালান: python 00-setup/hello_llm.py")
else:
    print("আগে 00-setup/.env ঠিক করুন।")
```

**চালান:**

```bash
python 00-setup/check_env.py
```

**যা দেখাবে (key বসানোর পরে):**

```
Python: 3.14.10
.env ফাইল: আছে
LLM_API_KEY: আছে
LLM_BASE_URL: https://openrouter.ai/api/v1
LLM_MODEL: openai/gpt-4.1-mini

সব ঠিক আছে। এখন চালান: python 00-setup/hello_llm.py
```

### কোন অংশ কী কাজ করে

| অংশ | কাজ |
|---|---|
| `import os, sys` | Python-এর সাধারণ টুল আনা |
| `from pathlib import Path` | ফাইলের ঠিকানা হ্যান্ডেল করা |
| `from dotenv import load_dotenv` | `.env` পড়ার টুল |
| `sys.stdout.reconfigure(...)` | Windows-এ বাংলা ঠিক দেখানো |
| `Path(__file__).parent / ".env"` | এই ফাইলের পাশে `.env` খোঁজা |
| `load_dotenv(env_file)` | `.env`-এর মানগুলো মেমোরিতে রাখা |
| `sys.version.split()[0]` | Python-এর ভার্সন |
| `env_file.exists()` | ফাইলটা সত্যিই আছে কি না |
| `os.getenv("LLM_API_KEY")` | key-টা পড়া |
| `os.getenv("LLM_BASE_URL", "নেই")` | না থাকলে "নেই" দেখানো |
| শেষ `if` | key আর model থাকলে পরের ধাপের কথা বলা |

---

## ধাপ ৮ — দ্বিতীয় ফাইল: `hello_llm.py`

**কোথায়:** `00-setup/hello_llm.py`

**পুরো কোড:**

```python
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

sys.stdout.reconfigure(encoding="utf-8")

env_file = Path(__file__).parent / ".env"
load_dotenv(env_file)

api_key = os.getenv("LLM_API_KEY")
model = os.getenv("LLM_MODEL")
base_url = os.getenv("LLM_BASE_URL")

if not api_key or not model:
    print("00-setup/.env ফাইলে LLM_API_KEY আর LLM_MODEL দিন।")
    sys.exit()

client = OpenAI(api_key=api_key, base_url=base_url)

response = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "system",
            "content": "তুমি Little Office Ltd.-এর সহায়ক। সংক্ষেপে বাংলায় উত্তর দাও।",
        },
        {
            "role": "user",
            "content": "তুমি কে?",
        },
    ],
)

print(response.choices[0].message.content)
```

**চালান:**

```bash
python 00-setup/hello_llm.py
```

**যা দেখাবে (উত্তর মডেলভেদে আলাদা):**

```
আমি Little Office Ltd.-এর সহায়ক অফিস অ্যাসিস্ট্যান্ট। আপনার কী সাহায্য করতে পারি?
```

### কোন অংশ কী কাজ করে

| অংশ | কাজ |
|---|---|
| `api_key`, `model`, `base_url` | `.env` থেকে তিনটি সেটিং পড়া |
| `if not api_key ...` | key/model না থাকলে সাথে সাথে থামা |
| `OpenAI(...)` | সার্ভারে কথা বলার দরজা তৈরি |
| `messages` → `system` | কর্মীর নিয়মপত্র ("তুমি কে, কীভাবে কথা বলবে") |
| `messages` → `user` | আজকের প্রশ্ন ("তুমি কে?") |
| `create(...)` | প্রশ্ন পাঠিয়ে উত্তর আনা |
| `choices[0].message.content` | আসল উত্তর |

### system আর user আলাদা কেন?

- `system` = অফিসের নিয়ম। প্রতিবার একই থাকে।
- `user` = আজকের কাজ। প্রতিবার বদলায়।

নিয়ম আলাদা রাখলে পরে শুধু প্রশ্ন বদলালেই হবে — নিয়ম আবার লিখতে হবে না।

### এই ফাইলের সবচেয়ে বড় শিক্ষা

Little Office Ltd. আসলে নেই। মডেল তা জানে না, কিন্তু ভদ্রভাবে উত্তর দিয়ে দিল।
**LLM যা জানে না, তা বানিয়ে বলতে পারে।** এটাই "hallucination"।
এর সমাধান টুল — শিখবেন Phase 3-এ।

---

## ধাপ ৯ — নিজে আবার বানান

এই README না দেখে চেষ্টা করুন:

1. `practice` নামে নতুন ফোল্ডার বানান।
2. নতুন `.venv`, একই ৩টি প্যাকেজ।
3. `.env` বানান।
4. `my_call.py` লিখুন — শুধু এই ৫টি কাজ:
   - key পড়া
   - client বানানো
   - system + user message
   - উত্তর নেওয়া
   - প্রিন্ট করা
5. চালান। কোথায় আটকালেন, নোটে লিখুন।

**ছোট পরীক্ষা:** প্রশ্ন বদলে করুন — `"Little Office Ltd.-এর আজকের স্টক কত?"`
মডেল কী বলে দেখুন। বানিয়ে বলে কি না খেয়াল করুন।

---

## সমস্যা হলে

| যা দেখছেন | সমাধান |
|---|---|
| `ModuleNotFoundError` | `.venv` চালু করুন, তারপর `pip install -r 00-setup/requirements.txt` |
| `401` | key ভুল — `.env` ঠিক করুন, নতুন key নিন |
| `402` | ফ্রি অ্যাকাউন্টে টাকার মডেল চলবে না — `:free` মডেল ব্যবহার করুন |
| `429` | ফ্রি মডেল ব্যস্ত/লিমিটে — কিছুক্ষণ পরে বা অন্য `:free` মডেল চেষ্টা করুন |
| `404 model not found` | `LLM_MODEL` বা `LLM_BASE_URL` মেলেনি |
| `.env` পাওয়া যাচ্ছে না | ফাইল `00-setup/.env`-এ আছে কি? নাম `.env.txt` হয়ে গেছে কি? |
| বাংলা অক্ষর এলোমেলো | Git Bash বা Windows Terminal ব্যবহার করুন |

---

## শেষ চেকলিস্ট

- [ ] `python --version` কাজ করছে
- [ ] `.venv` চালু হয়েছে
- [ ] ৩টি প্যাকেজ ইনস্টল
- [ ] `.env`-এ আসল key আছে
- [ ] `check_env.py` সব "আছে" দেখাচ্ছে
- [ ] `hello_llm.py` উত্তর দেখাচ্ছে
- [ ] `.env` git-এ যাবে না (`.gitignore`-এ আছে)
- [ ] README না দেখে নিজে লিখেছেন

---

## পরের ধাপ

Phase 1 — Python বেসিক।
শুধু যতটুকু Agent বানাতে লাগে: list, dict, function, JSON, try/except।
[সিলেবাস দেখুন](../ai-agent-syllabus-bangla.md)
