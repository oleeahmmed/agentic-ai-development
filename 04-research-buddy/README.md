# Phase 5 — Research Buddy (সহজ গাইড)

> **লক্ষ্য:** একাধিক ধাপের কাজ স্পষ্ট গ্রাফে সাজানো — খোঁজা, সারাংশ, সমালোচনা, দরকার হলে আবার খোঁজা, শেষে সোর্সসহ রিপোর্ট।
> **সময়:** ২ সপ্তাহ, দিনে ৩০–৬০ মিনিট।

---

## শুরুর আগে

Phase 0-এর `.env` ঠিক থাকতে হবে। LangGraph-ও ইনস্টল করতে হবে:

```bash
source .venv/Scripts/activate
pip install -r 00-setup/requirements.txt
python 00-setup/check_env.py
```

`requirements.txt`-এ এখন চারটি প্যাকেজ — নতুনটি `langgraph`।

---

## গল্প: মিতুর হাতে গবেষণার দায়িত্ব

Phase 2–4-এ মিতু এক প্রশ্নের উত্তর দিত। কিন্তু "কৃত্রিম বুদ্ধিমত্তা নিয়ে একটা রিপোর্ট বানাও" — এটা এক ধাপের কাজ নয়।

রিপোর্ট বানাতে হয়:

1. প্রশ্নটা ছোট প্রশ্নে ভাঙা
2. প্রতিটা প্রশ্নে খোঁজা
3. পাওয়া লেখা পড়ে সারাংশ বানানো
4. "এই সারাংশে উত্তরটা সম্পূর্ণ?" — নিজেই সমালোচনা
5. না হলে আবার খোঁজা
6. অনুমতি নিয়ে রিপোর্ট লেখা

Phase 3-এ এই কাজটা একটার পর একটা `for` লুপে করতেন। ধাপ বাড়লে লুপ জটিল হয়ে যায়, আর "কোথায় আছি, কোন ধাপে আটকেছে" বোঝা কঠিন।

**গ্রাফ** এই সমস্যার সমাধান: প্রতিটি কাজ একটা বাক্স (node), বাক্সগুলোর মাঝে তীর (edge), আর শর্ত থাকলে শাখা (conditional edge)। ছবিটা কাগজে আঁকা যায়, কোডেও ঠিক সেই ছবিটাই লেখা হয়।

---

## এই ফোল্ডারে কী আছে

| ফাইল | কাজ |
|---|---|
| `tools.py` | উইকিপিডিয়ায় সার্চ ও পাতা পড়া |
| `01_test_tools.py` | LLM ছাড়া টুল পরীক্ষা |
| `nodes.py` | গ্রাফের প্রতিটি কাজ (node) |
| `graph.py` | বাক্স-তীর জোড়া, লুপ, অনুমতি, রিপোর্ট |
| `prompts/system.md` | গবেষণা সহকারীর নিয়ম |
| `reports/` | তৈরি হওয়া `.md` রিপোর্ট (নিজে তৈরি হবে, git-এ যাবে না) |

---

## সার্চ কোথা থেকে?

সিলেবাসে Tavily বা DuckDuckGo লেখা আছে। কিন্তু:

| বিকল্প | সমস্যা |
|---|---|
| Tavily | আলাদা API key লাগে |
| DuckDuckGo (ddgs) | এখানে "No results found" — ব্লক করে |
| **Wikipedia API** | key লাগে না, নির্ভরযোগ্য, সোর্স URL দেয় |

তাই এই প্রজেক্টে Wikipedia ব্যবহার করা হয়েছে। **গ্রাফের শিক্ষা বদলায় না** — পরে `tools.py`-এর ভিতরে Tavily বসালেই হবে। টুল বদলানো আর গ্রাফ বদলানো আলাদা কাজ।

> উইকিপিডিয়া পরপর অনেক অনুরোধ পছন্দ করে না। তাই `tools.py`-তে ছোট বিরতি, ক্যাশ আর retry রাখা হয়েছে।

---

# পাঠ ১ — `tools.py`

**কোথায়:** `04-research-buddy/tools.py`

```python
import re
import time

import httpx

HEADERS = {
    "User-Agent": (
        "ai-agent-learning/1.0 "
        "(https://github.com/oleeahmmed/agentic-ai-development; educational project)"
    )
}
API_URL = "https://en.wikipedia.org/w/api.php"

_PAGES = {}


def clean(text):
    return re.sub(r"<[^>]+>", "", text or "")


def get_json(params):
    for attempt in range(3):
        response = httpx.get(
            API_URL,
            params=params,
            headers=HEADERS,
            timeout=15,
            trust_env=False,
        )

        if response.status_code == 200:
            return response.json()

        time.sleep(1 + attempt)

    return {}


def search_wikipedia(query, limit=3):
    data = get_json(
        {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "utf8": 1,
            "srlimit": limit,
        }
    )
    results = data.get("query", {}).get("search", [])

    return [
        {
            "title": item["title"],
            "url": "https://en.wikipedia.org/wiki/" + item["title"].replace(" ", "_"),
            "snippet": clean(item.get("snippet", "")),
        }
        for item in results
    ]


def read_page(title):
    if title in _PAGES:
        return _PAGES[title]

    data = get_json(
        {
            "action": "query",
            "prop": "extracts",
            "explaintext": 1,
            "redirects": 1,
            "titles": title,
            "format": "json",
            "utf8": 1,
        }
    )
    pages = data.get("query", {}).get("pages", {})
    page = next(iter(pages.values()), None)

    if not page or "missing" in page:
        _PAGES[title] = None
        return None

    result = {
        "title": page.get("title", title),
        "url": "https://en.wikipedia.org/wiki/" + page.get("title", title).replace(" ", "_"),
        "text": page.get("extract", ""),
    }

    _PAGES[title] = result

    return result


def search_and_read(query, limit=2):
    pages = []

    for result in search_wikipedia(query, limit):
        time.sleep(0.5)
        page = read_page(result["title"])

        if page and page["text"]:
            pages.append(page)

    return pages
```

### কোন অংশ কী কাজ করে

| অংশ | কাজ |
|---|---|
| `HEADERS` | উইকিপিডিয়াকে "কে অনুরোধ করছে" জানানো; না দিলে 403 আসে |
| `API_URL` | উইকিপিডিয়ার একটি API, সব কাজ এখানেই |
| `_PAGES = {}` | পড়া পাতা মনে রাখা — একই পাতা দুইবার আনবে না |
| `clean(text)` | সার্চের ফলাফল থেকে `<span>` ট্যাগ মুছে দেওয়া |
| `get_json(params)` | অনুরোধ পাঠিয়ে JSON ফেরত দেয়; ২০০ না হলে ৩ বার চেষ্টা |
| `time.sleep(1 + attempt)` | ব্যর্থ হলে ১, ২ সেকেন্ড থেমে আবার চেষ্টা |
| `search_wikipedia(...)` | প্রশ্ন → শিরোনাম, লিংক, ছোট অংশ |
| `read_page(title)` | শিরোনাম → পুরো পাতার প্লেইন টেক্সট + আসল URL |
| `redirects: 1` | "LangGraph" লিখলে উইকিপিডিয়া "LangChain"-এ পাঠালেও কাজ করে |
| `explaintext: 1` | HTML নয়, পরিষ্কার লেখা |
| `next(iter(pages.values()))` | উইকিপিডিয়ার অদ্ভুত JSON থেকে প্রথম পাতা বের করা |
| `search_and_read(...)` | সার্চ + পড়া একসাথে; `limit=2` মানে প্রথম ২টি পাতা |
| `time.sleep(0.5)` | পরপর অনুরোধে উইকিপিডিয়ার রাগ এড়ানো |

**সবচেয়ে গুরুত্বপূর্ণ:** এখানে LLM নেই। এটা শুধু ইন্টারনেট থেকে সত্য তথ্য আনার হাত।

---

# পাঠ ২ — টুল পরীক্ষা: `01_test_tools.py`

LLM ছাড়া আগে টুল ঠিক আছে কি না দেখুন।

**ফাইল:** `01_test_tools.py`

```python
import sys

from tools import read_page, search_and_read, search_wikipedia

sys.stdout.reconfigure(encoding="utf-8")

print("১. সার্চ")
for item in search_wikipedia("Artificial intelligence", 3):
    print("-", item["title"])
    print(" ", item["url"])
    print(" ", item["snippet"][:80])
print()

print("২. একটি পাতা পড়া")
page = read_page("Artificial intelligence")
print("শিরোনাম:", page["title"])
print("লিংক:", page["url"])
print("লেখা:", page["text"][:200], "...")
print()

print("৩. সার্চ + পড়া একসাথে")
for page in search_and_read("Python programming language", 2):
    print("-", page["title"], "| অক্ষর:", len(page["text"]))
print()

print("৪. অচেনা বিষয়")
print(search_wikipedia("Xyzzyville qwerty", 2))
```

**চালান:**

```bash
python 04-research-buddy/01_test_tools.py
```

**ফলাফল (বদলাতে পারে):**

```
১. সার্চ
- Artificial intelligence
  https://en.wikipedia.org/wiki/Artificial_intelligence
  Artificial intelligence (AI) is the capability of computational systems to perfo
- Artificial general intelligence
  https://en.wikipedia.org/wiki/Artificial_general_intelligence
  Artificial general intelligence (AGI) is a hypothetical type of artificial intel
- A.I. Artificial Intelligence
  https://en.wikipedia.org/wiki/A.I._Artificial_Intelligence
  A.I. Artificial Intelligence (or simply A.I.) is a 2001 American science fiction

২. একটি পাতা পড়া
শিরোনাম: Artificial intelligence
লিংক: https://en.wikipedia.org/wiki/Artificial_intelligence
লেখা: Artificial intelligence (AI) is the capability of computational systems to ...

৩. সার্চ + পড়া একসাথে
- Artificial intelligence | অক্ষর: 58213
- Artificial general intelligence | অক্ষর: 32078

৪. অচেনা বিষয়
[]
```

### কোন অংশ কী কাজ করে

| অংশ | কাজ |
|---|---|
| `from tools import ...` | পাশের `tools.py` থেকে তিনটি function |
| `search_wikipedia(..., 3)` | প্রথম ৩টি ফলাফল |
| `item["snippet"][:80]` | সার্চের ছোট অংশের প্রথম ৮০ অক্ষর |
| `read_page(...)` | এক পাতার পুরো লেখা |
| `page["text"][:200]` | লেখার প্রথম ২০০ অক্ষর |
| `search_and_read(..., 2)` | সার্চ করে প্রথম ২টি পাতা পড়া |
| `len(page["text"])` | কত অক্ষর পাওয়া গেল |
| `Xyzzyville qwerty` | ভুয়া বিষয় — খালি তালিকা, error নয় |

**পরীক্ষা:** `print(search_wikipedia("চট্টগ্রাম", 2))` দিয়ে দেখুন উইকিপিডিয়া বাংলা লেখা চেনে কি না। (সার্চ সাধারণত কাজ করে, তবে আমরা সার্চ প্রশ্ন ইংরেজিতে চাইব — কারণ ইংরেজি পাতায় তথ্য বেশি।)

---

# পাঠ ৩ — `prompts/system.md`

**কোথায়:** `04-research-buddy/prompts/system.md`

```markdown
# গবেষণা সহকারী

তুমি Little Office Ltd.-এর গবেষণা সহকারী।

## নিয়ম

- সব উত্তর বাংলায় দাও।
- শুধু দেওয়া উৎসের তথ্য ব্যবহার করো। বাইরের জ্ঞান ব্যবহার করো না।
- প্রতিটি তথ্যের পাশে উৎসের নম্বর দাও: [1], [2]।
- উৎসে উত্তর না থাকলে স্পষ্ট বলো: "উৎসে এই তথ্য নেই।"
- কখনো নিজে URL বানিয়ে লিখো না।
- সংক্ষেপে ও পরিষ্কারভাবে লেখো।
```

### কোন অংশ কী কাজ করে

| অংশ | কাজ |
|---|---|
| "শুধু দেওয়া উৎসের তথ্য" | মডেলের বাইরের জ্ঞান বন্ধ — বানিয়ে বলার সুযোগ কমে |
| "প্রতিটি তথ্যের পাশে [1], [2]" | কোন দাবি কোন উৎস থেকে, তা বোঝা যায় |
| "উৎসে এই তথ্য নেই" | না জানলে সৎভাবে বলা |
| "নিজে URL বানিয়ে লিখো না" | ভুয়া লিংক ঠেকানো |

> নিয়মগুলো **প্রম্পটে** রাখা হয়েছে, কোডে নয়। কাজের ধরন বদলালে শুধু এই ফাইল বদলান।

---

# পাঠ ৪ — `nodes.py`

**কোথায়:** `04-research-buddy/nodes.py`

প্রতিটি node হলো `function(state) -> আংশিক আপডেট`। ফাংশন পুরো state ফেরত দেয় না — শুধু যা বদলেছে।

```python
import json
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from langgraph.types import interrupt
from openai import OpenAI

import tools

base = Path(__file__).parent
load_dotenv(base.parent / "00-setup" / ".env")

api_key = os.getenv("LLM_API_KEY")
model = os.getenv("LLM_MODEL")

if not api_key or not model:
    raise SystemExit("00-setup/.env ফাইলে LLM_API_KEY আর LLM_MODEL দিন।")

client = OpenAI(api_key=api_key, base_url=os.getenv("LLM_BASE_URL"))
system_prompt = (base / "prompts" / "system.md").read_text(encoding="utf-8")


def ask(prompt):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content.strip()


def ask_json(prompt):
    text = ask(prompt).strip()
    text = text.strip("`").strip()

    if text.startswith("json"):
        text = text[4:].strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def source_text(sources, limit=2500):
    parts = []

    for number, source in enumerate(sources, 1):
        parts.append(f"[{number}] {source['title']}\n{source['text'][:limit]}")

    return "\n\n".join(parts)


def plan_node(state):
    question = state["question"]

    data = ask_json(
        f"প্রশ্ন: {question}\n\n"
        "এই প্রশ্নের উত্তর খুঁজতে উইকিপিডিয়ায় ব্যবহারের জন্য ২–৩টি ছোট ইংরেজি সার্চ প্রশ্ন লেখো। "
        'শুধু JSON তালিকা দাও, যেমন: ["query one", "query two"]'
    )

    if not isinstance(data, list) or not data:
        queries = [question]
    else:
        queries = [str(item) for item in data[:3]]

    return {"queries": queries}


def search_node(state):
    sources = list(state["sources"])
    seen = {source["url"] for source in sources}
    log = []

    for query in state["queries"]:
        log.append(query)

        for page in tools.search_and_read(query, limit=2):
            if page["url"] in seen:
                continue

            seen.add(page["url"])
            sources.append(page)

    return {"sources": sources, "search_log": log}


def summarize_node(state):
    if not state["sources"]:
        return {"summary": ""}

    summary = ask(
        f"প্রশ্ন: {state['question']}\n\n"
        f"উৎস:\n{source_text(state['sources'])}\n\n"
        "শুধু উৎসের তথ্য দিয়ে বাংলায় ২৫০ শব্দের মধ্যে সারাংশ লেখো। "
        "প্রতিটি তথ্যের পাশে [1], [2] এভাবে উৎস নম্বর দাও।"
    )

    return {"summary": summary}


def critique_node(state):
    if not state["sources"]:
        return {"enough": False, "gaps": "কোনো উৎস পাওয়া যায়নি।"}

    data = ask_json(
        f"প্রশ্ন: {state['question']}\n\n"
        f"সারাংশ:\n{state['summary']}\n\n"
        "এই সারাংশ প্রশ্নের সম্পূর্ণ উত্তর দেয় কি? না দিলে কী তথ্য বাকি, সংক্ষেপে লেখো। "
        'শুধু JSON: {"enough": true অথবা false, "gaps": "বাকি তথ্য"}'
    )

    if not isinstance(data, dict):
        return {"enough": True, "gaps": ""}

    return {
        "enough": bool(data.get("enough", True)),
        "gaps": str(data.get("gaps", "")),
    }


def revise_node(state):
    data = ask_json(
        f"মূল প্রশ্ন: {state['question']}\n\n"
        f"ঘাটতি: {state['gaps']}\n\n"
        f"আগে যা খোঁজা হয়েছে: {', '.join(state['search_log'])}\n\n"
        "ঘাটতি ভরাতে উইকিপিডিয়ায় ১–২টি নতুন ইংরেজি সার্চ প্রশ্ন লেখো। "
        "শুধু JSON তালিকা দাও।"
    )

    if isinstance(data, list) and data:
        queries = [str(item) for item in data[:2]]
    else:
        queries = [state["question"] + " details"]

    return {"queries": queries, "rounds": state["rounds"] + 1}


def approve_node(state):
    answer = interrupt("রিপোর্ট লেখা হবে? (y/n)")

    return {"approved": str(answer).strip().lower().startswith("y")}


def write_node(state):
    body = ask(
        f"প্রশ্ন: {state['question']}\n\n"
        f"উৎস:\n{source_text(state['sources'])}\n\n"
        "এই প্রশ্নের উত্তর দিয়ে বাংলায় ৪০০–৬০০ শব্দের একটি রিপোর্ট লেখো। "
        "প্রতিটি দাবির পাশে [1], [2] এভাবে উৎস নম্বর দাও। "
        "উৎসে না থাকা কোনো তথ্য লিখো না।"
    )

    lines = [f"# {state['question']}", "", body, "", "## উৎস", ""]

    for number, source in enumerate(state["sources"], 1):
        lines.append(f"{number}. [{source['title']}]({source['url']})")

    folder = base / "reports"
    folder.mkdir(exist_ok=True)

    name = "report-" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".md"
    file = folder / name
    file.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return {"report_path": str(file)}
```

### প্রতিটি অংশ কী কাজ করে

| অংশ | কাজ |
|---|---|
| `ask(prompt)` | system prompt + প্রশ্ন পাঠিয়ে উত্তর আনা |
| `ask_json(prompt)` | `ask` করে উত্তরকে dict/list বানায়; না পারলে `None` |
| `strip` | উত্তরের দুই পাশের ব্যাকটিক ও ফাঁকা জায়গা সরানো |
| `startswith("json")` | কোড-ব্লকের "json" শব্দটা বাদ দেওয়া |
| `source_text(sources)` | উৎসগুলোকে `[1] শিরোনাম + লেখা` আকারে সাজানো |
| `limit=2500` | প্রতিটি উৎসের প্রথম ২৫০০ অক্ষর — prompt যেন না ফেটে |
| `plan_node` | প্রশ্ন → ২–৩টি ইংরেজি সার্চ প্রশ্ন |
| `search_node` | সার্চ প্রশ্ন → উৎসের তালিকা; একই URL দুইবার নয় |
| `seen = {...}` | আগে পাওয়া URL মনে রাখা, ডুপ্লিকেট বাদ দেওয়া |
| `summarize_node` | উৎস → বাংলা সারাংশ, `[1]` সাইটেশনসহ |
| `critique_node` | সারাংশ যথেষ্ট কি না, কী বাকি — JSON-এ |
| `revise_node` | ঘাটতি → নতুন সার্চ প্রশ্ন; `rounds` এক বাড়ে |
| `interrupt(...)` | গ্রাফ এখানে **থেমে যায়**, মানুষের উত্তর পর্যন্ত |
| `approve_node` | `y` হলে `approved = True` |
| `write_node` | রিপোর্ট লেখা + নিচে আসল উৎসের তালিকা |
| `datetime.now().strftime(...)` | ফাইলের নামে তারিখ-সময়, যাতে পুরনোটা নষ্ট না হয় |
| `folder.mkdir(exist_ok=True)` | `reports/` না থাকলে বানানো |

### JSON কেন চাইছি?

`plan_node` আর `critique_node` — দুই জায়গায় মডেলের উত্তর কোডে দরকার (তালিকা বা `true/false`)। তাই মডেলকে **শুধু JSON** দিতে বলা হয়েছে।

তবু মডেল ভুল করতে পারে। তাই `ask_json` ব্যর্থ হলে `None` ফেরত দেয়, আর প্রতিটি node একটি নিরাপদ বিকল্প বেছে নেয়:

| node | JSON না পেলে |
|---|---|
| `plan_node` | পুরো প্রশ্নটাই এক সার্চ হিসেবে ব্যবহার |
| `critique_node` | ধরে নেয় "যথেষ্ট" (অনন্ত লুপ এড়াতে) |
| `revise_node` | প্রশ্নের সাথে `details` জুড়ে নতুন সার্চ |

---

# পাঠ ৫ — `graph.py`

**কোথায়:** `04-research-buddy/graph.py`

এখানেই গ্রাফের ছবিটা কোডে লেখা হয়।

```python
import operator
import sys
import uuid
from typing import Annotated, TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command

import nodes

sys.stdout.reconfigure(encoding="utf-8")


class ResearchState(TypedDict):
    question: str
    queries: list[str]
    search_log: Annotated[list[str], operator.add]
    sources: list[dict]
    summary: str
    enough: bool
    gaps: str
    rounds: int
    approved: bool
    report_path: str


def next_step(state):
    if state["enough"] or state["rounds"] >= 3:
        return "approve"

    return "revise"


def after_approval(state):
    if state["approved"] and state["sources"]:
        return "write_report"

    return END


builder = StateGraph(ResearchState)
builder.add_node("plan", nodes.plan_node)
builder.add_node("search", nodes.search_node)
builder.add_node("summarize", nodes.summarize_node)
builder.add_node("critique", nodes.critique_node)
builder.add_node("revise", nodes.revise_node)
builder.add_node("approve", nodes.approve_node)
builder.add_node("write_report", nodes.write_node)

builder.add_edge(START, "plan")
builder.add_edge("plan", "search")
builder.add_edge("search", "summarize")
builder.add_edge("summarize", "critique")
builder.add_conditional_edges("critique", next_step)
builder.add_edge("revise", "search")
builder.add_conditional_edges("approve", after_approval)
builder.add_edge("write_report", END)

graph = builder.compile(checkpointer=MemorySaver())


def show(chunk):
    for name, update in chunk.items():
        if name == "__interrupt__":
            print("  [থামা]", update[0].value)
            continue

        print("  [ধাপ]", name)

        if name == "search":
            print("       উৎস:", len(update.get("sources", [])))
        if name == "critique":
            print("       যথেষ্ট?", update.get("enough"))
        if name == "revise":
            print("       নতুন সার্চ:", update.get("queries"))
        if name == "write_report":
            print("       সেভ:", update.get("report_path"))


def research(question):
    config = {
        "configurable": {"thread_id": "run-" + uuid.uuid4().hex[:8]},
        "recursion_limit": 25,
    }
    state = {
        "question": question,
        "queries": [],
        "search_log": [],
        "sources": [],
        "summary": "",
        "enough": False,
        "gaps": "",
        "rounds": 0,
        "approved": False,
        "report_path": "",
    }

    for chunk in graph.stream(state, config=config, stream_mode="updates"):
        show(chunk)

    if graph.get_state(config).next:
        answer = input("\nরিপোর্ট লেখা হবে? (y/n): ").strip()

        for chunk in graph.stream(Command(resume=answer), config=config, stream_mode="updates"):
            show(chunk)

    final = graph.get_state(config).values

    if final.get("report_path"):
        print("\nরিপোর্ট সেভ হয়েছে:", final["report_path"])
    else:
        print("\nরিপোর্ট লেখা হয়নি।")


print("Research Buddy — প্রশ্ন লিখুন, উৎসসহ রিপোর্ট পাবেন। exit = বন্ধ")


def main():
    while True:
        question = input("\nপ্রশ্ন: ").strip()

        if question == "exit":
            break

        if not question:
            continue

        try:
            research(question)
        except Exception as error:
            print("সমস্যা:", error)


if __name__ == "__main__":
    main()
```

### গ্রাফটা দেখতে এমন

```
START → plan → search → summarize → critique ─(যথেষ্ট?)→ approve → write_report → END
                  ↑                         │                  │
                  └────── revise ←───────────┘                  └→ END (অনুমতি নেই)
```

- `critique` দুই দিকে যেতে পারে: `approve` বা `revise`
- `revise` আবার `search`-এ ফেরে — এটাই লুপ
- `approve`-এ মানুষের অনুমতি; `y` হলে `write_report`, নাহলে `END`

### state-এর প্রতিটি ঘর

| ঘর | মানে |
|---|---|
| `question` | ব্যবহারকারীর মূল প্রশ্ন |
| `queries` | এই রাউন্ডে কোন সার্চ চলবে |
| `search_log` | এ পর্যন্ত সব সার্চ — reducer দিয়ে জমা হয় |
| `sources` | পাওয়া উৎস (`title`, `url`, `text`) |
| `summary` | বাংলা সারাংশ |
| `enough` | সারাংশ যথেষ্ট কি না |
| `gaps` | কী তথ্য বাকি |
| `rounds` | কতবার `revise` হয়েছে |
| `approved` | মানুষ রিপোর্ট লিখতে অনুমতি দিয়েছে কি না |
| `report_path` | সেভ করা ফাইলের ঠিকানা |

### reducer কী?

```python
search_log: Annotated[list[str], operator.add]
```

সাধারণ ঘরে node যা ফেরত দেয়, সেটাই **পুরনো মান বদলে** বসে। কিন্তু `search_log`-এ `operator.add` লেখা আছে, তাই নতুন তালিকা **পুরনোটার সাথে জুড়ে যায়**।

`search_node` প্রতিবার শুধু এই রাউন্ডের সার্চ ফেরত দেয়; reducer সেগুলো জমা রাখে। তাই `revise_node` আগের সব সার্চ দেখতে পায় — একই সার্চ বারবার না করার জন্য।

### কোন ফাংশন কী করে

| অংশ | কাজ |
|---|---|
| `ResearchState` | গ্রাফের খাতা — কোন কোন ঘর থাকবে |
| `next_step` | critique-এর পর `approve` না `revise` |
| `rounds >= 3` | লুপের সীমা — অনন্ত ঘোরা বন্ধ |
| `after_approval` | অনুমতি আছে এবং উৎস আছে → রিপোর্ট |
| `StateGraph(ResearchState)` | খালি গ্রাফ, খাতার আকার দেওয়া |
| `add_node(...)` | প্রতিটি বাক্স যোগ |
| `add_edge(...)` | সবসময়ের তীর |
| `add_conditional_edges(...)` | শর্তসাপেক্ষ তীর |
| `START`, `END` | গ্রাফের শুরু ও শেষ |
| `compile(checkpointer=...)` | গ্রাফ চালানোর উপযোগী করা + স্মৃতি |
| `graph.stream(...)` | ধাপে ধাপে চালানো — কোন node চলছে দেখা যায় |
| `stream_mode="updates"` | প্রতিটি node কী বদলাল, তা টুকরো টুকরো পাওয়া |
| `graph.get_state(config)` | এই `thread_id`-এর সর্বশেষ অবস্থা |
| `.next` | পরের ধাপ কী — খালি না হলে গ্রাফ থেমে আছে |
| `Command(resume=answer)` | থেমে থাকা গ্রাফকে উত্তর দিয়ে আবার চালানো |
| `thread_id` | কোন কাজের খাতা — একই id দিলে একই কাজ চলবে |
| `recursion_limit: 25` | সর্বোচ্চ ২৫টি ধাপ; তার বেশি হলে error |
| `if __name__ == "__main__"` | সরাসরি চালালে `main()`; import করলে চলে না |

### checkpointer কেন লাগে?

`interrupt` দিয়ে থামলে গ্রাফের সব state কোথাও রাখতে হয়। নাহলে আবার চালানোর সময় "আমি কোথায় ছিলাম" জানবে না।

`MemorySaver()` সেই state **RAM-এ** রাখে। তাই:

- একই প্রোগ্রাম চলাকালীন থামা → resume কাজ করে
- প্রোগ্রাম বন্ধ করলে state মুছে যায়

প্রোগ্রাম বন্ধ করার পরেও চালু রাখতে `SqliteSaver` লাগে — এটা পরে করতে পারেন (Stretch)।

### `interrupt` কীভাবে কাজ করে

1. `approve_node` চলার সময় `interrupt(...)` ডাকা হয়
2. গ্রাফ সেখানেই থেমে যায়, state সেভ হয়
3. `graph.get_state(config).next` দেখায় `('approve',)`
4. ব্যবহারকারী `y` বা `n` দিলে `Command(resume=...)` গ্রাফকে আবার চালায়
5. `interrupt(...)`-এর ফেরত মান হয়ে ওঠে সেই উত্তর

> এজেন্ট নিজে থেকে ফাইল লিখবে না — মানুষের অনুমতি লাগবে। Phase 8-এর ইমেইল/রিফান্ডেও একই কৌশল।

---

# চালান

```bash
python 04-research-buddy/graph.py
```

**এভাবে কথা বলুন (উদাহরণ — উত্তর মডেলভেদে বদলাবে):**

```
Research Buddy — প্রশ্ন লিখুন, উৎসসহ রিপোর্ট পাবেন। exit = বন্ধ

প্রশ্ন: কৃত্রিম বুদ্ধিমত্তা কী?
  [ধাপ] plan
  [ধাপ] search
       উৎস: 4
  [ধাপ] summarize
  [ধাপ] critique
       যথেষ্ট? True
  [থামা] রিপোর্ট লেখা হবে? (y/n)

রিপোর্ট লেখা হবে? (y/n): y
  [ধাপ] approve
  [ধাপ] write_report
       সেভ: C:\Users\olee\Desktop\ai-agent\04-research-buddy\reports\report-20260901-101500.md

রিপোর্ট সেভ হয়েছে: C:\Users\olee\Desktop\ai-agent\04-research-buddy\reports\report-20260901-101500.md

প্রশ্ন: exit
```

**রিপোর্ট ফাইলের আকার:**

```markdown
# কৃত্রিম বুদ্ধিমত্তা কী?

## পরিচয়
কৃত্রিম বুদ্ধিমত্তা (AI) হলো এমন সিস্টেম, যা মানুষের মতো শেখা, যুক্তি ও সমস্যা সমাধান করতে পারে [1]। ...

## উৎস

1. [Artificial intelligence](https://en.wikipedia.org/wiki/Artificial_intelligence)
2. [Machine learning](https://en.wikipedia.org/wiki/Machine_learning)
```

### প্রতিটি লগের মানে

| লগ | মানে |
|---|---|
| `[ধাপ] plan` | প্রশ্ন ভাঙা হলো |
| `[ধাপ] search` | উইকিপিডিয়ায় খোঁজা হলো |
| `উৎস: 4` | ৪টি অনন্য পাতা পাওয়া গেছে |
| `[ধাপ] critique` | নিজের সারাংশ যাচাই |
| `যথেষ্ট? False` | আরও খোঁজা দরকার |
| `[ধাপ] revise` | নতুন সার্চ প্রশ্ন |
| `[থামা]` | মানুষের অনুমতির জন্য অপেক্ষা |
| `[ধাপ] write_report` | রিপোর্ট ফাইলে সেভ |

---

# পরীক্ষা — ৫টি

| # | কাজ | প্রত্যাশা |
|---|---|---|
| 1 | সহজ প্রশ্ন ("Python কী?") | এক রাউন্ডেই `যথেষ্ট? True`, অনুমতির পর রিপোর্ট |
| 2 | বড় প্রশ্ন ("কৃত্রিম বুদ্ধিমত্তার ইতিহাস") | `False` আসলে `revise` → আবার `search` |
| 3 | বারবার `False` দিলে | ৩ রাউন্ডের পরে থেমে যায়, অনুমতি চায় |
| 4 | অনুমতির সময় `n` | `write_report` চলে না, কোনো ফাইল তৈরি হয় না |
| 5 | অচেনা বিষয় ("Xyzzyville") | উৎস ০, সারাংশ খালি, রিপোর্ট হয় না |

### "লুপ অনন্ত হয় না" — প্রমাণ

দুই স্তরের সুরক্ষা আছে:

1. `next_step`-এ `rounds >= 3` — চারবারের বেশি সার্চ নয়
2. `recursion_limit: 25` — LangGraph নিজেই ২৫ ধাপের পরে থামিয়ে দেয়

একটা লুপ-প্রবণ প্রশ্ন দিয়ে দেখুন — ৩ রাউন্ডের পরে নিজেই অনুমতি চাইবে।

### রিপোর্টের URL কি আসল?

হ্যাঁ — কারণ URL মডেল লেখে না। `write_node` শেষে কোড নিজেই `state["sources"]` থেকে লিংক বসায়:

```python
for number, source in enumerate(state["sources"], 1):
    lines.append(f"{number}. [{source['title']}]({source['url']})")
```

মডেল শুধু `[1]`, `[2]` নম্বর লেখে। নম্বরের সাথে লিংকের মিল কোডে তৈরি, তাই বানানো URL ঢোকার পথ নেই।

---

## সমস্যা হলে

| যা দেখছেন | সমাধান |
|---|---|
| `ModuleNotFoundError: langgraph` | `.venv` চালু করুন, `pip install -r 00-setup/requirements.txt` |
| `429` + `free-models-per-day` | OpenRouter ফ্রি মডেলের দৈনিক সীমা শেষ — কাল আবার, বা credits যোগ করুন, বা অন্য `:free` মডেল |
| `403` উইকিপিডিয়া থেকে | `tools.py`-এর `HEADERS`-এ User-Agent আছে কি না দেখুন |
| `429` উইকিপিডিয়া থেকে | কিছুক্ষণ থামুন; `time.sleep` বাড়ান |
| উৎস ০, রিপোর্ট হয় না | ইংরেজি বিষয় লিখুন; `01_test_tools.py` দিয়ে সার্চ পরীক্ষা করুন |
| `JSONDecodeError` নেই, কিন্তু অদ্ভুত সার্চ | মডেল JSON দেয়নি — কোড বিকল্প পথ নিয়েছে; `prompts/system.md` দেখুন |
| রিপোর্ট ফাইল খুঁজে পাচ্ছি না | `04-research-buddy/reports/`-এ দেখুন; `n` দিলে ফাইল হয় না |
| `GraphRecursionError` | `recursion_limit` বাড়ান, অথবা লুপের শর্ত দেখুন |

---

## শেষ চেকলিস্ট

- [ ] `01_test_tools.py` চালিয়ে ৪টি ফলাফল দেখেছেন
- [ ] `tools.py`-তে LLM নেই — নিজের ভাষায় বলতে পারেন
- [ ] `nodes.py`-এর প্রতিটি node `state`-এর আংশিক আপডেট ফেরত দেয় — বুঝেছেন
- [ ] `search_log`-এ reducer কেন লাগে বলতে পারেন
- [ ] `graph.py` চালিয়ে `[ধাপ]` লগ দেখেছেন
- [ ] `n` দিলে রিপোর্ট হয় না — দেখেছেন
- [ ] ৩ রাউন্ডের পরে লুপ থামে — দেখেছেন
- [ ] রিপোর্টের URL কোড থেকে আসে, মডেল থেকে নয় — বুঝেছেন
- [ ] `interrupt` → `Command(resume=...)` কীভাবে কাজ করে বলতে পারেন
- [ ] কাগজে গ্রাফ এঁকে প্রতিটি তীর ব্যাখ্যা করতে পারেন

---

## পরের ধাপ

Phase 6 — **Skills** (ফোল্ডার: [`05-skill-creator`](../05-skill-creator/README.md))।
এখন প্রতিটি কাজ কোডে লেখা। পরের ফেজে কাজের নিয়মগুলো আলাদা `SKILL.md` ফাইলে রাখা হবে — কোড না বদলিয়ে এজেন্ট নতুন কাজ শিখবে।

> **Stretch:** পুরো রিপোর্ট একবারে না লিখে প্রতিটি সোর্সের জন্য আলাদা subgraph, অথবা `Send` API দিয়ে একসাথে কয়েকটি সার্চ।
