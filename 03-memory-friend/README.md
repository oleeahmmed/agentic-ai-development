# Phase 4 — Memory Friend (সহজ গাইড)

> **লক্ষ্য:** এমন এজেন্ট, যে আপনার নাম-পছন্দ মনে রাখে — প্রোগ্রাম বন্ধ করলেও ভোলে না।
> **সময়:** ১–২ সপ্তাহ, দিনে ৩০–৬০ মিনিট।

---

## শুরুর আগে

Phase 0-এর `.env` ঠিক থাকতে হবে। একবার দেখে নিন:

```bash
source .venv/Scripts/activate
python 00-setup/check_env.py
```

---

## গল্প: কালকের কথা আজও

Phase 2-এ মিতু কথোপকথন মনে রাখত — কিন্তু শুধু প্রোগ্রাম চালু থাকা পর্যন্ত। বন্ধ করলে সব ভুলে যেত।

কারণ সেই "স্মৃতি" ছিল শুধু একটা `messages` লিস্ট, কম্পিউটারের মেমোরিতে। প্রোগ্রাম শেষ = লিস্ট শেষ।

এখন মিতু যা শেখে, সেটা **ফাইলে** লিখে রাখব। প্রোগ্রাম বন্ধ, কম্পিউটার বন্ধ — তবু থাকবে।

---

## দুই ধরনের স্মৃতি

| ধরন | কোথায় থাকে | কতদিন থাকে |
|---|---|---|
| **Short-term** | `messages` লিস্ট | প্রোগ্রাম বন্ধ হলে মুছে যায় |
| **Long-term** | `03-memory-friend/memories.json` ফাইল | যতদিন ফাইলটা রাখেন |

এই দুইটা একসাথে চলে:

- কথোপকথনের ধারা → short-term
- নাম, শহর, পছন্দ → long-term

`/reset` দিলে short-term মুছে যায়, কিন্তু long-term থাকে। এটাই পার্থক্য বোঝার সবচেয়ে সহজ পরীক্ষা।

---

## এই ফোল্ডারে কী আছে

| ফাইল | কাজ |
|---|---|
| `memory.py` | স্মৃতি সেভ, পড়া, মুছে ফেলা |
| `01_memory_test.py` | LLM ছাড়া স্মৃতি পরীক্ষা |
| `02_memory_agent.py` | চ্যাট + স্মৃতি |
| `prompts/system.md` | মিতুর স্মৃতি-নিয়ম |
| `memories.json` | আসল স্মৃতি — **প্রথম save-এ নিজে তৈরি হবে**, git-এ যাবে না |

---

# পাঠ ১ — `memory.py`

**কোথায়:** `03-memory-friend/memory.py`

```python
import json
from pathlib import Path

FILE = Path(__file__).parent / "memories.json"


def load_all():
    if not FILE.exists():
        return {}

    return json.loads(FILE.read_text(encoding="utf-8"))


def save_all(data):
    text = json.dumps(data, ensure_ascii=False, indent=2)
    FILE.write_text(text, encoding="utf-8")


def get_memory(user_id):
    return load_all().get(user_id, {})


def save_memory(user_id, key, value):
    key = key.strip()
    value = value.strip()

    if not key or not value:
        return "key আর value দুটোই দরকার।"

    data = load_all()
    data.setdefault(user_id, {})[key] = value
    save_all(data)

    return f"মনে রাখলাম: {key} = {value}"


def forget_all(user_id):
    data = load_all()
    data[user_id] = {}
    save_all(data)

    return "সব স্মৃতি মুছে ফেলা হয়েছে।"
```

এই ফাইলে LLM নেই। এটা শুধু **স্মৃতির আলমারি**।

### ফাইলের আকার

`memories.json` দেখতে এমন:

```json
{
  "rafi": {
    "নাম": "রাফি",
    "প্রিয় শহর": "ঢাকা"
  },
  "karim": {
    "নাম": "করিম"
  }
}
```

বাইরের চাবি = `user_id`। ভিতরের চাবি = তথ্যের নাম। তাই দুইজনের স্মৃতি মিশে যায় না।

### `memories.json` কোথায়?

ফাইলটা `memory.py`-এর পাশেই তৈরি হয়:

```
03-memory-friend/memories.json
```

আপনার কম্পিউটারে পুরো ঠিকানা:

```
C:\Users\olee\Desktop\ai-agent\03-memory-friend\memories.json
```

তিনটি জিনিস খেয়াল রাখুন:

- **শুরুতে ফাইলটা থাকেই না।** প্রথমবার `save_memory` চললে (এজেন্টে কিছু বললে বা `01_memory_test.py` চালালে) ফাইলটা নিজে তৈরি হয়।
- এজেন্ট চালিয়ে শুধু `User id` লিখলে এখনো ফাইল তৈরি হয়নি — তখন খুঁজে পাবেন না।
- `01_memory_test.py` একবার চালালেই ফাইলটা দেখা যাবে — এতে LLM লাগে না।

দেখার উপায়:

```bash
ls 03-memory-friend/
cat 03-memory-friend/memories.json
```

VS Code-এ খুলতে: `code 03-memory-friend/memories.json`

### কোন অংশ কী কাজ করে

| অংশ | কাজ |
|---|---|
| `FILE` | `03-memory-friend/memories.json`-এর ঠিকানা |
| `load_all()` | পুরো ফাইল পড়া; ফাইল না থাকলে `{}` |
| `save_all(data)` | পুরো ফাইল লেখা |
| `ensure_ascii=False` | বাংলা অক্ষর ঠিক রাখা |
| `get_memory(user_id)` | একজন মানুষের তথ্য |
| `save_memory(user_id, key, value)` | নতুন তথ্য রাখা |
| `data.setdefault(user_id, {})` | নতুন মানুষ হলে তার খাতা বানানো |
| `[key] = value` | একই `key` থাকলে **পুরনোটা বদলে যায়** |
| `forget_all(user_id)` | শুধু ওই মানুষের স্মৃতি খালি করা |

> **override কী?** আগে সেভ ছিল `শহর: চট্টগ্রাম`। এখন `শহর: ঢাকা` সেভ করলে পুরনোটা মুছে নতুনটা বসে। আলাদা কিছু করতে হয় না — dict-এ একই চাবিতে লিখলেই হয়।

---

# পাঠ ২ — স্মৃতি পরীক্ষা: `01_memory_test.py`

LLM ছাড়া আগে স্মৃতি ঠিক আছে কি না দেখুন।

**ফাইল:** `01_memory_test.py`

```python
import sys

import memory

sys.stdout.reconfigure(encoding="utf-8")

user = "test"

print("১. সেভ")
print(memory.save_memory(user, "নাম", "রাফি"))
print(memory.save_memory(user, "শহর", "চট্টগ্রাম"))
print()

print("২. আবার পড়া")
print(memory.get_memory(user))
print()

print("৩. পুরনো পছন্দ বদলানো")
print(memory.save_memory(user, "শহর", "ঢাকা"))
print(memory.get_memory(user))
print()

print("৪. ভুলে যাওয়া")
print(memory.forget_all(user))
print(memory.get_memory(user))
print()

print("৫. ফাইলে যা আছে")
print(memory.FILE.read_text(encoding="utf-8"))
```

**চালান:**

```bash
python 03-memory-friend/01_memory_test.py
```

**ফলাফল:**

```
১. সেভ
মনে রাখলাম: নাম = রাফি
মনে রাখলাম: শহর = চট্টগ্রাম

২. আবার পড়া
{'নাম': 'রাফি', 'শহর': 'চট্টগ্রাম'}

৩. পুরনো পছন্দ বদলানো
মনে রাখলাম: শহর = ঢাকা
{'নাম': 'রাফি', 'শহর': 'ঢাকা'}

৪. ভুলে যাওয়া
সব স্মৃতি মুছে ফেলা হয়েছে।
{}

৫. ফাইলে যা আছে
{
  "test": {}
}
```

### কোন অংশ কী কাজ করে

| অংশ | কাজ |
|---|---|
| `import memory` | পাশের `memory.py` আনা |
| `user = "test"` | পরীক্ষার জন্য আলাদা মানুষ |
| `save_memory(...)` | তথ্য রাখা |
| `get_memory(...)` | তথ্য পড়া |
| `forget_all(...)` | সব মুছা |
| `memory.FILE.read_text(...)` | ফাইলটা নিজের চোখে দেখা |

ফাইলটা খুলে দেখুন — সেভ করার সাথে সাথে বদলায়।

---

# পাঠ ৩ — `prompts/system.md`

**কোথায়:** `03-memory-friend/prompts/system.md`

```markdown
# মিতু — মনে রাখা সহকারী

তুমি মিতু, Little Office Ltd.-এর ব্যক্তিগত সহকারী।

## নিয়ম

- ব্যবহারকারী নিজের সম্পর্কে কিছু জানালে `save_memory` দিয়ে মনে রাখো।
- স্থায়ী তথ্য মনে রাখো: নাম, শহর, পছন্দ, লক্ষ্য, গুরুত্বপূর্ণ তারিখ।
- একবারের সাময়িক কথা মনে রাখো না।
- নতুন পছন্দ পুরনোটার উপর লিখে দাও।
- "যা মনে আছে" অংশে যা নেই, তা জানো না বলে স্বীকার করো।
- সংক্ষেপে বাংলায় উত্তর দাও।
```

**"স্থায়ী তথ্য"** শব্দটা গুরুত্বপূর্ণ। "আজ বৃষ্টি হচ্ছে" — এটা মনে রাখার দরকার নেই। "আমার প্রিয় খাবার বিরিয়ানি" — এটা রাখার মতো।

সব জিনিস সেভ করলে ফাইল আবর্জনায় ভরে যাবে, আর ভুল তথ্য উত্তর নষ্ট করবে। একে বলে **memory policy**।

---

# পাঠ ৪ — agent: `02_memory_agent.py`

**ফাইল:** `02_memory_agent.py`

```python
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

import memory

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

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "save_memory",
            "description": "ব্যবহারকারী সম্পর্কে স্থায়ী তথ্য মনে রাখে।",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "যেমন নাম, শহর, প্রিয় খাবার"},
                    "value": {"type": "string", "description": "মনে রাখার মান"},
                },
                "required": ["key", "value"],
            },
        },
    },
]


def start_messages(user_id):
    facts = memory.get_memory(user_id)

    if facts:
        lines = [f"- {key}: {value}" for key, value in facts.items()]
        facts_text = "\n".join(lines)
    else:
        facts_text = "এখনো কিছু জানা নেই।"

    content = system_prompt + "\n\n## যা মনে আছে\n\n" + facts_text

    return [{"role": "system", "content": content}]


def show_memory(user_id):
    facts = memory.get_memory(user_id)

    if not facts:
        print("এখনো কিছু মনে নেই।")
        return

    for key, value in facts.items():
        print(f"- {key}: {value}")


user_id = input("User id (Enter = rafi): ").strip() or "rafi"
messages = start_messages(user_id)

print(f"মিতুর সাথে কথা বলুন ({user_id})।")
print("/memory = স্মৃতি দেখা, /forget = মুছে ফেলা, /reset = কথোপকথন নতুন, exit = বন্ধ")

while True:
    question = input("তুমি: ").strip()

    if question == "exit":
        break

    if question == "/memory":
        show_memory(user_id)
        continue

    if question == "/forget":
        print(memory.forget_all(user_id))
        messages = start_messages(user_id)
        continue

    if question == "/reset":
        messages = start_messages(user_id)
        print("কথোপকথন রিসেট হলো। স্মৃতি ঠিক আছে।")
        continue

    if not question:
        continue

    messages[0] = start_messages(user_id)[0]
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
            print("মিতু:", message.content)
            break

        for call in message.tool_calls:
            args = json.loads(call.function.arguments or "{}")
            result = memory.save_memory(
                user_id,
                args.get("key", ""),
                args.get("value", ""),
            )

            print("  [স্মৃতি]", result)

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": result,
                }
            )
    else:
        print("মিতু: উত্তর তৈরিতে সমস্যা হলো।")

print("বন্ধ হলো।")
```

**চালান:**

```bash
python 03-memory-friend/02_memory_agent.py
```

**প্রথমবার (নতুন তথ্য শেখা):**

```
User id (Enter = rafi): rafi
মিতুর সাথে কথা বলুন (rafi)।
/memory = স্মৃতি দেখা, /forget = মুছে ফেলা, /reset = কথোপকথন নতুন, exit = বন্ধ
তুমি: আমার নাম রাফি
  [স্মৃতি] মনে রাখলাম: নাম = রাফি
মিতু: নাম মনে রাখলাম, রাফি। কী সাহায্য দিতে পারি?
তুমি: আমার প্রিয় শহর চট্টগ্রাম
  [স্মৃতি] মনে রাখলাম: প্রিয় শহর = চট্টগ্রাম
মিতু: প্রিয় শহর মনে রাখলাম, চট্টগ্রাম। আরও কিছু জানাতে চাইলে বলুন।
তুমি: exit
বন্ধ হলো।
```

**প্রোগ্রাম বন্ধ করে আবার চালান:**

```
User id (Enter = rafi): rafi
তুমি: আমার নাম কী?
মিতু: তোমার নাম **রাফি**।
তুমি: আমার প্রিয় শহর এখন ঢাকা
  [স্মৃতি] মনে রাখলাম: প্রিয় শহর = ঢাকা
মিতু: ঠিক আছে, এখন থেকে তোমার প্রিয় শহর **ঢাকা**।
তুমি: /memory
- নাম: রাফি
- প্রিয় শহর: ঢাকা
```

নতুন প্রোগ্রামেও নাম মনে আছে — কারণ নামটা ছিল ফাইলে, মডেলের মাথায় নয়।

### কোন অংশ কী কাজ করে

| অংশ | কাজ |
|---|---|
| `TOOLS` | মডেলের একমাত্র টুল: `save_memory` |
| `start_messages(user_id)` | স্মৃতি ফাইল থেকে পড়ে system prompt-এ বসানো |
| `## যা মনে আছে` | মডেল এখান থেকেই উত্তর দেয় |
| `messages[0] = ...` | **প্রতি টার্নে** স্মৃতি নতুন করে বসানো |
| `user_id` | কার খাতা — আলাদা মানুষ আলাদা স্মৃতি |
| `/memory` | ফাইলে কী আছে দেখানো |
| `/forget` | স্মৃতি মুছে ফেলা |
| `/reset` | শুধু কথোপকথন নতুন, স্মৃতি থাকে |
| `for step in range(5)` | Phase 3-এর মতোই টুল লুপ |

### কেন `messages[0]` প্রতিবার বদলায়?

একই কথোপকথনে আপনি নতুন তথ্য দিলেন। মডেল `save_memory` দিয়ে সেভ করল, কিন্তু system prompt-এ সেটা তখনো বসেনি। পরের প্রশ্নের আগে `messages[0]` নতুন করে বানালে নতুন তথ্যও "যা মনে আছে"-তে ঢুকে পড়ে।

---

## দুই স্মৃতি একসাথে

| কাজ | Short-term (`messages`) | Long-term (`memories.json`) |
|---|---|---|
| "আগের প্রশ্ন কী ছিল?" | ✅ | ❌ |
| "আমার নাম কী?" | প্রোগ্রাম চললে ✅ | সবসময় ✅ |
| `/reset` | মুছে যায় | থাকে |
| `/forget` | থাকে | মুছে যায় |
| প্রোগ্রাম বন্ধ | মুছে যায় | থাকে |

---

# পরীক্ষা — ৫টি ধাপ

| # | কাজ | প্রত্যাশা |
|---|---|---|
| 1 | "আমার নাম রাফি" বলুন | `[স্মৃতি] মনে রাখলাম: নাম = রাফি` |
| 2 | প্রোগ্রাম বন্ধ করে আবার চালান | "আমার নাম কী?" → রাফি |
| 3 | new user id দিয়ে চালান (যেমন `karim`) | রাফিকে চেনে না — আলাদা খাতা |
| 4 | "আমার প্রিয় শহর এখন ঢাকা" বলুন | `/memory`-তে পুরনো শহর বদলে ঢাকা |
| 5 | `/forget` দিন, তারপর নাম জিজ্ঞেস করুন | "আমি জানি না" |

### `/reset` বনাম `/forget`

`02_memory_agent.py` চালিয়ে `/reset` দিন, তারপর জিজ্ঞেস করুন:

```
তুমি: /reset
কথোপকথন রিসেট হলো। স্মৃতি ঠিক আছে।
তুমি: আমার নাম কী?
মিতু: তোমার নাম **রাফি**।
তুমি: আমি কী কী বলেছিলাম?
মিতু: এই কথোপকথনে তুমি শুধু একবার বলেছিলে: "আমার নাম কী?"
আমার মেমরিতে তোমার সম্পর্কে দুইটি তথ্য আছে:
- নাম: রাফি
- প্রিয় শহর: ঢাকা
```

এটাই আসল শিক্ষা: **কথোপকথন মুছে গেছে, কিন্তু মানুষকে চেনা যায়নি।**

---

## স্মৃতি নিয়ে ৩টি নিয়ম

1. **স্থায়ী তথ্য রাখুন, সাময়িক নয়** — "আমার নাম রাফি" রাখুন; "আজ ক্লান্ত" রাখবেন না।
2. **নতুন তথ্য পুরনোটাকে বদলাক** — একই `key` ব্যবহার করলে override হয়।
3. **ইউজারের নিয়ন্ত্রণ দিন** — `/memory` দিয়ে দেখা, `/forget` দিয়ে মুছে ফেলা।

### গোপনীয়তা

`memories.json`-এ আসল নাম, শহর, পছন্দ থাকে। তাই ফাইলটা `.gitignore`-এ আছে — GitHub-এ যাবে না। এই ফাইল আপনার কম্পিউটারেই থাকে।

---

## স্মৃতি বড় হলে?

এখন সব স্মৃতি প্রতিবার prompt-এ যায়। ১০–২০টি তথ্যে এটা ঠিক আছে।

কিন্তু ১০,০০০ নোট থাকলে পুরোটা পাঠানো যায় না — context window ভরে যাবে। তখন দরকার **retrieve**: সব নয়, শুধু প্রাসঙ্গিক অংশ খুঁজে আনা। সেটার নাম RAG (embedding + similarity search)। ধারণাটা সিলেবাসে আছে — [সিলেবাস](../ai-agent-syllabus-bangla.md)।

---

## সমস্যা হলে

| যা দেখছেন | সমাধান |
|---|---|
| সেভ হচ্ছে না (`[স্মৃতি]` আসে না) | মডেল টুল না ডাকলে `prompts/system.md`-এর নিয়ম দেখুন |
| বাংলা এলোমেলো | Git Bash / Windows Terminal ব্যবহার করুন |
| `JSONDecodeError` | `memories.json` হাতে ভাঙা হয়েছে — ফাইলটা মুছে আবার চালান |
| `memories.json` খুঁজে পাচ্ছি না | প্রথম save-এর আগে ফাইল থাকে না — `python 03-memory-friend/01_memory_test.py` চালিয়ে `03-memory-friend/` দেখুন |
| দুইজনের তথ্য মিশে যাচ্ছে | শুরুতে সঠিক `user id` দিয়েছেন কি না দেখুন |
| `401` / `429` | Phase 0-এর `.env` ও মডেল দেখুন |

---

## শেষ চেকলিস্ট

- [ ] `01_memory_test.py` চালিয়ে ৫টি ধাপ দেখেছেন
- [ ] `03-memory-friend/memories.json` নিজে খুলে দেখেছেন (প্রথম save-এর পরে তৈরি হয়)
- [ ] সেভ করার পর প্রোগ্রাম বন্ধ করে আবার চালিয়ে দেখেছেন
- [ ] `karim` দিয়ে আলাদা খাতা পরীক্ষা করেছেন
- [ ] পুরনো পছন্দ override হয়েছে
- [ ] `/memory` আর `/forget` কাজ করেছে
- [ ] `/reset`-এর পরেও স্মৃতি থাকে — নিজের ভাষায় বলতে পারেন

---

## পরের ধাপ

Phase 5 — **Research Buddy** (ফোল্ডার: [`04-research-buddy`](../04-research-buddy/README.md))।
এখন কাজগুলো এক লাইনে চলে। পরের ফেজে LangGraph দিয়ে একাধিক ধাপ — খোঁজা, সারাংশ, সমালোচনা — গ্রাফে সাজানো হবে।
