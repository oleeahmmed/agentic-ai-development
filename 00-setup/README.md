# Phase 0 — পরিবেশ তৈরি (হাতে-কলমে গাইড)

> এই ফাইলটি দেখে হুবহু আবার বানানো যাবে। প্রতিটি ধাপে **কমান্ড → প্রত্যাশিত ফলাফল → কেন করছি** আছে।
> সময়: ৩০–৪৫ মিনিট। খরচ: প্রথম কলে ১ সেন্টেরও কম।

---

## এই ফেজে কী কী বানানো হলো

| ফাইল/ফোল্ডার | কাজ |
|---|---|
| `.venv/` | আলাদা Python পরিবেশ (git-এ যাবে না) |
| `00-setup/hello_llm.py` | প্রথম LLM কল — system + user message, token হিসাব |
| `00-setup/check_env.py` | Python, প্যাকেজ, `.env` যাচাই (নেটওয়ার্ক কল করে না) |
| `00-setup/.env.example` | কোন কোন সেটিং লাগবে তার নমুনা |
| `00-setup/requirements.txt` | এই ফেজের প্যাকেজ |
| `.gitignore` | `.env`, `.venv`, `__pycache__` বাদ দেওয়ার নিয়ম |
| `README.md` (এই ফাইল) | ধাপে ধাপে পুনরুত্পাদনের নির্দেশনা |

ফোল্ডারগুলো (`01-hello-agent/` … `06-company-helper/`) এখনই তৈরি করা হয়েছে, যাতে প্রতিটি প্রজেক্টের নিজের গাইড ও কোড আলাদা থাকে।

---

## ধাপ ১ — ফোল্ডার কাঠামো

রিপো রুট (`ai-agent/`) থেকে:

```bash
mkdir -p 00-setup 01-hello-agent 02-weather-agent 03-memory-friend \
         04-research-buddy 05-skill-creator 06-company-helper shared notes
```

**কেন:** প্রতিটি প্রজেক্টের নিজের ফোল্ডার — কোড, গাইড, ডেটা একসাথে থাকবে। পরে কিছু ভাঙলে বাকি প্রজেক্ট অক্ষত থাকবে।

---

## ধাপ ২ — ভার্চুয়াল এনভায়রনমেন্ট

```bash
python -m venv .venv
.venv/Scripts/python.exe --version
```

প্রত্যাশিত: `Python 3.14.10` (বা ৩.১১+ যেকোনো ভার্সন)।

**কেন:** `.venv` একটি আলাদা বাক্স। এখানে যা ইনস্টল করবেন, আপনার সিস্টেমের অন্য প্রজেক্টে তার প্রভাব পড়বে না। এক প্রজেক্টের প্যাকেজ ভার্সন আরেক প্রজেক্ট নষ্ট করবে না।

**সক্রিয় করার দরকার নেই** — আমরা সবসময় `.venv/Scripts/python.exe` দিয়ে সরাসরি চালাব। চাইলে:

```bash
source .venv/Scripts/activate     # Git Bash
# PowerShell: .venv\Scripts\Activate.ps1
```

ভিতরে আছেন কি না বোঝার উপায়: প্রম্পটের আগে `(.venv)` দেখাবে।

> Python 3.14 নতুন; বেশিরভাগ প্যাকেজ কাজ করে। ভবিষ্যতে LangGraph-এ কোনো সমস্যা হলে Python 3.12/3.13-এ নতুন venv বানাবেন — কোড বদলাতে হবে না।

---

## ধাপ ৩ — প্যাকেজ ইনস্টল

```bash
.venv/Scripts/python.exe -m pip install --upgrade pip
.venv/Scripts/python.exe -m pip install -r 00-setup/requirements.txt
```

যাচাই:

```bash
.venv/Scripts/python.exe -m pip list
```

প্রত্যাশিত (ভার্সন আপনার সময়ে আলাদা হতে পারে):

```
httpx            0.28.1
openai           3.50.0
python-dotenv    1.2.4
```

**কেন কোনটা:**

- `openai` — LLM-এর সাথে কথা বলার ক্লায়েন্ট (OpenAI, OpenRouter, Gemini, Ollama — সবাই একই OpenAI-ফরম্যাটে চলে)
- `python-dotenv` — `.env` ফাইল থেকে গোপন সেটিং পড়া
- `httpx` — সাধারণ HTTP কল; পরের ফেজে আবহাওয়ার API-তে লাগবে

---

## ধাপ ৪ — LLM API key নেওয়া

যেকোনো **একটি** বেছে নিন। শিক্ষার জন্য সস্তা মডেলই যথেষ্ট।

**অপশন A — OpenRouter (সবচেয়ে সুবিধাজনক)**
1. https://openrouter.ai → Sign up
2. Credits-এ ছোট টপ-আপ (৫ ডলার অনেকদিন চলবে)
3. Keys → Create Key → নাম দিন `ai-agent-labs`
4. `sk-or-v1-...` কী কপি করুন
5. মডেলের slug দেখুন Models পেজে (যেমন `openai/gpt-4.1-mini`, `google/gemini-2.5-flash`)

**অপশন B — Google AI Studio (ফ্রি টিয়ার)**
1. https://aistudio.google.com → Get API key
2. কী কপি করুন
3. Base URL: `https://generativelanguage.googleapis.com/v1beta/openai/`

**অপশন C — OpenAI**
1. https://platform.openai.com → API keys → Create new secret key
2. বিলিং চালু থাকতে হবে

**অপশন D — Ollama (লোকাল, ইন্টারনেট/খরচ নেই)**
1. https://ollama.com থেকে ইনস্টল
2. `ollama pull qwen3:8b`
3. Base URL: `http://localhost:11434/v1`, key: `ollama`

> **নিরাপত্তা:** API key = অফিসের আইডি কার্ড + ওয়ালেট। স্ক্রিনশটে, চ্যাটে, গিটহাবে দেখাবেন না। লিক হলে সাথে সাথে ড্যাশবোর্ড থেকে revoke করে নতুন key নিন।

---

## ধাপ ৫ — `.env` তৈরি

```bash
cp 00-setup/.env.example 00-setup/.env
code 00-setup/.env        # অথবা notepad 00-setup/.env
```

শুধু একটি ব্লক সক্রিয় রাখুন, বাকিগুলো `#` দিয়ে কমেন্ট। উদাহরণ (OpenRouter):

```env
LLM_API_KEY=sk-or-v1-আপনার-আসল-কী
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=openai/gpt-4.1-mini
```

| ভেরিয়েবল | কাজ |
|---|---|
| `LLM_API_KEY` | পরিচয়পত্র — কে কল করছে |
| `LLM_BASE_URL` | কোন সার্ভারে যাবে (একই কোড, ভিন্ন provider) |
| `LLM_MODEL` | কোন মডেল উত্তর দেবে |

**কেন `.env`:** কোডে key লিখলে ভুলে git-এ চলে যাবে। `.env` গিটহাবের বাইরে থাকে, কোড একই থাকে। অফিসের গোপন নথি আর সাধারণ ফাইলের পার্থক্যের মতো।

> Windows Notepad ব্যবহার করলে File → Save as → "All files" বেছে `00-setup/.env` লিখুন; নাহলে `00-setup/.env.txt` তৈরি হবে আর স্ক্রিপ্ট ফাইলটা খুঁজে পাবে না।

---

## ধাপ ৬ — পরিবেশ যাচাই

```bash
.venv/Scripts/python.exe 00-setup/check_env.py
```

key বসানোর **আগে** এমন দেখাবে (এটাই স্বাভাবিক):

```
[OK  ] Python 3.11+ — পাওয়া গেছে 3.14
[OK  ] প্যাকেজ: openai
[OK  ] প্যাকেজ: python-dotenv
[OK  ] প্যাকেজ: httpx
[FAIL] .env ফাইল — নেই — .env.example কপি করে .env বানান
[FAIL] LLM_API_KEY সেট — .env-এ আসল key দিন
[FAIL] LLM_MODEL সেট — .env-এ মডেলের নাম দিন
```

key বসানোর **পরে** সব `OK` হবে, শেষে দেখাবে:

```
সব ঠিক আছে। এখন চালান:
  .venv/Scripts/python.exe 00-setup/hello_llm.py
```

**কেন এই স্ক্রিপ্ট:** ভুল ধরার সেরা সময় — কল করার আগে। নেটওয়ার্ক কল না করেই বোঝা যায় কী নেই।

---

## ধাপ ৭ — প্রথম LLM কল

```bash
.venv/Scripts/python.exe 00-setup/hello_llm.py
```

প্রত্যাশিত আউটপুট (উত্তর মডেলভেদে আলাদা):

```
মডেল     : openai/gpt-4.1-mini
Base URL : https://openrouter.ai/api/v1
প্রশ্ন     : তুমি কে? এক বাক্যে বলো।
-------------------------------------------------------
আমি Little Office Ltd.-এর সহায়ক অফিস অ্যাসিস্ট্যান্ট...
-------------------------------------------------------
Tokens: input=48, output=21, total=69

Phase 0 সফল। এখন README-এর ৯ নম্বর ধাপে যান।
```

### কোডটি লাইন ধরে বোঝা

`00-setup/hello_llm.py` খুলে দেখুন:

1. **`load_dotenv(ENV_PATH)`** — `.env` ফাইলের প্রতিটি লাইন `os.environ`-এ ঢোকায়। এরপর `os.getenv` দিয়ে পড়া যায়।
2. **`ENV_PATH = Path(__file__).parent / ".env"`** — ফাইলটি যে ফোল্ডারে আছে, সেখানেই `.env` খোঁজে। ফলে যে ফোল্ডার থেকে কমান্ড চালান, তাতে কিছু যায় আসে না।
3. **`api_key`, `model`, `base_url`** — সবই বাইরে থেকে আসে, কোডে লেখা নেই। provider বদলাতে শুধু `.env` বদলাবেন।
4. **`OpenAI(api_key=..., base_url=...)`** — ক্লায়েন্ট। `base_url` না দিলে ডিফল্ট OpenAI-তে যাবে।
5. **`messages`** — দুটি চিঠি:
   - `system`: স্থায়ী পরিচয় ও নিয়ম ("তুমি কে, কীভাবে কথা বলবে")
   - `user`: আজকের কাজ ("তুমি কে?")
6. **`client.chat.completions.create(...)`** — সার্ভারে অনুরোধ; উত্তর ফেরত আসে।
7. **`response.choices[0].message.content`** — আসল উত্তর। (`choices` লিস্ট, কারণ একাধিক উত্তর চাওয়া যায়।)
8. **`response.usage`** — কত token খরচ হলো। এটাই আপনার বিলের হিসাব।
9. **`try/except`** — key ভুল (401), নেটওয়ার্ক সমস্যা, বা অন্য error-এ বাংলায় বোঝায়, ভয়ংকর ট্রেসব্যাক দেখায় না।
10. **`sys.stdout.reconfigure(encoding="utf-8")`** — Windows কনসোলে বাংলা অক্ষর যাতে `UnicodeEncodeError` না দেয়।

**একটা গুরুত্বপূর্ণ লক্ষ্য:** এখানে উত্তর এসেছে মডেলের **সাধারণ জ্ঞান** থেকে। Little Office Ltd. বলে আসলে কিছু নেই — মডেল সেটা জানে না, কিন্তু ভদ্রভাবে উত্তর দিয়েছে। পরের ফেজে এই ফাঁদটাই ধরবেন।

---

## ধাপ ৮ — Git দিয়ে সংরক্ষণ

```bash
git status
git init
git add .
git status          # .env আছে কি না দেখুন — থাকা যাবে না
git commit -m "chore: phase 0 environment setup"
git branch -M main
```

GitHub-এ নতুন (private) রিপো বানিয়ে:

```bash
git remote add origin https://github.com/<username>/<repo>.git
git push -u origin main
```

**কেন:** প্রতিদিনের কাজের স্ন্যাপশট। ভুল হলে ফিরে যাওয়া যায়। প্রতিটি ফেজ শেষে একটি commit — এটি শেখার অংশ।

`.gitignore` যা বাদ দেয়: `.venv/`, `__pycache__/`, `.env`, ডেটাবেস ফাইল, লগ। `.venv` কখনো commit করবেন না — হাজারো ফাইল, OS-নির্ভর।

---

## ধাপ ৯ — নিজে আবার বানান (সবচেয়ে গুরুত্বপূর্ণ)

এখন এই গাইড না দেখে একটা নতুন ফোল্ডারে চেষ্টা করুন:

1. `practice/` ফোল্ডার, নতুন venv, একই ৩টি প্যাকেজ।
2. `.env` নিজে বানিয়ে key বসান।
3. `hello.py` **মনে থেকে** লিখুন: dotenv → key পড়া → client → system+user → উত্তর প্রিন্ট।
4. চালান। কোথায় আটকালেন, নোটে লিখুন।

**বোনাস পরীক্ষা — Hallucination ধরা**

`USER_PROMPT` বদলে করুন: `"Little Office Ltd.-এর আজকের স্টক কত?"`

- প্রথমে যেমন আছে তেমন চালান — দেখুন মডেল বানিয়ে বলছে কি না।
- এবার `SYSTEM_PROMPT`-এ যোগ করুন:
  `"কোম্পানির নির্দিষ্ট তথ্য তোমার জানা নেই। জানা না থাকলে স্পষ্ট বলো: 'আমি এই তথ্য জানি না।'"`
- আবার চালান — পার্থক্য লক্ষ্য করুন।

এটাই Phase 2-এর মূল শিক্ষা: **প্রম্পট দিয়ে আচরণ নিয়ন্ত্রণ করা যায়, কিন্তু সত্য জানানো যায় না — তার জন্য টুল/ডেটা লাগে।**

---

## সমস্যা হলে

| উপসর্গ | কারণ ও সমাধান |
|---|---|
| `ModuleNotFoundError: openai` | ভুল Python দিয়ে চালাচ্ছেন। `.venv/Scripts/python.exe` ব্যবহার করুন |
| `401 Unauthorized` | key ভুল/মেয়াদোত্তীর্ণ — `.env` আবার দেখুন, নতুন key নিন |
| `404 model not found` | `LLM_MODEL` slug ভুল, অথবা `LLM_BASE_URL` মেলেনি |
| `429` | রেট লিমিট/ক্রেডিট শেষ — একটু অপেক্ষা বা টপ-আপ |
| `APIConnectionError` | ইন্টারনেট, VPN, বা base URL ভুল |
| `UnicodeEncodeError` | `PYTHONUTF8=1 .venv/Scripts/python.exe ...` অথবা স্ক্রিপ্টের reconfigure লাইন রাখুন |
| `.env` পাওয়া যাচ্ছে না | ফাইলটি `00-setup/.env`-এ আছে কি? নাম `.env.txt` হয়ে গেছে কি? |
| বাংলা বক্স/প্রশ্নবোধক দেখাচ্ছে | Windows Terminal ব্যবহার করুন; CMD-তে `chcp 65001` |

---

## খরচ নিয়ন্ত্রণ

- শিক্ষার সময় ছোট মডেল ব্যবহার করুন; বড় মডেল শুধু দরকারে।
- প্রতিটি কলে `usage` দেখুন — input token বেশি হলে প্রম্পট ছোট করুন।
- ড্যাশবোর্ডে মাসিক লিমিট সেট করুন।
- একই প্রশ্ন বারবার করতে হলে উত্তর ক্যাশ করুন (পরে শিখবেন)।

---

## শেষ করার চেকলিস্ট

- [ ] Python 3.11+ আছে
- [ ] `.venv` তৈরি হয়েছে
- [ ] `openai`, `python-dotenv`, `httpx` ইনস্টল
- [ ] `.env`-এ আসল key, model, base URL
- [ ] `check_env.py`-তে সব `OK`
- [ ] `hello_llm.py` উত্তর ও token দেখাচ্ছে
- [ ] `git status`-এ `.env` নেই
- [ ] প্রথম commit/push হয়েছে
- [ ] গাইড না দেখে আবার লিখেছেন
- [ ] hallucination পরীক্ষাটি করেছেন

---

## পরের ফেজে যাওয়ার আগে ৫টি প্রশ্ন

1. `system` আর `user` message-এর কাজ আলাদা কেন?
2. `.env` কেন দরকার, কোডে key লিখলে কী সমস্যা?
3. `LLM_BASE_URL` কী কাজে লাগে?
4. token কী, আর খরচের সাথে সম্পর্ক কী?
5. key লিক হলে প্রথম কী করবেন?

উত্তর নিজের ভাষায় বলতে পারলে Phase 1 (Python) শুরু করুন — [সিলেবাস](../ai-agent-syllabus-bangla.md)।
