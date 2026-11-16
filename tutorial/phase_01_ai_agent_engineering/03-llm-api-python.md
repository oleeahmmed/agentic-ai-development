# Chapter 03 — LLM API & Python Integration

**সময়:** ৪ ঘণ্টা  
**লক্ষ্য:** Ubuntu-তে Python project থেকে OpenAI API request পাঠানো, response নেওয়া এবং error handle করা।

## 1. API কী?

API হলো নির্ধারিত interface, যার মাধ্যমে একটি software অন্য software-এর service ব্যবহার করে।

```text
Python Application
      |
   HTTPS request
      |
   OpenAI API
      |
   Model
      |
   HTTPS response
      |
Python Application
```

## 2. Environment তৈরি

```bash
mkdir -p ~/rahim_ai
cd ~/rahim_ai
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install openai python-dotenv
```

## 3. API key নিরাপদে রাখা

`.env`:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4.1-mini
```

নিজের API key বসাবে। Key কাউকে পাঠাবে না।

`.gitignore`:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

## 4. config.py

```python
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY পাওয়া যায়নি। .env পরীক্ষা করো।")
```

নিজের account-এ উপলভ্য model name ব্যবহার করবে।

## 5. প্রথম API call

`first_call.py`:

```python
from openai import OpenAI
from config import OPENAI_API_KEY, MODEL_NAME

client = OpenAI(api_key=OPENAI_API_KEY)

response = client.responses.create(
    model=MODEL_NAME,
    input="Explain AI Agent in simple Bengali."
)

print(response.output_text)
```

চালাও:

```bash
python first_call.py
```

## 6. Code বুঝে নাও

- `OpenAI(...)` API client তৈরি করে।
- `responses.create(...)` API request পাঠায়।
- `model` কোন model ব্যবহার হবে তা নির্ধারণ করে।
- `input` model-এর কাছে পাঠানো content।
- `response.output_text` text response দেয়।

## 7. Error handling

`safe_call.py`:

```python
from openai import (
    OpenAI,
    APIConnectionError,
    APIStatusError,
    RateLimitError,
)
from config import OPENAI_API_KEY, MODEL_NAME

client = OpenAI(
    api_key=OPENAI_API_KEY,
    timeout=30.0,
    max_retries=2,
)

def ask_ai(question: str) -> str:
    try:
        response = client.responses.create(
            model=MODEL_NAME,
            input=question,
        )
        return response.output_text

    except RateLimitError:
        return "Rate limit, quota বা billing সমস্যা হয়েছে।"

    except APIConnectionError:
        return "Network connection সমস্যা হয়েছে।"

    except APIStatusError as error:
        return f"API status error: {error.status_code}"

    except Exception as error:
        return f"Unexpected error: {type(error).__name__}"


if __name__ == "__main__":
    print(ask_ai(input("You: ")))
```

## 8. Terminal chat loop

`chat.py`:

```python
from openai import OpenAI
from config import OPENAI_API_KEY, MODEL_NAME

client = OpenAI(api_key=OPENAI_API_KEY, timeout=30.0, max_retries=2)

print("Rahim AI — type 'exit' to quit")

while True:
    question = input("\\nYou: ").strip()

    if question.lower() == "exit":
        print("AI: Goodbye!")
        break

    if not question:
        continue

    try:
        response = client.responses.create(
            model=MODEL_NAME,
            input=question,
        )
        print("\\nAI:", response.output_text)

    except Exception as error:
        print("Request failed:", type(error).__name__)
```

চালাও:

```bash
python chat.py
```

এই Chapter-এর chat loop আগের প্রশ্ন মনে রাখে না। প্রতিটি request আলাদা। Conversation history Chapter 05-এ তৈরি করব।

## 9. সাধারণ error

| Error | কী পরীক্ষা করবে |
|---|---|
| `ModuleNotFoundError` | venv active এবং package installed কি না |
| Authentication / 401 | API key সঠিক কি না |
| 429 | Rate limit, quota, billing |
| Connection error | Internet, DNS, network |
| Model not found | Model name ও account access |

API usage-এর খরচ হতে পারে; dashboard-এ billing ও usage limit দেখে নিও।

## 10. Homework
1. `first_call.py` নিজে তৈরি করো।
2. বাংলা ও ইংরেজি prompt পাঠাও।
3. `MODEL_NAME` `.env` থেকে load করো।
4. `safe_call.py` চালাও।
5. API key কখনো print করবে না।
6. Request/response flow আঁকো।

## Completion checklist
- [ ] venv তৈরি করেছি।
- [ ] `.env` থেকে key load করেছি।
- [ ] API call সফল হয়েছে।
- [ ] Error handling যোগ করেছি।
- [ ] Terminal chat চালিয়েছি।
