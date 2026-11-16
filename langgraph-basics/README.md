# LangGraph বেসিক (সহজ গাইড)

> **লক্ষ্য:** Phase 3-এ যে লুপ নিজে হাতে লিখেছিলেন, সেটাই এখন গ্রাফের ছবিতে সাজানো।
> **এই পাঠে LLM লাগে না** — শুধু গ্রাফের ধারণা। Phase 5-এ এর আসল ব্যবহার আছে।
> **সময়:** ২–৩ দিন, দিনে ৩০–৬০ মিনিট।

---

## আগে যা জানা থাকা ভালো

- [Phase 0](../00-setup/README.md) — `.env` (এই পাঠে লাগবে না, Phase 5-এ লাগবে)
- [Phase 3](../02-weather-agent/README.md) — টুল, লুপ, `messages`

LangGraph নতুন জাদু নয়। Phase 3-এর লুপটাই এখানে টুকরো টুকরো করে সাজানো: কোন ধাপের পরে কোন ধাপ, আর কোন শর্তে কোথায় যাবে।

---

## কেন LLM ছাড়া?

গ্রাফের ধারণা বুঝতে মডেল দরকার নেই। এখানে প্রতিটি "কাজ" সাধারণ Python function — তাই ফলাফল প্রতিবার একই, আর চালাতে টাকা/key লাগে না।

Phase 5-এর [Research Buddy](../04-research-buddy/README.md)-তে ঠিক এই গ্রাফগুলোর ভিতরে আসল LLM বসানো হয়েছে।

---

## চালানোর নিয়ম

`langgraph` আগেই ইনস্টল করা আছে (`00-setup/requirements.txt`-এ ছিল):

```bash
source .venv/Scripts/activate
python langgraph-basics/01_first_graph.py
```

শুধু ফাইলের নাম বদলাবেন — `02_state.py`, `03_condition.py` ইত্যাদি।

> CrewAI-র `.venv-crewai` এখানে লাগবে না। এই পাঠ মূল `.venv`-এ চলে।

---

## এই ফোল্ডারে কী আছে

| ফাইল | কী শেখাবে |
|---|---|
| `01_first_graph.py` | সবচেয়ে ছোট গ্রাফ — এক নোড, শুরু থেকে শেষ |
| `02_state.py` | State-এ তথ্য জমা, নোড শুধু নিজের অংশ ফেরত দেয় |
| `03_condition.py` | শর্ত দেখে দুই পথের একটায় যাওয়া |
| `04_loop.py` | একই নোডে ফেরা — লুপ, কিন্তু থামার নিয়মসহ |
| `05_memory.py` | চেকপয়েন্টার — আগের ফল মনে রাখা |
| `06_interrupt.py` | মাঝপথে থামানো, অনুমতি নিয়ে আবার চালানো |

---

## LangGraph-এর ৪টি জিনিস

| জিনিস | কী | Phase 3-এ এর সমতুল্য |
|---|---|---|
| **State** | গ্রাফের খাতা — সব নোড একই খাতায় লেখে | `messages` |
| **Node** | একটি কাজ — সাধারণ Python function | টুল চালানো / উত্তর লেখা |
| **Edge** | কোন নোডের পরে কোনটা | `for` লুপের ক্রম |
| **Graph** | নোড + এজ মিলিয়ে মানচিত্র | পুরো `while` লুপ |

গ্রাফ বানানোর তিন ধাপ, প্রতিটি ফাইলে একই:

```python
builder = StateGraph(State)   # খাতা
builder.add_node(...)         # কাজ
builder.add_edge(...)         # পথ
graph = builder.compile()     # তৈরি
graph.invoke(...)             # চালাও
```

---

# পাঠ ১ — প্রথম গ্রাফ

সবচেয়ে ছোট গ্রাফ: শুরু → এক নোড → শেষ।

```
START ──▶ hello ──▶ END
```

**ফাইল:** `langgraph-basics/01_first_graph.py`

```python
import sys
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

sys.stdout.reconfigure(encoding="utf-8")


class State(TypedDict):
    reply: str


def hello(state):
    print("নোড পেল:", state)
    return {"reply": "হ্যালো, আমি মিতু।"}


builder = StateGraph(State)
builder.add_node("hello", hello)
builder.add_edge(START, "hello")
builder.add_edge("hello", END)

graph = builder.compile()

print("--- গ্রাফ শুরু ---")
result = graph.invoke({})
print("--- গ্রাফ শেষ ---")
print(result)
```

**চালান:**

```bash
python langgraph-basics/01_first_graph.py
```

**ফলাফল:**

```
--- গ্রাফ শুরু ---
নোড পেল: {}
--- গ্রাফ শেষ ---
{'reply': 'হ্যালো, আমি মিতু।'}
```

### কোন অংশ কী কাজ করে

| অংশ | কাজ |
|---|---|
| `class State(TypedDict)` | খাতার কাঠামো — এখানে শুধু `reply` |
| `def hello(state)` | একটি নোড — খাতা পায়, লেখা ফেরত দেয় |
| `StateGraph(State)` | গ্রাফ বানানোর শুরু |
| `add_node("hello", hello)` | নাম + আসল function |
| `add_edge(START, "hello")` | শুরুর পর `hello` চলবে |
| `add_edge("hello", END)` | `hello` শেষ হলে গ্রাফ শেষ |
| `compile()` | গ্রাফ তৈরি — এরপর চালানো যায় |
| `invoke({})` | খালি খাতা দিয়ে চালানো |

> নোড যা ফেরত দেয়, সেটা খাতায় জমা হয়। `return {"reply": ...}` মানে "খাতার `reply` ঘরে এই মান লেখো"।

**ছোট কাজ:** `reply`-এর লেখা বদলে আবার চালান।

---

# পাঠ ২ — State: খাতা ভাগ করা

দুই নোড, একই খাতা। প্রথম নোড নাম লেখে, দ্বিতীয় নোড শুধু নিজের কাজের হিসাব যোগ করে।

```
START ──▶ greet ──▶ plan ──▶ END
```

**ফাইল:** `langgraph-basics/02_state.py`

```python
import operator
import sys
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph

sys.stdout.reconfigure(encoding="utf-8")


class State(TypedDict):
    name: str
    greeting: str
    steps: Annotated[list[str], operator.add]


def greet(state):
    print("greet পেল:", state)
    return {"greeting": f"হ্যালো {state['name']}!", "steps": ["greet"]}


def plan(state):
    print("plan পেল:", state)
    return {"steps": ["plan"]}


builder = StateGraph(State)
builder.add_node("greet", greet)
builder.add_node("plan", plan)
builder.add_edge(START, "greet")
builder.add_edge("greet", "plan")
builder.add_edge("plan", END)

graph = builder.compile()

result = graph.invoke({"name": "মিতু", "steps": []})
print("--- শেষ ফল ---")
print(result)
```

**চালান:**

```bash
python langgraph-basics/02_state.py
```

**ফলাফল:**

```
greet পেল: {'name': 'মিতু', 'steps': []}
plan পেল: {'name': 'মিতু', 'greeting': 'হ্যালো মিতু!', 'steps': ['greet']}
--- শেষ ফল ---
{'name': 'মিতু', 'greeting': 'হ্যালো মিতু!', 'steps': ['greet', 'plan']}
```

### কোন অংশ কী কাজ করে

| অংশ | কাজ |
|---|---|
| `name`, `greeting` | সাধারণ ঘর — নতুন মান পুরোনোটা সরিয়ে বসে |
| `Annotated[list[str], operator.add]` | এই ঘরে নতুন list **যোগ হয়**, মুছে যায় না |
| `greet` returns `{"greeting": ..., "steps": ["greet"]}` | শুধু নিজের বদলানো ঘর ফেরত দেয় |
| `plan` returns `{"steps": ["plan"]}` | `name`/`greeting` ফেরত দেয় না — তবু খাতায় থাকে |
| `invoke({"name": ..., "steps": []})` | শুরুর খাতা |

খেয়াল করুন: `plan` কিন্তু `name` বা `greeting` ফেরত দেয়নি। তারপরও শেষ ফলে দুটোই আছে — কারণ **খাতা এক, নোড শুধু নিজের অংশ লেখে**।

`steps`-এ `operator.add` না দিলে দ্বিতীয় নোডের `["plan"]` প্রথমটার `["greet"]` মুছে দিত। এটাই **reducer**।

**ছোট কাজ:** `plan`-এ `"steps": ["plan", "end"]` করুন — শেষ list-এ কতটা থাকে?

---

# পাঠ ৩ — শর্ত: কোন পথে যাবে

একটি নোড সিদ্ধান্ত নেয়, তারপর গ্রাফ দুই পথের একটায় যায়।

```
                ┌── yes ──▶ use_tool ──┐
START ──▶ decide┤                       ├──▶ END
                └── no ───▶ answer ────┘
```

**ফাইল:** `langgraph-basics/03_condition.py`

```python
import sys
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

sys.stdout.reconfigure(encoding="utf-8")


class State(TypedDict):
    question: str
    need_tool: bool
    answer: str


def decide(state):
    need_tool = "আবহাওয়া" in state["question"]
    print("প্রশ্ন:", state["question"])
    print("টুল লাগবে?", need_tool)
    return {"need_tool": need_tool}


def router(state):
    return "yes" if state["need_tool"] else "no"


def use_tool(state):
    return {"answer": "ঢাকায় এখন ২৫°C (টুল থেকে পাওয়া)।"}


def answer(state):
    return {"answer": "এটি সাধারণ প্রশ্ন, টুল লাগে না।"}


builder = StateGraph(State)
builder.add_node("decide", decide)
builder.add_node("use_tool", use_tool)
builder.add_node("answer", answer)
builder.add_edge(START, "decide")
builder.add_conditional_edges(
    "decide",
    router,
    {"yes": "use_tool", "no": "answer"},
)
builder.add_edge("use_tool", END)
builder.add_edge("answer", END)

graph = builder.compile()

print("--- প্রশ্ন ১ ---")
print(graph.invoke({"question": "আজ ঢাকার আবহাওয়া কেমন?"}))

print("\n--- প্রশ্ন ২ ---")
print(graph.invoke({"question": "তুমি কে?"}))
```

**চালান:**

```bash
python langgraph-basics/03_condition.py
```

**ফলাফল:**

```
--- প্রশ্ন ১ ---
প্রশ্ন: আজ ঢাকার আবহাওয়া কেমন?
টুল লাগবে? True
{'question': 'আজ ঢাকার আবহাওয়া কেমন?', 'need_tool': True, 'answer': 'ঢাকায় এখন ২৫°C (টুল থেকে পাওয়া)।'}

--- প্রশ্ন ২ ---
প্রশ্ন: তুমি কে?
টুল লাগবে? False
{'question': 'তুমি কে?', 'need_tool': False, 'answer': 'এটি সাধারণ প্রশ্ন, টুল লাগে না।'}
```

### কোন অংশ কী কাজ করে

| অংশ | কাজ |
|---|---|
| `decide` | খাতায় `need_tool` লেখে |
| `router(state)` | শুধু একটি শব্দ ফেরত দেয় — `"yes"` বা `"no"` |
| `add_conditional_edges(...)` | কোন শব্দে কোন নোডে যাবে তার তালিকা |
| `{"yes": "use_tool", "no": "answer"}` | শব্দ → নোডের নাম |
| `add_edge("use_tool", END)` | দুই পথই শেষে মেলে |

`router` নিজে কোনো কাজ করে না — সে শুধু **পথ বেছে দেয়**। এজেন্টের ভাষায় এটাই "টুল লাগবে কি না" সিদ্ধান্ত।

**ছোট কাজ:** শর্তটা বদলে `"কে"` শব্দ খুঁজুন — উল্টো পথে যায় কি না দেখুন।

---

# পাঠ ৪ — লুপ: একই নোডে ফেরা

এজেন্টের লুপ এখানে এজ হয়: শর্ত পূরণ হলে একই নোডে ফিরে যায়।

```
        ┌──── again ────┐
        ▼               │
START ──▶ work ──────────┘
           │
           └── done ──▶ END
```

**ফাইল:** `langgraph-basics/04_loop.py`

```python
import operator
import sys
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph

sys.stdout.reconfigure(encoding="utf-8")


class State(TypedDict):
    count: int
    log: Annotated[list[str], operator.add]


def work(state):
    count = state["count"] + 1
    print("কাজ চলছে — ধাপ", count)
    return {"count": count, "log": [f"ধাপ {count}"]}


def keep_going(state):
    if state["count"] < 3:
        return "again"
    return "done"


builder = StateGraph(State)
builder.add_node("work", work)
builder.add_edge(START, "work")
builder.add_conditional_edges(
    "work",
    keep_going,
    {"again": "work", "done": END},
)

graph = builder.compile()

result = graph.invoke({"count": 0, "log": []})
print("--- শেষ ফল ---")
print(result)
```

**চালান:**

```bash
python langgraph-basics/04_loop.py
```

**ফলাফল:**

```
কাজ চলছে — ধাপ 1
কাজ চলছে — ধাপ 2
কাজ চলছে — ধাপ 3
--- শেষ ফল ---
{'count': 3, 'log': ['ধাপ 1', 'ধাপ 2', 'ধাপ 3']}
```

### কোন অংশ কী কাজ করে

| অংশ | কাজ |
|---|---|
| `count = state["count"] + 1` | প্রতিবার এক বাড়ে |
| `keep_going` | ৩-এর কম হলে `"again"` |
| `{"again": "work"}` | **একই নোডে ফেরা** — এটাই লুপ |
| `{"done": END}` | থামার পথ |
| `log` + `operator.add` | প্রতিটি ধাপের হিসাব জমা থাকে |

লুপ থামে কারণ **শর্ত** থামায় — `count` ৩ হলে `"done"` আসে। শর্ত না থাকলে LangGraph নিজেই একটা সীমা মানে থামিয়ে দেয় (`recursion_limit`, ডিফল্ট ২৫) — কিন্তু ভরসা করবেন না, নিজের শর্ত লিখুন।

**ছোট কাজ:** `< 3` বদলে `< 5` করুন।

---

# পাঠ ৫ — মেমোরি: চেকপয়েন্টার

এখন পর্যন্ত প্রতিবার `invoke` নতুন খাতা দিয়ে শুরু। চেকপয়েন্টার দিলে আগের ফল মনে থাকে।

**ফাইল:** `langgraph-basics/05_memory.py`

```python
import operator
import sys
from typing import Annotated, TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

sys.stdout.reconfigure(encoding="utf-8")


class State(TypedDict):
    name: str
    notes: Annotated[list[str], operator.add]


def note(state):
    return {"notes": [f"{state['name']} এসেছে"]}


builder = StateGraph(State)
builder.add_node("note", note)
builder.add_edge(START, "note")
builder.add_edge("note", END)

graph = builder.compile(checkpointer=MemorySaver())

config = {"configurable": {"thread_id": "মিতু"}}

graph.invoke({"name": "মিতু", "notes": []}, config)
print("প্রথমবার:", graph.get_state(config).values)

graph.invoke({}, config)
print("দ্বিতীয়বার:", graph.get_state(config).values)
```

**চালান:**

```bash
python langgraph-basics/05_memory.py
```

**ফলাফল:**

```
প্রথমবার: {'name': 'মিতু', 'notes': ['মিতু এসেছে']}
দ্বিতীয়বার: {'name': 'মিতু', 'notes': ['মিতু এসেছে', 'মিতু এসেছে']}
```

### কোন অংশ কী কাজ করে

| অংশ | কাজ |
|---|---|
| `MemorySaver()` | চেকপয়েন্টার — ফল মেমোরিতে রাখে |
| `compile(checkpointer=...)` | গ্রাফকে বললাম "ফল মনে রাখো" |
| `thread_id` | কোন কথোপকথনের মেমোরি — নাম/আইডি |
| `invoke({}, config)` | নতুন কিছু না দিয়ে আগের খাতা দিয়ে চালানো |
| `get_state(config)` | সেই থ্রেডের জমানো খাতা দেখা |
| `.values` | খাতার আসল dict |

দ্বিতীয়বার `{}` পাঠানো হয়েছে, কিন্তু `name` আগের থেকেই ছিল — তাই নোড কাজ করতে পেরেছে।

> `MemorySaver` শুধু **প্রোগ্রাম চলার সময়** মনে রাখে; বন্ধ করলে মুছে যায়। আলাদা `thread_id` মানে আলাদা মেমোরি।

**ছোট কাজ:** দ্বিতীয়বার `thread_id` বদলে `"রাফি"` দিন — কী ঘটে? (মনে রাখবেন `name` তখন খালি)

---

# পাঠ ৬ — থামানো ও চালু করা

কিছু কাজের আগে মানুষের অনুমতি লাগে। LangGraph-এ `interrupt()` গ্রাফকে মাঝপথে থামায়; পরে `Command(resume=...)` দিয়ে আবার চালানো যায়।

```
START ──▶ ask (এখানে থামে) ──▶ finish ──▶ END
                    ▲
              resume="y"
```

**ফাইল:** `langgraph-basics/06_interrupt.py`

```python
import sys
from typing import TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

sys.stdout.reconfigure(encoding="utf-8")


class State(TypedDict):
    approved: bool
    result: str


def ask(state):
    answer = interrupt("রিপোর্ট লেখা হবে? (y/n)")
    print("ইউজার বলল:", answer)
    return {"approved": answer == "y"}


def finish(state):
    if state["approved"]:
        return {"result": "রিপোর্ট লেখা হয়েছে।"}
    return {"result": "রিপোর্ট লেখা হয়নি।"}


builder = StateGraph(State)
builder.add_node("ask", ask)
builder.add_node("finish", finish)
builder.add_edge(START, "ask")
builder.add_edge("ask", "finish")
builder.add_edge("finish", END)

graph = builder.compile(checkpointer=MemorySaver())

config = {"configurable": {"thread_id": "রিপোর্ট"}}

graph.invoke({"approved": False}, config)
print("গ্রাফ থেমেছে। পরের নোড:", graph.get_state(config).next)

result = graph.invoke(Command(resume="y"), config)
print("চূড়ান্ত ফল:", result)
```

**চালান:**

```bash
python langgraph-basics/06_interrupt.py
```

**ফলাফল:**

```
গ্রাফ থেমেছে। পরের নোড: ('ask',)
ইউজার বলল: y
চূড়ান্ত ফল: {'approved': True, 'result': 'রিপোর্ট লেখা হয়েছে।'}
```

### কোন অংশ কী কাজ করে

| অংশ | কাজ |
|---|---|
| `interrupt("...")` | এখানেই থামে, প্রশ্নটা বাইরে দেয় |
| `get_state(config).next` | কোন নোডে থেমেছে — `('ask',)` |
| `Command(resume="y")` | "এই উত্তর নিয়ে আবার চালাও" |
| `answer = interrupt(...)` | resume-এর মানটাই `answer`-এ ঢোকে |
| `MemorySaver` | না থাকলে থেমে যাওয়া গ্রাফ আবার চালানো যেত না |

`interrupt` কিন্তু প্রশ্ন প্রিন্ট করে না — মানটা ফেরত দেয়। প্রিন্ট করতে চাইলে নিজে করতে হয়। এখানে Phase 5-এর মতো `Command(resume="y")` হার্ডকোড করা হয়েছে; আসল প্রজেক্টে এটা ইউজারের `input()` থেকে আসে।

**ছোট কাজ:** `"n"` দিয়ে চালান — ফল বদলায় কি না দেখুন।

---

## LangGraph আর নিজের লুপ — তুলনা

| কাজ | Phase 3 (নিজে) | LangGraph |
|---|---|---|
| খাতা | `messages` | `State` (TypedDict) |
| কাজের ধাপ | `for step in range(...)` | Node |
| ক্রম | কোডের লাইন | Edge |
| শর্ত | `if` | `add_conditional_edges` |
| লুপ | `while` / `for` | এজ দিয়ে ফেরা |
| মেমোরি | `messages` লিস্ট | Checkpointer + `thread_id` |
| অনুমতি | `input()` মাঝপথে | `interrupt` + `Command(resume=...)` |

**কখন কোনটা:**

- **শিখতে** — নিজের লুপ (Phase 3)। প্রতিটি লাইন চোখের সামনে।
- **জটিল বহু-ধাপ কাজ** — LangGraph। গ্রাফের ছবি দেখে বোঝা যায়, থামানো-চালানো সহজ।

---

## Phase 5-এ এগুলো কোথায় আছে

[Research Buddy](../04-research-buddy/README.md)-র গ্রাফ:

```
plan ──▶ search ──▶ summarize ──▶ critique ──▶ (যথেষ্ট?) ──▶ approve ──▶ write
                                    │
                                    └── না হলে ──▶ revise ──▶ search
```

| এখানে শেখা | Phase 5-এ |
|---|---|
| নোড | `plan_node`, `search_node`, ... |
| শর্ত | `next_step(state)` — যথেষ্ট কি না |
| লুপ | `revise` → `search` |
| reducer | `search_log: Annotated[list, operator.add]` |
| চেকপয়েন্টার | `MemorySaver` + `thread_id` |
| interrupt | `approve_node` — রিপোর্ট লেখার অনুমতি |

---

## ৬টি অনুশীলন

1. `01`-এ দ্বিতীয় নোড যোগ করুন — `bye`।
2. `02`-এ `steps`-এ reducer না দিয়ে চালান — কী হারায় দেখুন।
3. `03`-এ তৃতীয় পথ যোগ করুন — প্রশ্নে "হিসাব" থাকলে `calculator` নোড।
4. `04`-এ লুপ ৫ বার করুন, তারপর `recursion_limit` ছোট করে দেখুন কী error আসে।
5. `05`-এ দুই `thread_id` দিয়ে আলাদা ফল দেখান।
6. `06`-এ `input()` দিয়ে y/n নিন।

---

## সমস্যা হলে

| যা দেখছেন | সমাধান |
|---|---|
| `ModuleNotFoundError: langgraph` | `.venv` চালু করুন; `pip install -r 00-setup/requirements.txt` |
| `GraphRecursionError` | লুপ থামানোর শর্ত ঠিক করুন |
| `invoke` ফল দিল না, শুধু থেমে গেল | `interrupt` আছে — `Command(resume=...)` দিয়ে চালান |
| `KeyError: '...'` | `State`-এ ঘরটা যোগ করুন; নোডের return-ও মিলান |
| মেমোরি কাজ করছে না | `checkpointer` আছে? একই `thread_id` দিয়েছেন? |
| `steps`-এ আগের মান মুছে যাচ্ছে | `Annotated[list, operator.add]` দিন |

---

## শেষ চেকলিস্ট

- [ ] ৬টি ফাইল চালিয়েছেন
- [ ] State, Node, Edge, Graph — চারটার কাজ বলতে পারেন
- [ ] নোড কেন পুরো খাতা ফেরত দেয় না — বলতে পারেন
- [ ] `operator.add` (reducer) কেন লাগে বলতে পারেন
- [ ] শর্ত দিয়ে দুই পথ বানিয়েছেন
- [ ] লুপ কীভাবে থামে বলতে পারেন
- [ ] `thread_id` আর চেকপয়েন্টারের কাজ বলতে পারেন
- [ ] `interrupt` → `Command(resume=...)` নিজে চালিয়েছেন

---

## পরের ধাপ

Phase 5 — **Research Buddy** (ফোল্ডার: [`04-research-buddy`](../04-research-buddy/README.md))।
এখানে শেখা গ্রাফের ভিতরে আসল LLM, Wikipedia সার্চ, আর নিজে লেখা রিপোর্ট বসানো হয়েছে।
