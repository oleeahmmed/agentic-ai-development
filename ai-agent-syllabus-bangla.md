# AI Agent মাস্টারি — সম্পূর্ণ বাংলা সিলেবাস

**LangGraph + Hermes Agent + Python + LLM + Skills + Tools + Memory**

> এক লাইনে লক্ষ্য: শূন্য থেকে শুরু করে এমন AI Agent বানানো, যে নিজে টুল ব্যবহার করে, মনে রাখে, শিখে, আর আপনার আসল কাজ করে দেয় — এবং সেটা আপনি নিজেই ডিজাইন করতে পারেন।

---

## ১. এক নজরে

| বিষয় | বিবরণ |
|---|---|
| কার জন্য | প্রোগ্রামিং জানেন না বা একদম শুরুতে আছেন, কিন্তু AI Agent বানাতে চান |
| কত সময় | সপ্তাহে ৮–১০ ঘণ্টা, মোট ১৬ সপ্তাহ (সপ্তাহ ০ সহ) |
| কী লাগবে | একটি ল্যাপটপ, ইন্টারনেট, একটি LLM API key |
| কী শিখবেন | Python, LLM বেসিক, Tool Calling, Memory/RAG, LangGraph, Skill ডিজাইন, Hermes Agent, Evaluation, Deployment |
| কী বানাবেন | ৬টি প্রজেক্ট — Hello Agent → Company Helper |
| শেষে হাতে থাকবে | ৬টি চলমান প্রজেক্ট + যেকোনো কাজকে Agent-এ রূপ দেওয়ার একটি পুনরাবৃত্ত পদ্ধতি |

**এই সিলেবাসের তিনটি নিয়ম**

1. **কোড না লিখে কিছুই শেখা হয় না।** প্রতিটি ফেজে হাতে-কলমে কাজ আছে — সেটা বাদ দেবেন না।
2. **প্রথমে সহজ, পরে শক্ত।** প্রথমে ফ্রেমওয়ার্ক ছাড়া নিজে agent loop লিখবেন। বুঝে গেলে LangGraph ব্যবহার করবেন। এতে "ভেতরে কী ঘটছে" পরিষ্কার থাকবে।
3. **প্রতিটি ফেজ শেষে একটি ডেমো।** চোখ বন্ধ করে নিজের ভাষায় বুঝিয়ে বলতে পারলে তবেই পরের ফেজে যাবেন।

---

## ২. প্রথমে গল্প: "মিতুর প্রথম সপ্তাহ"

কল্পনা করুন, **Little Office Ltd.** নামে একটি ছোট সফটওয়্যার কোম্পানি আছে। ১২ জন কর্মী, ডেস্ক অ্যাকসেসরিজ বিক্রি করে। HR একজন নতুন জুনিয়র নিয়োগ করল — নাম **মিতু**।

মিতু খুব স্মার্ট, বাংলা-ইংরেজি ভালো বোঝে, সাধারণ হিসাব জানে। কিন্তু কোম্পানি সম্পর্কে সে কিছুই জানে না।

**Day 0 — মিতুর নিজের জ্ঞান।**
মিতু জানে "রিফান্ড" কী, "অর্ডার" কী — এগুলো সাধারণ জ্ঞান। কিন্তু কোম্পানির অর্ডার নম্বর, স্টক, কাস্টমারের নাম সে জানে না।
👉 এটাই **LLM-এর pre-trained knowledge**। অনেক জানা, কিন্তু আপনার ব্যবসার কিছুই জানে না।

**Day 1 — বস একটা কাগজ দিল।**
কাগজে লেখা: "তুমি Little Office-এর কাস্টমার সাপোর্ট অ্যাসিস্ট্যান্ট। ভদ্রভাবে উত্তর দেবে, বাংলা বা ইংরেজিতে — কাস্টমার যেভাবে লিখবে। কখনো মিথ্যা প্রতিশ্রুতি দেবে না।"
👉 এটাই **System Prompt**।

**Day 1 বিকেল — বস বলল, "আজ এই তিনটি কাজ করো।"**
👉 এটাই **User message / task**।

**Day 2 — ট্রেনিং ম্যানুয়াল।**
HR দিল ৫ পাতার ম্যানুয়াল: "রিফান্ড রিকোয়েস্ট এলে এই ৫ ধাপে যাচাই করবে। ক্ষতিকর কিছু বললে এইভাবে শান্ত করবে।"
👉 এটাই **Skill** — কাজ করার জ্ঞান ও পদ্ধতি।

**Day 3 — সরঞ্জাম।**
মিতুর হাতে ল্যাপটপ, কোম্পানির ডাটাবেসে লগইন, ইমেইল অ্যাকাউন্ট, ক্যালকুলেটর।
👉 এগুলো **Tools** — বাইরের জগতে কিছু করার ক্ষমতা।

**Day 4 — ডায়েরি।**
মিতু ডায়েরিতে লিখে রাখল: "স্যার চা না, কফি খান", "মাসিক রিপোর্ট ৫ তারিখে জমা দিতে হয়"।
👉 এটাই **Memory**।

**Day 5 — বস বলল, "কোন কেসে কোন ধাপে যাবে, তুমি নিজে ঠিক করো।"**
এক কাস্টমার অর্ডার স্ট্যাটাস চাইছে, আরেকজন রিফান্ড। মিতু নিজেই বুঝে নিল কোন কাজে কোন টুল ব্যবহার করবে, ফলাফল দেখে পরের ধাপ ঠিক করল।
👉 এটাই **Agent / agentic loop** — শুধু উত্তর নয়, সিদ্ধান্ত + কাজ + আবার সিদ্ধান্ত।

**Day 6 — নিয়ম।**
বস বলল: "৫০০ টাকার বেশি রিফান্ড নিজে দিতে পারবে না, আমার অনুমতি নেবে। কাস্টমারকে ইমেইল পাঠানোর আগেও দেখাবে।"
👉 এটাই **Guardrail + Human-in-the-loop**।

**Day 7 — রিপোর্ট।**
বস জিজ্ঞেস করল: "তুমি কী করলে, কোন টুল কখন ব্যবহার করলে, কোথায় আটকালে?"
👉 এটাই **Logging / Tracing**।

**Day 8 — ভুল।**
মিতু পুরনো ডায়েরির তথ্য ব্যবহার করে ভুল উত্তর দিল, কারণ তথ্য পুরনো হয়ে গিয়েছিল। আরেকবার কাস্টমার যা বলেনি, তা ধরে নিয়ে উত্তর বানিয়ে ফেলল।
👉 এটাই **Hallucination, stale memory, context সমস্যা**।

**Day 9 — নতুন দক্ষতা।**
একই কাজ বারবার আসছিল। মিতু নিজেই একটি checklist বানিয়ে ফেলল পরেরবারের জন্য।
👉 এটাই **Skill creation** — Hermes Agent যে কাজটা করে।

এই একটা গল্পেই AI Agent-এর প্রায় সব অংশ ঢুকে গেছে। এখন নামগুলো গুছিয়ে দেখি।

---

## ৩. কোনটা কী — গুলিয়ে যায় যেসব জিনিস

| জিনিস | সহজ কথা | গল্পে | উদাহরণ |
|---|---|---|---|
| **Prompt** | নির্দেশনা | বসের এক লাইনের আদেশ | "ভদ্রভাবে উত্তর দাও" |
| **Skill** | কাজ করার জ্ঞান/পদ্ধতি | ট্রেনিং ম্যানুয়াল | "রিফান্ড যাচাইয়ের ৫ ধাপ" |
| **Tool** | বাইরের ক্ষমতা | ল্যাপটপ, ডাটাবেস, ইমেইল | `get_order("A102")` |
| **Memory** | মনে রাখা | ডায়েরি | "কাস্টমারের নাম রাফি" |
| **Agent** | সিদ্ধান্ত + লুপ | মিতু নিজে | ফলাফল দেখে পরের ধাপ ঠিক করে |
| **RAG** | খুঁজে এনে উত্তর | ফাইল ক্যাবিনেট থেকে নথি বের করা | পলিসি ডকুমেন্ট থেকে উদ্ধৃতি |
| **Guardrail** | নিষেধের সীমানা | বসের নিয়ম | ৫০০ টাকার বেশি রিফান্ড নয় |
| **Eval** | পরীক্ষার খাতা | কাজের মান যাচাই | ২০টি টেস্ট কেস |

**Skill বনাম Tool (সবচেয়ে গুরুত্বপূর্ণ পার্থক্য)**

- **Tool** দেয় *ক্ষমতা*: "আমি ডাটাবেস পড়তে পারি।"
- **Skill** দেয় *জ্ঞান*: "কখন, কেন, কোন ক্রমে ডাটাবেস পড়তে হবে।"

শুধু Tool আছে কিন্তু Skill নেই — এমন কর্মী জানে না কখন কোন টুল ব্যবহার করবে।
শুধু Skill আছে কিন্তু Tool নেই — এমন কর্মী জানে কী করতে হবে, কিন্তু করতে পারে না।

**Chatbot বনাম Agent**

| Chatbot | Agent |
|---|---|
| ইনপুট → উত্তর | ইনপুট → ভাবনা → টুল → ফলাফল → আবার ভাবনা → কাজ → উত্তর |
| কিছু পরিবর্তন করতে পারে না | ফাইল, ডাটাবেস, ইমেইল, API — আসল কাজ করতে পারে |
| এক ধাপ | একাধিক ধাপ, শর্ত অনুযায়ী পথ বদলায় |

**কখন Agent লাগে না**

কাজটির ধাপ যদি আগে থেকেই ফিক্সড হয়, তাহলে সাধারণ Python কোডই ভালো — সস্তা, দ্রুত, নির্ভরযোগ্য।
Agent লাগে যখন: ভাষা বুঝতে হয়, ইনপুট অনিশ্চিত, কোন টুল/ধাপ লাগবে সেটা আগে থেকে বলা যায় না।

> শুরুতে সবসময় সবচেয়ে কম স্বাধীনতা দিয়ে শুরু করুন: fixed chain → router → tool-calling agent → planner/executor → multi-agent। সরাসরি multi-agent দিয়ে শুরু করা নতুনদের সবচেয়ে বড় ভুল।

---

## ৪. যেকোনো কাজকে Agent বানানোর ৭ ধাপ

এই ৭টি প্রশ্নই আপনার "ডিজাইন ক্যানভাস"। ভবিষ্যতে যে কাজই আসুক, এই ৭ ধাপে ভাঙুন।

1. **কাজটা স্পষ্ট করে লেখা** — ইনপুট কী, আউটপুট কী, সফলতা কীভাবে মাপবেন।
2. **সিদ্ধান্তের তালিকা** — কোন কোন জায়গায় এজেন্টকে *ভাবতে* হবে (শাখা/শর্ত)।
3. **Tool তালিকা** — কোন তথ্য/অ্যাকশন লাগবে। প্রথমে শুধু read-only টুল; write/destructive টুল পরে।
4. **Skill/Policy লেখা** — নিয়ম, টোন, ধাপ, নিষেধ, ব্যর্থ হলে কী করবে।
5. **Memory দরকার কি?** — কী মনে রাখতে হবে, কতদিন, কে দেখতে পারবে।
6. **গ্রাফ আঁকা** — বাক্স ও তীর: START → কোন নোড → কোন শর্তে কোথায় → END। মানুষের অনুমতি কোথায় লাগবে।
7. **Eval সেট** — ২০টি টেস্ট কেস, যার ৫টি ভুল/প্রতারক ইনপুট। না থাকলে "কাজ করছে" মনে হবে, কিন্তু কাজ করবে না।

**উদাহরণ: "ইমেইলে আসা অর্ডার স্ট্যাটাস প্রশ্নের উত্তর দেওয়া"**

- ইনপুট: কাস্টমারের ইমেইল। আউটপুট: সঠিক তথ্যসহ ভদ্র উত্তর, অথবা মানুষের কাছে escalate।
- সিদ্ধান্ত: অর্ডার নাম্বার আছে? কাস্টমার শনাক্ত হলো? প্রশ্নটা স্ট্যাটাস না রিফান্ড?
- Tools: `find_customer`, `get_order`, `send_email` (approval সহ)।
- Skill: সাপোর্ট টোন + রিফান্ড পলিসি + escalate নিয়ম।
- Memory: কাস্টমারের নাম, আগের টিকিট।
- Graph: intake → classify → tool loop → policy check → (approval?) → reply।
- Eval: সঠিক অর্ডার, ভুল অর্ডার, অন্য কাস্টমারের তথ্য চাওয়া, "ignore previous instructions", রিফান্ড দাবি।

---

## ৫. প্রজেক্ট রোডম্যাপ

| # | প্রজেক্ট | কী শিখবে | মূল ফিচার | মূল টেক |
|---|---|---|---|---|
| 1 | **Hello Agent** | LLM, prompt, conversation | পার্সোনা + কথোপকথন মনে রাখা | Python + LLM API |
| 2 | **Weather Agent** | Tool calling, agent loop | আবহাওয়া/ফোরকাস্ট টুল, সঠিক আর্গুমেন্ট | নিজের লেখা loop + Open-Meteo |
| 3 | **Memory Friend** | Memory, embedding, RAG | পছন্দ মনে রাখে, restart-এর পরেও | SQLite/JSON → vector store |
| 4 | **Research Buddy** | LangGraph | খোঁজে, সারাংশ দেয়, রিভাইজ করে, সোর্স দেয় | LangGraph + search API |
| 5 | **Skill Creator** | Skill ডিজাইন, Hermes | অভিজ্ঞতা থেকে নতুন SKILL.md বানায় | Hermes Agent / LangGraph |
| 6 | **Company Helper** | পুরো সিস্টেম একসাথে | অর্ডার চেক, রিফান্ড পলিসি, ইমেইল approval, escalate | LangGraph + skills + memory + eval |

প্রতিটি প্রজেক্ট আগেরটার উপর দাঁড়ায়। তাই ক্রম বদলাবেন না।

---

## ৬. ফেজ-বাই-ফেজ সিলেবাস

### Phase 0 — পরিবেশ তৈরি (৩–৪ দিন)

**লক্ষ্য:** কোড লেখা ও API চালানোর পরিবেশ ঠিক করা।

- Python 3.12+ ইনস্টল, `python --version` দিয়ে যাচাই
- ভার্চুয়াল এনভায়রনমেন্ট: `python -m venv .venv` (Git Bash: `source .venv/Scripts/activate`)
- VS Code + Python extension; ফাইল চালানো ও ডিবাগ করা
- Git + GitHub অ্যাকাউন্ট, প্রথম commit ও push
- LLM API key: OpenRouter (এক জায়গায় অনেক মডেল), Google AI Studio (ফ্রি টিয়ার), বা OpenAI — যেটা সুবিধা
- `.env` ফাইলে key রাখা, `.gitignore`-এ `.env` যোগ করা, `python-dotenv` দিয়ে পড়া
- প্রথম স্ক্রিপ্ট: API-তে "তুমি কে?" পাঠিয়ে উত্তর প্রিন্ট

**শেষ করার মানদণ্ড:** টার্মিনাল থেকে একটি LLM কল সফলভাবে চলে; key কোডে হার্ডকোড করা নেই; রিপো repo-তে push হয়েছে।

> API key = অফিসের আইডি কার্ড + ওয়ালেট। কাউকে দেবেন না, কোডে লিখে commit করবেন না। লিক হলে কেউ আপনার টাকায় কল চালাবে।

---

### Phase 1 — Python: যতটুকু দরকার, ঠিক ততটুকু (২ সপ্তাহ)

**লক্ষ্য:** Agent বানানোর জন্য প্রয়োজনীয় Python — এর বেশি নয়।

- ভেরিয়েবল, টাইপ, f-string, input/print
- list, dict, loop, if/else — ডেটা নিয়ে কাজ
- function: প্যারামিটার, return, scope
- module ও `pip`/`uv` দিয়ে প্যাকেজ
- ফাইল পড়া/লেখা, `pathlib`, JSON read/write
- `try/except`, error message পড়া, বেসিক logging
- class — শুধু ডেটা + মেথড বোঝার জন্য
- type hint, `dataclass`, Pydantic-এর প্রথম পরিচয়
- HTTP API কল (`httpx` বা `requests`), status code, JSON response
- `async/await` — ধারণা মাত্র (streaming-এ লাগবে)

**হাতে-কলমে:** JSON ফাইলে টাস্ক সেভ ও লিস্ট করার CLI — আপনার `ai-mini-office`-এর `tools.py`-র মতো, তবে নিজে লিখে, error handling সহ।

**শেষ করার মানদণ্ড:** একটি ফ্রি API (যেমন Open-Meteo) থেকে ডেটা এনে JSON পার্স করে প্রিন্ট করতে পারেন; dict, function, exception নিজের ভাষায় বুঝাতে পারেন।

---

### Phase 2 — LLM বেসিক + প্রজেক্ট ১: Hello Agent (১ সপ্তাহ)

**লক্ষ্য:** LLM আসলে কী করে, আর কীভাবে তাকে "কর্মী" বানানো যায়।

- LLM = next-token prediction; এটি ডাটাবেস নয়, সত্য যাচাই করে না
- message role: system / user / assistant (পরে tool)
- system prompt-এর গঠন: পরিচয়, লক্ষ্য, নিয়ম, টোন, আউটপুট ফরম্যাট, না-জানা থাকলে কী বলবে
- temperature, top_p — সৃজনশীলতা বনাম নির্ভুলতা
- streaming — উত্তর লেখার সাথে সাথে দেখানো (ঐচ্ছিক; শুরুতে বাদ দিতে পারেন)
- structured output — JSON schema / Pydantic দিয়ে নির্দিষ্ট ফরম্যাটে উত্তর
- hallucination কেন হয়, কীভাবে কমায়: গ্রাউন্ডিং, টুল, "জানি না" বলার অনুমতি
- prompt injection-এর প্রথম পরিচয়

**প্রজেক্ট ১ — Hello Agent**
- "মিতু" নামের অফিস অ্যাসিস্ট্যান্ট, system prompt-এ ছোট একটি কোম্পানি হ্যান্ডবুক
- CLI চ্যাট, পুরো কথোপকথন `messages` লিস্টে রাখা, `/reset` কমান্ড
- নিজের নাম/পছন্দ জিজ্ঞেস করলে উত্তর দেয়, কিন্তু বানিয়ে কিছু বলে না

**শেষ করার মানদণ্ড:** ১০ টার্নের কথোপকথনে পার্সোনা ঠিক থাকে; হ্যান্ডবুকে নেই এমন পলিসি জিজ্ঞেস করলে বানিয়ে বলে না; `/reset` কাজ করে।

> এটা এখনো chatbot। Agent হবে পরের ধাপে — যখন LLM নিজে সিদ্ধান্ত নেবে কোন টুল চালাবে।

---

### Phase 3 — Tool Calling + প্রজেক্ট ২: Weather Agent (১ সপ্তাহ)

**লক্ষ্য:** LLM-এর হাতে "হাত" দেওয়া — এবং ভেতরের লুপটা নিজে লেখা।

- Function calling কীভাবে কাজ করে: schema → model আর্গুমেন্ট দেয় → আপনার কোড চালায় → ফলাফল model-কে ফেরত
- JSON schema দিয়ে tool বর্ণনা; নাম, description, parameters
- **নিজে হাতে agent loop লেখা** (ফ্রেমওয়ার্ক ছাড়া, ~২০ লাইনে): while loop, tool call, result message, max steps
- Pydantic দিয়ে আর্গুমেন্ট validate; ভুল আর্গুমেন্টে এমন error দিন যা model বুঝে ঠিক করতে পারে
- ভালো tool-এর বৈশিষ্ট্য: ছোট ও নির্দিষ্ট কাজ, পরিষ্কার নাম, structured return, args-কে কখনো বিশ্বাস না করা
- একাধিক tool, সঠিক tool বাছাই, infinite loop ঠেকানো
- Open-Meteo API: geocoding + forecast (ফ্রি, key লাগে না)

**প্রজেক্ট ২ — Weather Agent**
- Tools: `get_weather(city)`, `get_forecast(city)` — শুরুতে দুটোই যথেষ্ট
- "আগামীকাল চট্টগ্রামে বৃষ্টি হবে?" → সঠিক টুল, সঠিক আর্গুমেন্ট
- অজানা শহর → ভদ্রভাবে ব্যর্থতা জানায়, বানিয়ে বলে না
- প্রতিটি tool call লগ করে

**শেষ করার মানদণ্ড:** ৫টি ভিন্ন প্রশ্নে সঠিক টুল বেছে নেয়; ভুয়া শহরের নামে বানিয়ে উত্তর দেয় না; সর্বোচ্চ ৫ ধাপে থামে; নিজের লেখা loop-এর প্রতিটি লাইন ব্যাখ্যা করতে পারেন।

---

### Phase 4 — Memory + প্রজেক্ট ৩: Memory Friend (১–২ সপ্তাহ)

**লক্ষ্য:** এজেন্ট যেন কালকের কথা আজও মনে রাখে — এবং অপ্রয়োজনীয় কিছু মনে না রাখে।

- Context window ≠ memory; কথোপকথন লম্বা হলে কী হয়
- Short-term memory: thread/messages, পুরনো অংশের সারাংশ (summarization)
- Long-term memory: প্রোফাইল (নাম, শহর, পছন্দ), episodic (ঘটনা), semantic (জ্ঞান)
- Storage ধাপে ধাপে: JSON → SQLite → vector store
- Embedding: টেক্সট → সংখ্যার vector; cosine similarity দিয়ে মিল
- Chunking, metadata, retrieval
- RAG: index → retrieve → (rerank) → prompt-এ যোগ → উত্তর + উৎস
- কখন RAG লাগে, কখন সাধারণ DB query-ই যথেষ্ট
- Memory write policy: কী সেভ করবেন, কখন, ডুপ্লিকেট এড়ানো, পুরনো তথ্য override, মেয়াদ
- ইউজারের নিয়ন্ত্রণ: `/memory show`, `/forget`
- গোপনীয়তা: PII, লোকাল স্টোরেজ, কে পড়তে পারবে

**প্রজেক্ট ৩ — Memory Friend**
- প্রোফাইল: নাম, শহর, প্রিয় খাবার, লক্ষ্য, গুরুত্বপূর্ণ তারিখ
- উত্তরের আগে প্রাসঙ্গিক memory retrieve; সেভ করার আগে "এটা কি সত্যিই মনে রাখার মতো?" যাচাই
- restart-এর পরেও মনে রাখে; `user_id` দিয়ে আলাদা মানুষ আলাদা memory
- `/memory` দিয়ে দেখায় কী মনে আছে, `/forget` দিয়ে মুছে ফেলে
- নতুন পছন্দ পুরনোটাকে override করে (দ্বন্দ্ব সমাধান)

**শেষ করার মানদণ্ড:** প্রোগ্রাম বন্ধ করে আবার চালালেও পছন্দ মনে আছে; দুই ইউজারের memory মিশে যায় না; "আমি কী কী বলেছিলাম?" জিজ্ঞেস করলে memory থেকে উত্তর দেয়; ভুলে যাওয়ার কমান্ড কাজ করে।

**Stretch:** পুরনো কথোপকথনের উপর vector search।

---

### Phase 5 — LangGraph + প্রজেক্ট ৪: Research Buddy (২ সপ্তাহ)

**লক্ষ্য:** জটিল, বহু-ধাপের কাজ নিয়ন্ত্রণ করা — স্পষ্ট গ্রাফে।

**সপ্তাহ ১ — ধারণা**
- কেন গ্রাফ: অবস্থা (state), শাখা, লুপ, persistence, মানুষের অনুমতি, ডিবাগ
- State: `TypedDict`, reducer (`Annotated[list, add_messages]`) — কে কী যোগ করে
- Node = `function(state) -> partial update`
- Edge, conditional edge, `START`, `END`
- `StateGraph` → compile → `invoke` / `stream`
- `thread_id` + checkpointer দিয়ে কথোপকথন/কাজ চালু রাখা ও resume
- `create_agent` শর্টকাট বনাম নিজের গ্রাফ — কখন কোনটা
- `interrupt` দিয়ে মানুষের অনুমতি
- `recursion_limit` দিয়ে লুপের সীমা
- একই গ্রাফে ছোট মডেল (শ্রেণিবিন্যাস) আর বড় মডেল (গভীর ভাবনা)

**সপ্তাহ ২ — প্রজেক্ট ৪: Research Buddy**

```
START → plan → search → summarize → critique ─(যথেষ্ট?)→ write_report → END
                     ↑                    │
                     └────── revise ←──────┘
```

- প্রশ্ন → উপ-প্রশ্নে ভাগ → সার্চ (Wikipedia API — key লাগে না; চাইলে Tavily/DuckDuckGo) → পড়া → সারাংশ → সমালোচনা → দরকার হলে আবার খোঁজা (সর্বোচ্চ ৩ বার) → সোর্সসহ রিপোর্ট → `.md` ফাইলে সেভ
- Checkpointer: মাঝপথে থামিয়ে আবার চালানো যায়
- Streaming: কোন ধাপে আছে দেখা যায়
- Eval: ১০টি টপিক; প্রতিটি দাবির পাশে সত্যিকারের URL আছে কি না

**শেষ করার মানদণ্ড:** লুপ অনন্ত হয় না; রিপোর্টে আসল সোর্স লিংক থাকে; তথ্য না পেলে বানিয়ে বলে না; interrupt-এর পরে resume হয়; গ্রাফের ছবি কাগজে এঁকে ব্যাখ্যা করতে পারেন।

**Stretch:** parallel search (`Send` API), প্রতিটি সোর্সের জন্য subgraph।

---

### বোনাস — CrewAI (ঐচ্ছিক, ২–৩ দিন)

**লক্ষ্য:** একই agent loop ফ্রেমওয়ার্ক দিয়ে — Agent, Task, Crew দিয়ে টিম বানানো।

- `crewai-basics/`-এ ৫টি ছোট পাঠ: এক crew → দুই কাজ → দুই এজেন্ট → টুল → টিম + ফাইল সেভ
- CrewAI এখন Python 3.10–3.13 চায়; `py -3.12` দিয়ে আলাদা `.venv-crewai` ব্যবহার করুন
- গাইড: [`crewai-basics/README.md`](crewai-basics/README.md)

---

### Phase 6 — Skills: এজেন্টকে কাজ শেখানো (১ সপ্তাহ)

**লক্ষ্য:** বিশাল system prompt-এর বদলে ছোট, পুনর্ব্যবহারযোগ্য "SOP ফাইল"।

- Skill = YAML frontmatter + markdown নির্দেশনা (`SKILL.md`)
- Frontmatter: `name`, `description` (কখন ব্যবহার করবে — এটাই সবচেয়ে গুরুত্বপূর্ণ লাইন)
- Body: কখন ব্যবহার, নিয়ম, ধাপে ধাপে workflow, আউটপুট ফরম্যাট, উদাহরণ, ব্যর্থ হলে কী করবে
- **Progressive disclosure:** সব সময় শুধু নাম+description কনটেক্সটে থাকে; দরকার হলে পুরো স্কিল লোড হয়; script/reference আরও পরে
- Skill বনাম Tool: skill বলে *কীভাবে*, tool দেয় *ক্ষমতা*; skill ভিতরে tool/script ব্যবহার করতে পারে
- লোড করার দুই উপায়: কোডে `load_skill()` (আপনার `ai-mini-office`-এ যেমন আছে) বনাম মডেল নিজে `load_skill(name)` টুল দিয়ে বেছে নেওয়া (বেশি scalable)
- লেখার নিয়ম: নির্দেশমূলক বাক্য, সংখ্যাযুক্ত ধাপ, স্পষ্ট আউটপুট, "টুল কনফার্ম না করলে সফল বলবে না"
- টেস্ট: ৫টি ইনপুট, যার ২টি edge case
- Versioning: git-এ রাখা, স্কিলের ভিতরে changelog
- Anti-pattern: ২০০০ লাইনের স্কিল, "be helpful"-এর মতো অস্পষ্ট কথা, স্কিলে secret, পরস্পরবিরোধী নিয়ম, উদাহরণহীন স্কিল

**হাতে-কলমে**
- `task-manager` স্কিলটি নতুন করে লেখা — when-to-use, workflow, failure handling সহ
- দুটি নতুন স্কিল: `email-tone` (ভদ্র রিপ্লাই লেখা), `report-writer` (সাপ্তাহিক রিপোর্ট)
- একটি `load_skill` টুল + স্কিল ক্যাটালগ (শুধু নাম+description) সিস্টেম প্রম্পটে দেওয়া

**শেষ করার মানদণ্ড:** ৩টি স্কিল টেস্ট করা; একটি বিশাল প্রম্পট বনাম একই কাজ ৩টি স্কিল দিয়ে করিয়ে পার্থক্য দেখাতে পারেন।

---

### Phase 7 — Hermes Agent + প্রজেক্ট ৫: Skill Creator (১ সপ্তাহ)

**লক্ষ্য:** এমন একটি এজেন্ট, যে নিজের অভিজ্ঞতা থেকে নতুন স্কিল বানায় ও উন্নত করে।

**Hermes Agent কী**
- Nous Research-এর ওপেন সোর্স, model-agnostic, long-running agent
- বিশেষত্ব: **self-improving learning loop** — কাজ করার অভিজ্ঞতা থেকে স্কিল বানায়, ব্যবহারের সময় স্কিল উন্নত করে
- Memory: session search, user modeling
- Skills: `~/.hermes/skills/`-এ markdown + YAML frontmatter (আপনার `SKILL.md` ফরম্যাটের মতোই)
- Custom tool: Python module
- Interface: CLI/TUI, web UI, gateway (মেসেজিং প্ল্যাটফর্ম)
- Provider: Nous Portal, OpenRouter, OpenAI

**ইনস্টল ও সেটআপ (Windows)**
```powershell
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
hermes setup
hermes model
hermes
```

**হাতে-কলমে**
1. একটি পুনরাবৃত্ত কাজ বেছে নিন (যেমন "সাপ্তাহিক কাস্টমার ইমেইলের সারসংক্ষেপ")।
2. নিজে একটি `SKILL.md` লিখে `~/.hermes/skills/`-এ রাখুন, তারপর Hermes-কে দিয়ে কাজ করান।
3. একই কাজ কয়েকবার করান; Hermes স্কিল তৈরি/উন্নত করলে **diff দেখে review করুন**, তারপর গ্রহণ করুন।
4. git-এ স্কিল ফোল্ডার রাখুন, যাতে ভুল হলে ফিরিয়ে নিতে পারেন।

**প্রজেক্ট ৫ — Skill Creator (দুই ট্র্যাক)**

- **Track A (সহজ, আগে এটা করুন):** Hermes-কে একটি কাজের লগ দিন, বলুন "এই কাজটা বারবার আসে — একটা স্কিল বানাও"। স্কিল ড্রাফট → আপনার review → টেস্ট প্রম্পটে যাচাই → চূড়ান্ত।
- **Track B (নিজের বানানো):** LangGraph-এ একটি `skill_writer` গ্রাফ — ইন্টারভিউ (কী কাজ, কখন, কোন টুল) → `SKILL.md` ড্রাফট → টুল স্টাব/টেস্ট কেস → নমুনায় চালানো → সমালোচনা → সংশোধন → **অনুমতির পরে** ফাইলে লেখা।

**শেষ করার মানদণ্ড:** একটি বাস্তব পুনরাবৃত্ত কাজের জন্য নতুন স্কিল; ৩/৩ টেস্টে কাজ করে; when-to-use ও failure handling আছে; কোনো secret নেই; ফাইল লেখার আগে অনুমতি নেয়।

**Hermes বনাম নিজের LangGraph স্ট্যাক**

| | Hermes Agent | নিজের LangGraph অ্যাপ |
|---|---|---|
| গতি | খুব দ্রুত শুরু | বেশি সময় লাগে |
| নিয়ন্ত্রণ | সীমিত (তাদের ডিজাইন মানতে হয়) | পুরো নিয়ন্ত্রণ |
| শেখার লুপ | বিল্ট-ইন | নিজে বানাতে হয় |
| নিজের ব্যবসার সিস্টেমে | কম উপযুক্ত | পুরোপুরি উপযুক্ত |
| কখন | দ্রুত প্রোটোটাইপ, ব্যক্তিগত অ্যাসিস্ট্যান্ট | প্রোডাক্ট, নির্দিষ্ট ওয়ার্কফ্লো, কঠোর নিয়ম |

---

### Phase 8 — প্রজেক্ট ৬: Company Helper (২ সপ্তাহ)

**লক্ষ্য:** সবকিছু একসাথে — LangGraph + skills + tools + memory + approval + eval + deploy।

**সেটআপ:** কাল্পনিক কোম্পানি Little Office Ltd., SQLite-এ ২০টি ভুয়া অর্ডার।

**সপ্তাহ ১ — ডেটা ও টুল**
- টেবিল: `customers`, `orders`, `order_items`, `tickets`
- Tools: `find_customer`, `get_order`, `search_products`, `check_refund_eligibility`, `create_ticket`, `send_email` (টেস্ট SMTP/Mailtrap বা ফাইলে আউটবক্স), `escalate_to_human`
- আগে শুধু read-only; write টুলে approval বাধ্যতামূলক

**সপ্তাহ ২ — গ্রাফ, স্কিল, eval**

```
START → intake/guard → classify ─┬→ order_status ─┐
                                 ├→ refund ───────┼→ tool loop → policy_check
                                 └→ other ────────┘                  │
                                              (approval?) → human ───┤
                                                                     ↓
                                                          respond → log → END
```

- Skills: `support-tone`, `refund-policy` (পলিসি ডকুমেন্ট RAG), `escalation-rules`, `email-template`
- Memory: কাস্টমার প্রোফাইল ও আগের টিকিট
- Guardrails: সর্বোচ্চ রিফান্ড সীমা, ইমেইল whitelist, Promise নয়, অন্য কাস্টমারের তথ্য কখনো নয়, "ignore previous instructions" ব্লক
- Observability: প্রতিটি কনভারসেশনের structured log, trace, cost
- Eval: ২০টি সাধারণ + ৫টি প্রতারক কেস; pass rate মাপা
- UI: Streamlit চ্যাট + FastAPI endpoint + দৈনিক সারাংশের cron

**শেষ করার মানদণ্ড (পরীক্ষা)**
1. ১০টি লিখিত সিনারিও সফলভাবে হ্যান্ডেল করে
2. ভুল অর্ডার নাম্বারে ভদ্রভাবে ব্যর্থ হয়, বানিয়ে কিছু বলে না
3. রিফান্ড রিকোয়েস্ট পলিসি অনুযায়ী উত্তর দেয়, অনুমতি ছাড়া টাকা ফেরত দেয় না
4. স্পষ্ট "ignore your rules" চেষ্টা ব্লক হয়, লগে ধরা পড়ে
5. ইমেইল পাঠানোর আগে মানুষের approval লাগে
6. অন্য কাস্টমারের অর্ডার চাইলে তথ্য দেয় না
7. প্রতি উত্তরের সাথে সোর্স/টুল প্রমাণ আছে
8. ২৫টি eval কেসে ৯০%+ pass

**Stretch:** support + billing আলাদা এজেন্ট (multi-agent), MCP server দিয়ে টুল শেয়ার, Telegram gateway।

---

### Phase 9 — Production, Eval, Deploy + Capstone (২ সপ্তাহ)

**লক্ষ্য:** ডেমো নয় — প্রতিদিন ব্যবহারযোগ্য, নিরাপদ, মাপা যায় এমন সিস্টেম।

- **Eval-driven:** golden dataset, assertion, LLM-as-judge, প্রম্পট/স্কিল বদলালে regression টেস্ট
- **Tracing:** LangSmith / Langfuse / OpenTelemetry — কোন ধাপে কী হলো, কত খরচ, কোথায় ব্যর্থ
- **Reliability:** timeout, retry with backoff, idempotency, recursion limit, fallback model
- **খরচ:** ছোট মডেল দিয়ে classification, বড় মডেল দিয়ে reasoning; caching; context ছোট রাখা
- **নিরাপত্তা:** OWASP LLM Top 10 — prompt injection, output handling, data leakage, excessive agency; টুলে least privilege; secrets manager; PII redaction; audit log; rate limit
- **Deploy:** FastAPI + SSE streaming, Docker, env config, health check, monitoring, backup
- **Ops:** প্রম্পট/স্কিল versioning, canary release, ইউজার feedback বোতাম, সাপ্তাহিক রিভিউ
- **নিজের কাজে ব্যবহারের নিয়ম:** shadow mode (শুধু সাজেশন) → approval-সহ assistant → low-risk autonomous → ধীরে বিস্তার; প্রতিটি ধাপে সময় বাঁচছে কি না মাপুন

**Capstone — আপনার নিজের কাজের এজেন্ট**
একটি আসল, পুনরাবৃত্ত, সময়খেকো কাজ বেছে নিন (যেমন অর্ডার রিলেটেড সাপোর্ট, রিপোর্ট তৈরি, ডেটা এন্ট্রি যাচাই)। ডেলিভারেবল:

- সমস্যা বিবরণ + সাফল্যের মাপকাঠি
- ডিজাইন ক্যানভাস (৭ ধাপ)
- কাজ করা repo + README + ডায়াগ্রাম
- ২০টি eval কেস ও ফলাফল
- ছোট ডেমো ভিডিও
- runbook: কীভাবে চালাবেন, কীভাবে থামাবেন, কোথায় মানুষ লাগবে

---

## ৭. ১৬ সপ্তাহের প্ল্যান

| সপ্তাহ | কাজ | আউটপুট |
|---|---|---|
| 0 | সেটআপ, প্রথম API কল | hello_llm.py |
| 1–2 | Python বেসিক | CLI task manager |
| 3 | LLM বেসিক | **প্রজেক্ট ১: Hello Agent** |
| 4 | Tool calling | **প্রজেক্ট ২: Weather Agent** |
| 5–6 | Memory, embedding, RAG | **প্রজেক্ট ৩: Memory Friend** |
| 7–8 | LangGraph | **প্রজেক্ট ৪: Research Buddy** |
| 9 | Skill ডিজাইন | ৩টি টেস্টেড SKILL.md |
| 10 | Hermes Agent | **প্রজেক্ট ৫: Skill Creator** |
| 11–12 | Company Helper | **প্রজেক্ট ৬ (MVP)** |
| 13 | Eval, নিরাপত্তা, tracing | eval রিপোর্ট |
| 14 | Deploy + UI + cron | চলমান সার্ভিস |
| 15 | Capstone + বাফার | নিজের এজেন্ট + ডেমো |

সপ্তাহে ২টি করে সেশন রাখুন (প্রতিটি ২–৩ ঘণ্টা) + সপ্তাহে ২–৩টি ছোট রাতের সেশন। টানা ৮ ঘণ্টার এক সেশন দরকার নেই।

---

## ৮. টেক স্ট্যাক (কেন কী)

| কাজ | টুল | কেন |
|---|---|---|
| ভাষা | Python 3.12+ | এজেন্ট ইকোসিস্টেমের প্রধান ভাষা |
| প্যাকেজ | `uv` বা `venv` + `pip` | দ্রুত, আলাদা পরিবেশ |
| LLM | OpenRouter / Gemini / OpenAI | এক key-তে অনেক মডেল; বাংলা টেস্ট করে বেছে নিন |
| লোকাল মডেল | Ollama | গোপনীয়তা, ইন্টারনেট ছাড়া |
| Orchestration | LangGraph + LangChain v1 | stateful graph, persistence, HITL |
| Validation | Pydantic | টুল আর্গুমেন্ট ও structured output যাচাই |
| HTTP | httpx | টুল ও API কল |
| DB | SQLite | প্রথম থেকেই বাস্তব ডেটা, শেখা সহজ |
| Vector | Chroma / sqlite-vec | embedding search |
| Search | Wikipedia API (key ছাড়া) / Tavily / DuckDuckGo | Research Buddy |
| UI | Streamlit / Gradio | দ্রুত চ্যাট UI |
| API | FastAPI | প্রোডাকশন endpoint + SSE |
| Eval/Trace | LangSmith / Langfuse / pytest | মান ও ডিবাগ |
| Skill runtime | Hermes Agent | শেখার লুপ ও স্কিল ম্যানেজমেন্ট |
| Optional | MCP | টুল/ডেটা সোর্স শেয়ার করা স্ট্যান্ডার্ড |

> ফ্রেমওয়ার্ক শেখার আগে অন্তত একবার ফ্রেমওয়ার্ক ছাড়া agent loop লিখবেন। নাহলে LangGraph "ম্যাজিক" মনে হবে, ডিবাগ করতে পারবেন না।

---

## ৯. ফোল্ডার স্ট্রাকচার

```
ai-agent/
├─ 00-setup/                 # প্রথম API কল, check_env.py, .env.example
├─ python-basics/            # Phase 1 — ৮টি পাঠ
├─ 01-hello-agent/
│  ├─ 01_single_call.py
│  ├─ 02_chat_loop.py
│  ├─ prompts/system.md
│  └─ README.md
├─ 02-weather-agent/
│  ├─ 01_test_tools.py
│  ├─ 02_agent_loop.py       # নিজের লেখা লুপ
│  ├─ tools.py
│  ├─ prompts/system.md
│  └─ README.md
├─ 03-memory-friend/
│  ├─ 01_memory_test.py
│  ├─ 02_memory_agent.py
│  ├─ memory.py
│  ├─ prompts/system.md
│  ├─ memories.json          # প্রথম save-এ তৈরি হয়, git-এ যায় না
│  └─ README.md
├─ 04-research-buddy/
│  ├─ 01_test_tools.py
│  ├─ tools.py               # Wikipedia সার্চ ও পাতা পড়া
│  ├─ nodes.py               # plan, search, summarize, critique, revise, approve, write
│  ├─ graph.py               # গ্রাফ, লুপ, interrupt, রিপোর্ট
│  ├─ prompts/system.md
│  └─ reports/               # তৈরি হওয়া রিপোর্ট (git-এ যায় না)
├─ 05-skill-creator/         # Phase 7 — পরিকল্পিত
│  ├─ skills/                # তৈরি হওয়া স্কিল
│  └─ notes/
├─ 06-company-helper/        # Phase 8 — পরিকল্পিত
│  ├─ app.py                 # FastAPI / Streamlit
│  ├─ graph.py
│  ├─ tools/
│  ├─ skills/
│  ├─ db/seed.py
│  ├─ evals/cases.json
│  └─ logs/
├─ crewai-basics/            # বোনাস — CrewAI ফ্রেমওয়ার্ক (Python 3.12 venv)
│  ├─ 01_first_crew.py
│  ├─ 02_two_tasks.py
│  ├─ 03_two_agents.py
│  ├─ 04_tool.py
│  ├─ 05_team.py
│  ├─ office_note.txt
│  └─ README.md
├─ ai-mini-office/           # আগের প্রোটোটাইপ
├─ shared/                   # skill_loader, llm client, logging
└─ notes/                    # প্রতিদিনের শেখা, ভুল, সমাধান
```

আপনার বর্তমান `ai-mini-office/` ফোল্ডারটি রাখুন — ফেজ ৬-এ এটাকেই আসল এজেন্টে রূপান্তর করবেন।

---

## ১০. দৈনিক রুটিন ও শেখার নিয়ম

**৯০ মিনিটের সেশন**
- ১৫ মিনিট: গত দিনের কোড/নোট রিভিউ
- ৩০ মিনিট: নতুন ধারণা পড়া/দেখা
- ৩৫ মিনিট: হাতে-কলমে কোড
- ১০ মিনিট: নোট — আজ কী শিখলাম, কোথায় আটকালাম, পরের ধাপ

**নিয়ম**
1. প্রতিদিন অন্তত ১টি commit। ছোট হোক।
2. ভিডিও/টিউটোরিয়াল দেখার অনুপাত ৩০%, কোড লেখার ৭০%।
3. ৩০ মিনিটের নিয়ম: কোথাও আটকে ৩০ মিনিটের বেশি না থাকলে প্রশ্ন/ডকুমেন্টে যান; ১ ঘণ্টায় না হলে নোটে লিখে পরের অংশে এগোন।
4. AI অ্যাসিস্ট্যান্ট ব্যবহার করুন, কিন্তু "লাইন বাই লাইন বুঝিয়ে দাও" চেয়ে নিন — কপি-পেস্ট করে চালিয়ে দিলে শেখা হবে না।
5. প্রতি ফেজ শেষে ৫ মিনিটের ভিডিও/নোট — নিজের ভাষায় ব্যাখ্যা (Feynman technique)।
6. প্রতিটি প্রজেক্টের README-তে ডায়াগ্রাম রাখুন — কোড লেখার আগে কাগজে গ্রাফ আঁকুন।

---

## ১১. নতুনদের ১২টি সাধারণ ভুল

1. টিউটোরিয়াল দেখেই এগিয়ে যাওয়া, নিজে না লিখে
2. আগে ফ্রেমওয়ার্ক, পরে বেসিক — উল্টো করা উচিত
3. বিশাল system prompt-এ সব ঠেসে দেওয়া (স্কিল + টুলে ভাগ করুন)
4. কোনো eval কেস না রাখা — "মনে হচ্ছে কাজ করছে" ফাঁদ
5. প্রথম দিনেই write/delete/email টুল দেওয়া
6. context window-এ সব ইতিহাস ঢুকিয়ে খরচ ও গুণমান নষ্ট
7. যা পায় তাই memory-তে সেভ করা
8. লগ না রাখা — ব্যর্থ হলে কারণ খুঁজে পাওয়া যায় না
9. লুপের সীমা না দেওয়া (infinite tool loop)
10. মডেলের দেওয়া টুল আর্গুমেন্ট যাচাই না করা
11. API key কোডে/গিটহাবে রাখা
12. সরাসরি multi-agent — অথচ একটি ভালো single agent-ই যথেষ্ট হতো

---

## ১২. নিরাপত্তা ও নৈতিকতা (শুরুতেই অভ্যাস)

- শুধু নিজের/অনুমোদিত সিস্টেমে কাজ করুন; কারও অ্যাকাউন্ট, সাইট বা ডেটা অনুমতি ছাড়া অটোমেট করবেন না
- ইমেইল/মেসেজ সবসময় টেস্ট অ্যাকাউন্টে; আসল কাস্টমারকে পাঠানোর আগে মানুষের অনুমতি
- টুলে least privilege: যে টুল দরকার নেই, দেবেন না; DB ইউজারকেও read-only রাখুন যেখানে সম্ভব
- মডেলের আউটপুট = অবিশ্বস্ত ইনপুট; shell/SQL/HTML-এ সরাসরি চালাবেন না (injection)
- PII ও secret লগ করবেন না; `.env` কখনো commit নয়
- বাইরের ডকুমেন্ট/ওয়েবপেজে লুকানো নির্দেশ থাকতে পারে — "ignore previous instructions" টাইপ হামলা ধরে রাখার টেস্ট রাখুন
- অপরিবর্তনীয় (irreversible) কাজের আগে সবসময় মানুষ

---

## ১৩. রিসোর্স

**অফিসিয়াল ডকুমেন্টেশন**
- LangGraph: https://docs.langchain.com/oss/python/langgraph/overview
- LangChain Agents (create_agent): https://docs.langchain.com/oss/python/langchain/agents
- LangGraph v1 রিলিজ নোট: https://docs.langchain.com/oss/python/releases/langgraph-v1
- Hermes Agent (GitHub): https://github.com/NousResearch/hermes-agent
- Hermes Agent সাইট: https://hermes-agent.nousresearch.com/
- MCP: https://modelcontextprotocol.io/

**পড়ার মতো**
- Anthropic — Building Effective Agents: https://www.anthropic.com/research/building-effective-agents
- 12-Factor Agents: https://github.com/humanlayer/12-factor-agents
- OWASP LLM Top 10: https://genai.owasp.org/
- AgentSkills: https://agentskills.io/

**টুল/সার্ভিস**
- Open-Meteo (ফ্রি আবহাওয়া API): https://open-meteo.com/
- Tavily Search: https://tavily.com/
- Chroma: https://www.trychroma.com/
- FastAPI: https://fastapi.tiangolo.com/
- LangSmith: https://smith.langchain.com/

**বাংলা টিপ:** প্রম্পট, স্কিল ও রিপোর্ট বাংলায় লিখলেও টেকনিক্যাল নাম (tool, state, node) ইংরেজিতেই রাখুন — ডকুমেন্টেশন ও এরর মেসেজ মেলানো সহজ হবে।

---

## ১৪. শব্দকোষ

| শব্দ | অর্থ |
|---|---|
| **LLM** | Large Language Model — টেক্সট থেকে পরের শব্দ অনুমান করে |
| **Token** | টেক্সটের ছোট টুকরা; খরচ ও সীমা এর এককে |
| **Context window** | একবারে কত token দেখা যায় |
| **Prompt** | মডেলকে দেওয়া নির্দেশনা |
| **System prompt** | স্থায়ী পরিচয় ও নিয়ম |
| **Temperature** | উত্তরের randomness |
| **Tool / Function calling** | মডেলের পক্ষ থেকে কোড চালানোর অনুরোধ |
| **Agent** | সিদ্ধান্ত + টুল + লুপ দিয়ে কাজ করা সিস্টেম |
| **Agent loop** | ভাবা → টুল → ফলাফল → আবার ভাবা |
| **State** | গ্রাফের চলমান ডেটা |
| **Node** | গ্রাফের একটি ধাপ/ফাংশন |
| **Edge** | নোড থেকে নোডে যাওয়ার পথ; conditional edge = শর্তসাপেক্ষ |
| **Checkpointer** | state সেভ করে, যাতে থামিয়ে আবার চালানো যায় |
| **Thread** | একটি আলাদা কথোপকথন/কাজের সূত্র |
| **Memory** | সেশন-পরবর্তী স্মৃতি |
| **RAG** | Retrieve-Augment-Generate — খুঁজে এনে উত্তর |
| **Embedding** | টেক্সটের সংখ্যাগত উপস্থাপনা |
| **Vector DB** | embedding সংরক্ষণ ও মিল খোঁজার ডেটাবেস |
| **Skill** | কাজের লিখিত পদ্ধতি (`SKILL.md`) |
| **HITL** | Human-in-the-loop — মানুষের অনুমতি |
| **Guardrail** | নিষেধ/সীমা |
| **Eval** | নির্দিষ্ট টেস্ট সেটে মান যাচাই |
| **Trace** | প্রতি ধাপের লগ — ডিবাগের জন্য |
| **Hallucination** | তথ্য বানিয়ে বলা |
| **Prompt injection** | ডেটার ভিতরে লুকানো নির্দেশ দিয়ে এজেন্টকে বিভ্রান্ত করা |
| **MCP** | Model Context Protocol — টুল/ডেটা যুক্ত করার স্ট্যান্ডার্ড |
| **Multi-agent** | একাধিক এজেন্টের সহযোগিতা |

---

## ১৫. আজ থেকে শুরু

**আজ (৬০ মিনিট)**
```bash
mkdir ai-agent-labs && cd ai-agent-labs
python -m venv .venv
source .venv/Scripts/activate      # Git Bash (Windows)
python -m pip install --upgrade pip
pip install openai python-dotenv httpx
```
- `.env` ফাইলে key রাখুন, `.gitignore`-এ `.env`
- `hello_llm.py` লিখুন: একটি system message + একটি user message পাঠিয়ে উত্তর প্রিন্ট

**প্রথম সপ্তাহ**
| দিন | কাজ |
|---|---|
| ১ | সেটআপ, প্রথম API কল, git commit |
| ২ | Python: variable, list, dict |
| ৩ | Python: function, loop, if |
| ৪ | ফাইল + JSON লেখা/পড়া, try/except |
| ৫ | CLI task manager (JSON স্টোরেজ) |
| ৬ | প্রজেক্ট ১-এর স্পেক পড়া, কাগজে design |
| ৭ | বিশ্রাম + সপ্তাহের নোট গুছানো |

**প্রথম ফেজের প্রশ্ন (নিজেকে জিজ্ঞেস করুন)**
1. LLM আর ডেটাবেসের পার্থক্য কী?
2. Skill আর Tool-এর পার্থক্য একটি বাক্যে বলুন।
3. Agent loop-এ `max steps` কেন দরকার?
4. Memory-তে কী সেভ করবেন না, আর কেন?
5. একটি কাজ কখন Agent দিয়ে করবেন না?

এই পাঁচটির উত্তর নিজের ভাষায় দিতে পারলে আপনি প্রস্তুত — Phase 0 শুরু করুন।

---

> **মনে রাখবেন:** আপনি "AI-কে দিয়ে কোড লেখানো" শিখছেন না — আপনি শিখছেন *একজন নতুন কর্মীকে (LLM) কাজ শেখানো, সরঞ্জাম দেওয়া, মনে রাখতে শেখানো, আর নিরাপদে কাজ করানো*। গল্পটা মিতুর, কোডটা Python-এর।
