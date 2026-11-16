# CrewAI বেসিক (সহজ গাইড)

> **লক্ষ্য:** Phase 3-এ নিজে যে agent loop লিখেছিলেন, সেটাই এখন একটি রেডিমেড ফ্রেমওয়ার্ক দিয়ে — কম কোডে।
> **সময়:** ২–৩ দিন, দিনে ৩০–৬০ মিনিট।

---

## আগে যা জানা থাকা ভালো

- [Phase 0](../00-setup/README.md) — `.env`, প্রথম LLM কল
- [Phase 3](../02-weather-agent/README.md) — টুল আর agent loop

CrewAI ম্যাজিক নয়। ভিতরে সেই একই লুপ: **মডেল → টুল/কাজ → ফল → মডেল**। শুধু লুপটা আর নিজে লিখতে হয় না।

---

## কোন Python লাগবে

CrewAI-র সর্বশেষ ভার্সন এখন **Python 3.10–3.13** চায়। 3.14-এ চলবে না।

এই মেশিনে দুটো Python আছে:

- Python **3.14** → পুরোনো `.venv` (Phase 0–5 চলবে)
- Python **3.12** → নতুন `.venv-crewai` (শুধু CrewAI)

প্রথমে একবার নতুন পরিবেশ বানান:

```bash
cd C:\Users\olee\Desktop\ai-agent
py -3.12 -m venv .venv-crewai
source .venv-crewai/Scripts/activate
pip install -r crewai-basics/requirements.txt
```

> প্রথম ইনস্টলে ৩–৫ মিনিট লাগতে পারে। একবারই লাগবে।

এরপর **প্রতিবার** CrewAI চালানোর আগে:

```bash
source .venv-crewai/Scripts/activate
```

Phase 0–5-এর কাজে আবার আগের `.venv`:

```bash
source .venv/Scripts/activate
```

দুটো আলাদা — একটাতে activate করলে অন্যটা বন্ধ হয়ে যায়।

---

## CrewAI-র ৪টি জিনিস

| জিনিস | কী | Phase 3-এ এর সমতুল্য |
|---|---|---|
| `Agent` | কে কাজ করবে — role, goal, backstory | `system.md` + মডেল |
| `Task` | কী কাজ, কেমন ফল চাই (`expected_output`) | আপনার প্রশ্ন + `TOOLS` |
| `Crew` | কে কোন কাজ করবে, কোন ক্রমে | আপনার `while` + `for` লুপ |
| `kickoff()` | দলকে শুরু করা | প্রশ্ন পাঠানো |

CrewAI নিজেই মডেলকে ডাকে, টুল চালায়, ফল ফেরত দেয়, শেষে উত্তর দেয়। আমরা শুধু **কে, কী, কোন ক্রমে** ঠিক করি।

---

## এই ফোল্ডারে কী আছে

| ফাইল | কী শেখাবে |
|---|---|
| `01_first_crew.py` | এক এজেন্ট, এক কাজ — সবচেয়ে ছোট crew |
| `02_two_tasks.py` | এক এজেন্ট, দুই কাজ — আগের কাজের ফল পরের কাজে |
| `03_two_agents.py` | দুই এজেন্ট — লেখক, তারপর সম্পাদক |
| `04_tool.py` | নিজের টুল — ফাইল পড়া |
| `05_team.py` | পুরো টিম + ফলাফল ফাইলে সেভ |
| `office_note.txt` | পাঠ ৪–৫-এ পড়ার নোট |
| `requirements.txt` | CrewAI ইনস্টলের তালিকা |

---

## প্রতি ফাইলের শুরুতে একই সেটআপ

পাঁচটি ফাইলের প্রথম অংশ হুবহু এক:

```python
import os
import sys
from pathlib import Path

from crewai import Agent, Crew, LLM, Process, Task
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv(Path(__file__).parent.parent / "00-setup" / ".env")
os.environ["NO_PROXY"] = "localhost,127.0.0.1"

llm = LLM(
    model=f"openai/{os.getenv('LLM_MODEL')}",
    base_url=os.getenv("LLM_BASE_URL"),
    api_key=os.getenv("LLM_API_KEY"),
)
```

### কোন অংশ কী কাজ করে

| অংশ | কাজ |
|---|---|
| `load_dotenv(...)` | `00-setup/.env` থেকে key, model, base URL আনা |
| `os.environ["NO_PROXY"] = ...` | ভাঙা `NO_PROXY` এড়িয়ে সরাসরি সংযোগ |
| `LLM(...)` | CrewAI-র মডেল সেটিং |
| `openai/` prefix | OpenRouter-কে OpenAI-র মতো ব্যবহার করা |
| `base_url` | OpenRouter-এর ঠিকানা |
| `api_key` | `.env`-এর key |

> `NO_PROXY` লাইনটা কেন? কিছু Windows সেটিংয়ে `NO_PROXY`-তে `[::1]` থাকে; সেটা পড়তে গিয়ে httpx `Invalid port` error দেয়। এই লাইনটা নিরাপদ মান বসিয়ে দেয়।

> এখানে কোনো key লেখা নেই — সবই `.env` থেকে আসে।

---

# পাঠ ১ — প্রথম crew

**ফাইল:** `crewai-basics/01_first_crew.py`

```python
import os
import sys
from pathlib import Path

from crewai import Agent, Crew, LLM, Process, Task
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv(Path(__file__).parent.parent / "00-setup" / ".env")
os.environ["NO_PROXY"] = "localhost,127.0.0.1"

llm = LLM(
    model=f"openai/{os.getenv('LLM_MODEL')}",
    base_url=os.getenv("LLM_BASE_URL"),
    api_key=os.getenv("LLM_API_KEY"),
)

writer = Agent(
    role="অফিস লেখক",
    goal="কর্মীদের জন্য ছোট ও পরিষ্কার বাংলা লেখা",
    backstory="তুমি Little Office Ltd.-এর অভিজ্ঞ লেখক।",
    llm=llm,
    verbose=True,
)

memo = Task(
    description="আগামীকাল অফিস বন্ধ থাকবে — এ নিয়ে কর্মীদের জন্য ৩ বাক্যের একটি বাংলা নোটিশ লেখো।",
    expected_output="৩ বাক্যের বাংলা নোটিশ।",
    agent=writer,
)

crew = Crew(
    agents=[writer],
    tasks=[memo],
    process=Process.sequential,
    verbose=True,
    tracing=False,
)

print("\n--- শুরু ---")
result = crew.kickoff()
print("\n--- চূড়ান্ত ফল ---")
print(result)
```

**চালান:**

```bash
source .venv-crewai/Scripts/activate
python crewai-basics/01_first_crew.py
```

**ফলাফল:** CrewAI নিজেই ধাপে ধাপে লগ দেখায় (কারা কাজ করছে, কী ভাবছে), শেষে বাংলা নোটিশ দেয়। লগ অনেক লম্বা — শেষের অংশ এমন:

```
--- চূড়ান্ত ফল ---
সকল কর্মীদের জানানো যাচ্ছে যে, আগামীকাল (তারিখ) সারাদিন অফিস বন্ধ থাকবে। জরুরি কর্ম থাকলে ইমেইল
বা ফোনে যোগাযোগ করুন। বাকি সবাই পরের কাজের দিনে নিয়মিত উপস্থিত থাকবেন।
```

### কোন অংশ কী কাজ করে

| অংশ | কাজ |
|---|---|
| `Agent(role=...)` | এজেন্টের পরিচয় — "অফিস লেখক" |
| `goal=...` | তার মূল লক্ষ্য |
| `backstory=...` | পেছনের গল্প — মডেলের সুর ঠিক করে |
| `llm=llm` | কোন মডেল ব্যবহার করবে |
| `verbose=True` | ধাপে ধাপে লগ দেখায় |
| `Task(description=...)` | আসল কাজের নির্দেশ |
| `expected_output=...` | কেমন ফল চাই — মডেলকে বাঁধা দেয় |
| `agent=writer` | এই কাজ কে করবে |
| `Crew(agents=[...], tasks=[...])` | দল ও কাজের তালিকা |
| `Process.sequential` | একের পর এক কাজ |
| `tracing=False` | শেষে trace শেয়ার করার প্রশ্ন বন্ধ |
| `crew.kickoff()` | কাজ শুরু — শেষে ফল ফেরত দেয় |

> `tracing=False` না দিলে CrewAI শেষে জিজ্ঞেস করে "trace শেয়ার করবেন?" এবং ২০ সেকেন্ড অপেক্ষা করে। শেখার সময় সেটা দরকার নেই।

**ছোট কাজ:** `goal` আর `backstory` বদলে আবার চালান — লেখার সুর বদলায় কি না দেখুন।

---

# পাঠ ২ — এক এজেন্ট, দুই কাজ

একজনই লেখক, কিন্তু কাজ দুই ধাপে: আগে খসড়া, পরে নোটিশ।

**ফাইল:** `crewai-basics/02_two_tasks.py`

```python
import os
import sys
from pathlib import Path

from crewai import Agent, Crew, LLM, Process, Task
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv(Path(__file__).parent.parent / "00-setup" / ".env")
os.environ["NO_PROXY"] = "localhost,127.0.0.1"

llm = LLM(
    model=f"openai/{os.getenv('LLM_MODEL')}",
    base_url=os.getenv("LLM_BASE_URL"),
    api_key=os.getenv("LLM_API_KEY"),
)

writer = Agent(
    role="অফিস লেখক",
    goal="কর্মীদের জন্য ছোট ও পরিষ্কার বাংলা লেখা",
    backstory="তুমি Little Office Ltd.-এর অভিজ্ঞ লেখক।",
    llm=llm,
    verbose=True,
)

outline = Task(
    description="কর্মীদের জন্য 'সাপ্তাহিক মিটিং' নিয়ে ৩টি পয়েন্টের খসড়া বাংলায় লেখো।",
    expected_output="৩টি সংক্ষিপ্ত পয়েন্ট।",
    agent=writer,
)

notice = Task(
    description="আগের খসড়ার ৩টি পয়েন্ট নিয়ে ৪ বাক্যের একটি পরিষ্কার বাংলা নোটিশ লেখো।",
    expected_output="৪ বাক্যের বাংলা নোটিশ।",
    agent=writer,
    context=[outline],
)

crew = Crew(
    agents=[writer],
    tasks=[outline, notice],
    process=Process.sequential,
    verbose=True,
    tracing=False,
)

print("\n--- শুরু ---")
result = crew.kickoff()
print("\n--- চূড়ান্ত ফল ---")
print(result)
```

### কোন অংশ কী কাজ করে

| অংশ | কাজ |
|---|---|
| `outline` | প্রথম কাজ — খসড়া |
| `notice` | দ্বিতীয় কাজ — চূড়ান্ত নোটিশ |
| `context=[outline]` | দ্বিতীয় কাজ **প্রথম কাজের ফল পড়বে** |
| `tasks=[outline, notice]` | ক্রম: আগে খসড়া, পরে নোটিশ |

`context` না দিলে মডেল আগের কাজের ফল নাও পেতে পারে। দেওয়াই নিরাপদ।

**ছোট কাজ:** `notice`-এ "৩ বাক্য" করুন — ফল কি ছোট হয়?

---

# পাঠ ৩ — দুই এজেন্ট

এখন দুইজন: লেখক লিখবে, সম্পাদক ঠিক করবে।

**ফাইল:** `crewai-basics/03_two_agents.py`

```python
import os
import sys
from pathlib import Path

from crewai import Agent, Crew, LLM, Process, Task
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv(Path(__file__).parent.parent / "00-setup" / ".env")
os.environ["NO_PROXY"] = "localhost,127.0.0.1"

llm = LLM(
    model=f"openai/{os.getenv('LLM_MODEL')}",
    base_url=os.getenv("LLM_BASE_URL"),
    api_key=os.getenv("LLM_API_KEY"),
)

writer = Agent(
    role="অফিস লেখক",
    goal="কর্মীদের জন্য ছোট ও পরিষ্কার বাংলা লেখা",
    backstory="তুমি Little Office Ltd.-এর অভিজ্ঞ লেখক।",
    llm=llm,
    verbose=True,
)

editor = Agent(
    role="বাংলা সম্পাদক",
    goal="লেখার বানান, বাক্য ও স্পষ্টতা ঠিক করা",
    backstory="তুমি বাংলা ভাষার সম্পাদক। লেখা ছোট ও স্পষ্ট করতে জানো।",
    llm=llm,
    verbose=True,
)

draft = Task(
    description="কর্মীদের জানাও যে ২০ নভেম্বর সকাল ১০টায় টিম মিটিং হবে। ১০ লাইনের মধ্যে আনুষ্ঠানিক বাংলা নোটিশ লেখো।",
    expected_output="একটি বাংলা মিটিং নোটিশ।",
    agent=writer,
)

checked = Task(
    description="আগের নোটিশটি পড়ো। বানান ও বাক্য ঠিক করো। চূড়ান্ত নোটিশটি পুরোটা লেখো, তার নিচে আলাদা লাইনে 'সম্পাদিত' লেখো।",
    expected_output="সম্পাদিত ও পরিষ্কার বাংলা নোটিশ।",
    agent=editor,
    context=[draft],
)

crew = Crew(
    agents=[writer, editor],
    tasks=[draft, checked],
    process=Process.sequential,
    verbose=True,
    tracing=False,
)

print("\n--- শুরু ---")
result = crew.kickoff()
print("\n--- চূড়ান্ত ফল ---")
print(result)
```

### কোন অংশ কী কাজ করে

| অংশ | কাজ |
|---|---|
| `writer` | প্রথম এজেন্ট — লিখবে |
| `editor` | দ্বিতীয় এজেন্ট — ঠিক করবে |
| `agent=writer` / `agent=editor` | কোন কাজ কে করবে |
| `context=[draft]` | সম্পাদক লেখকের ফল পাবে |
| `agents=[writer, editor]` | দুইজনই দলে আছে |

খেয়াল করুন: **একই `llm`, আলাদা role**। ভূমিকা বদলালে মডেলের আচরণও বদলায়।

---

# পাঠ ৪ — নিজের টুল

Phase 3-এ টুল ছিল JSON বর্ণনা + function। CrewAI-তে সেটা ছোট: `@tool` লাগান, তারপর `tools=[...]`।

**ফাইল:** `crewai-basics/04_tool.py`

```python
import os
import sys
from pathlib import Path

from crewai import Agent, Crew, LLM, Process, Task
from crewai.tools import tool
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv(Path(__file__).parent.parent / "00-setup" / ".env")
os.environ["NO_PROXY"] = "localhost,127.0.0.1"

llm = LLM(
    model=f"openai/{os.getenv('LLM_MODEL')}",
    base_url=os.getenv("LLM_BASE_URL"),
    api_key=os.getenv("LLM_API_KEY"),
)


@tool("read_office_note")
def read_office_note() -> str:
    """অফিসের নোট ফাইলটি পড়ে লেখা ফেরত দেয়।"""
    note = Path(__file__).parent / "office_note.txt"
    return note.read_text(encoding="utf-8")


reader = Agent(
    role="নোট পাঠক",
    goal="অফিসের নোট পড়ে মূল কথা বের করা",
    backstory="তুমি ফাইল পড়ে সংক্ষেপে সারমর্ম বলতে পারো।",
    tools=[read_office_note],
    llm=llm,
    verbose=True,
)

summary = Task(
    description="read_office_note টুল দিয়ে অফিসের নোটটি পড়ো। তারপর ৩টি বুলেটে মূল কথা বাংলায় লেখো।",
    expected_output="৩টি বাংলা বুলেট।",
    agent=reader,
)

crew = Crew(
    agents=[reader],
    tasks=[summary],
    process=Process.sequential,
    verbose=True,
    tracing=False,
)

print("\n--- শুরু ---")
result = crew.kickoff()
print("\n--- চূড়ান্ত ফল ---")
print(result)
```

**চালান:**

```bash
python crewai-basics/04_tool.py
```

**ফলাফল (লম্বা লগের শেষে):**

```
- ২০ নভেম্বর সকাল ১০টায় টিম মিটিং নির্ধারিত আছে।
- নতুন কাস্টমার রিপোর্ট শুক্রবার তারিখের মধ্যে জমা দিতে হবে।
- অফিসের ইন্টারনেট সংযোগ বুধবার বিকেলে মেরামতের জন্য বন্ধ থাকবে।
```

### কোন অংশ কী কাজ করে

| অংশ | কাজ |
|---|---|
| `@tool("read_office_note")` | function-কে টুল বানায় |
| `"""..."""` | টুলের বর্ণনা — মডেল **এটাই পড়ে** |
| `tools=[read_office_note]` | এজেন্টকে টুলটি দেয় |
| `Path(__file__).parent` | ফাইলটা এই ফোল্ডারেই খোঁজে |
| `.read_text(...)` | ফাইলের লেখা পড়ে |

CrewAI নিজেই মডেলকে টুলের তালিকা দেখায়, মডেল চাইলে টুল চালায়, ফল ফেরত দেয় — Phase 3-এর `TOOLS` + `run_tool` + লুপ, সব একসাথে।

**ছোট কাজ:** `office_note.txt`-এ নিজের এক লাইন যোগ করুন, আবার চালান।

---

# পাঠ ৫ — পুরো টিম + ফাইলে সেভ

শেষ ধাপ: নোট পাঠক + লেখক মিলে কাজ করবে, ফলাফল `notice.md`-তে সেভ হবে।

**ফাইল:** `crewai-basics/05_team.py`

```python
import os
import sys
from pathlib import Path

from crewai import Agent, Crew, LLM, Process, Task
from crewai.tools import tool
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv(Path(__file__).parent.parent / "00-setup" / ".env")
os.environ["NO_PROXY"] = "localhost,127.0.0.1"

llm = LLM(
    model=f"openai/{os.getenv('LLM_MODEL')}",
    base_url=os.getenv("LLM_BASE_URL"),
    api_key=os.getenv("LLM_API_KEY"),
)

OUTPUT = Path(__file__).parent / "notice.md"


@tool("read_office_note")
def read_office_note() -> str:
    """অফিসের নোট ফাইলটি পড়ে লেখা ফেরত দেয়।"""
    note = Path(__file__).parent / "office_note.txt"
    return note.read_text(encoding="utf-8")


reader = Agent(
    role="নোট পাঠক",
    goal="অফিসের নোট পড়ে মূল কথা বের করা",
    backstory="তুমি ফাইল পড়ে সংক্ষেপে সারমর্ম বলতে পারো।",
    tools=[read_office_note],
    llm=llm,
    verbose=True,
)

writer = Agent(
    role="অফিস লেখক",
    goal="কর্মীদের জন্য ছোট ও পরিষ্কার বাংলা লেখা",
    backstory="তুমি Little Office Ltd.-এর অভিজ্ঞ লেখক।",
    llm=llm,
    verbose=True,
)

summary = Task(
    description="read_office_note টুল দিয়ে অফিসের নোটটি পড়ো। তারপর ৩টি বুলেটে মূল কথা বাংলায় লেখো।",
    expected_output="৩টি বাংলা বুলেট।",
    agent=reader,
)

notice = Task(
    description="আগের সারমর্ম থেকে কর্মীদের জন্য ৫ বাক্যের একটি বাংলা নোটিশ লেখো।",
    expected_output="৫ বাক্যের বাংলা নোটিশ।",
    agent=writer,
    context=[summary],
    output_file=str(OUTPUT),
)

crew = Crew(
    agents=[reader, writer],
    tasks=[summary, notice],
    process=Process.sequential,
    verbose=True,
    tracing=False,
)

print("\n--- শুরু ---")
result = crew.kickoff()
print("\n--- চূড়ান্ত ফল ---")
print(result)
print("\nসেভ হয়েছে:", OUTPUT)
```

**চালান:**

```bash
source .venv-crewai/Scripts/activate
python crewai-basics/05_team.py
cat crewai-basics/notice.md
```

**ফলাফল (মডেলভেদে লেখা বদলায়):**

```
**নোটিশ**

২০ নভেম্বর সকাল ১০টায় টিম মিটিং অনুষ্ঠিত হবে। সকল কর্মীদের সময়মতো উপস্থিত থাকতে অনুরোধ করা হচ্ছে।
নতুন কাস্টমার রিপোর্ট শুক্রবারের মধ্যে জমা দিতে হবে। বুধবার বিকেলে ইন্টারনেট মেরামতের জন্য বন্ধ থাকবে,
তাই জরুরি কাজ আগেই শেষ করুন। সংযোগ ফিরলে সকলে নিয়মিত কাজ শুরু করবেন।
```

শেষে টার্মিনালে দেখবেন:

```
সেভ হয়েছে: C:\Users\olee\Desktop\ai-agent\crewai-basics\notice.md
```

### কোন অংশ কী কাজ করে

| অংশ | কাজ |
|---|---|
| `OUTPUT = ... / "notice.md"` | কোথায় সেভ হবে |
| `tools=[read_office_note]` | শুধু পাঠকের কাছে টুল |
| `summary` → `notice` | আগে পড়া, পরে লেখা |
| `context=[summary]` | লেখক সারমর্ম পায় |
| `output_file=...` | কাজের ফল ফাইলে সেভ |

> `notice.md` প্রতিবার নতুন করে লেখা হয়। এটা গিটে যায় না (`.gitignore`-এ আছে)।

---

## CrewAI আর নিজের লুপ — তুলনা

| কাজ | Phase 3 (নিজে) | CrewAI |
|---|---|---|
| মডেল ডাকা | `client.chat.completions.create(...)` | ভিতরে নিজেই |
| টুল বাছাই | `message.tool_calls` | নিজেই |
| টুল চালানো | `run_tool(name, args)` | নিজেই |
| মেমোরি | `messages` লিস্ট | নিজেই সামলায় |
| সর্বোচ্চ ধাপ | `range(1, 5)` | `max_iter` |
| টিম বানানো | নিজে লিখতে হয় | `Crew(agents=[...])` |

**কখন কোনটা:**

- **শিখতে** — নিজের লুপ (Phase 3)। ভিতরে কী হচ্ছে বোঝা যায়।
- **দ্রুত কাজ** — CrewAI। কম কোড, রেডিমেড টিম।

---

## ৫টি অনুশীলন

1. `01`-এ `goal` বদলে "আনুষ্ঠানিক" শব্দটা যোগ করুন।
2. `02`-এ তিনটি কাজ করুন — খসড়া → নোটিশ → শিরোনাম।
3. `03`-এ তিন নম্বর এজেন্ট যোগ করুন — "অনুবাদক" (বাংলা → ইংরেজি)।
4. `04`-এ নতুন টুল বানান — `count_lines`, ফাইলের লাইন গুনবে।
5. `05`-এ `output_file` বদলে `notice.txt` করুন।

---

## সমস্যা হলে

| যা দেখছেন | সমাধান |
|---|---|
| `No module named 'crewai'` | `.venv-crewai` activate করেছেন কি? |
| ইনস্টলে `tiktoken`/`regex` build error | Python 3.14-এ হচ্ছে — `py -3.12` দিয়ে নতুন venv |
| `429` | ফ্রি মডেল ব্যস্ত — কিছুক্ষণ পরে চেষ্টা করুন |
| `401` / key error | `00-setup/.env` দেখুন |
| টুল ডাকছে না | Task-এ টুলের নাম লিখেছেন কি? `tools=[...]` আছে কি? |
| আউটপুট খুব লম্বা | `verbose=False` করুন |
| `notice.md` খুঁজে পাচ্ছি না | `crewai-basics/` ফোল্ডারে দেখুন; সফল `kickoff()`-এর পর তৈরি হয় |
| `Invalid port: ':1]'` | `NO_PROXY` ভাঙা — প্রতিটি ফাইলে থাকা `os.environ["NO_PROXY"] = ...` লাইনটা রাখুন |
| বাংলা অক্ষর এলোমেলো / অন্য ভাষার অক্ষর | ফ্রি মডেলের দুর্বলতা — `.env`-এ ভালো মডেল বসিয়ে চেষ্টা করুন |
| প্রতিবার শেষে ২০ সেকেন্ড অপেক্ষা | `Crew(..., tracing=False)` দিন |

---

## শেষ চেকলিস্ট

- [ ] `.venv-crewai` বানিয়ে CrewAI ইনস্টল করেছেন
- [ ] ৫টি ফাইল চালিয়েছেন
- [ ] `Agent`, `Task`, `Crew`-র পার্থক্য বলতে পারেন
- [ ] `context` কী কাজে লাগে বলতে পারেন
- [ ] `@tool` দিয়ে নিজের টুল বানিয়েছেন
- [ ] `notice.md` ফাইলে ফলাফল দেখেছেন
- [ ] বলতে পারেন — CrewAI আর নিজের লুপের পার্থক্য

---

## পরের ধাপ

সিলেবাস অনুযায়ী পরের কাজ **Phase 6 — Skills**: এজেন্টকে নতুন দক্ষতা শেখানো।
বিস্তারিত: [ai-agent-syllabus-bangla.md](../ai-agent-syllabus-bangla.md)।
