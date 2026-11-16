# Chapter 06 — Build Your First AI Assistant

**সময়:** ৪–৬ ঘণ্টা  
**লক্ষ্য:** আগের Chapter-এর জ্ঞান দিয়ে modular Python project-এ basic terminal AI assistant তৈরি করা।

এই project-এ এখনো Skill Loader, Long-term Memory, Tools বা autonomous Agent Loop থাকবে না। এগুলো পরবর্তী Phase-এ আলাদাভাবে তৈরি হবে।

## 1. Folder structure

```text
rahim_ai/
├── main.py
├── config.py
├── llm.py
├── prompts.py
├── history.py
├── requirements.txt
├── .env
├── .gitignore
└── data/
    └── conversations.json
```

## 2. Environment

```bash
cd ~/rahim_ai
source .venv/bin/activate
python -m pip install openai python-dotenv
python -m pip freeze > requirements.txt
mkdir -p data
```

`.env`:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4.1-mini
```

`.gitignore`:

```gitignore
.env
.venv/
__pycache__/
*.pyc
data/
```

## 3. config.py

```python
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY পাওয়া যায়নি। .env পরীক্ষা করো।")
```

## 4. prompts.py

```python
SYSTEM_INSTRUCTIONS = """
তুমি Rahim AI, একজন helpful ও honest AI assistant।

নিয়ম:
1. ব্যবহারকারী বাংলায় লিখলে বাংলায় উত্তর দেবে।
2. সহজ ও পরিষ্কার ভাষা ব্যবহার করবে।
3. Code চাইলে runnable example দেবে।
4. ধাপে ধাপে ব্যাখ্যা করবে।
5. তথ্য জানা না থাকলে অনুমান করে সত্য হিসেবে বলবে না।
"""
```

## 5. llm.py

```python
from openai import OpenAI
from config import OPENAI_API_KEY, MODEL_NAME

client = OpenAI(
    api_key=OPENAI_API_KEY,
    timeout=30.0,
    max_retries=2,
)

def generate_response(instructions: str, messages: list) -> str:
    response = client.responses.create(
        model=MODEL_NAME,
        instructions=instructions,
        input=messages,
    )
    return response.output_text
```

এই module API details আড়াল করে। `main.py`-কে SDK request details জানতে হয় না।

## 6. history.py

```python
import json
from pathlib import Path

DATA_DIR = Path("data")
HISTORY_FILE = DATA_DIR / "conversations.json"

def load_history() -> list:
    DATA_DIR.mkdir(exist_ok=True)

    if not HISTORY_FILE.exists():
        return []

    try:
        data = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise RuntimeError("History JSON file invalid.") from error

    if not isinstance(data, list):
        raise ValueError("History data must be a list.")

    return data


def save_history(messages: list) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    temp_file = HISTORY_FILE.with_suffix(".tmp")

    temp_file.write_text(
        json.dumps(messages, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temp_file.replace(HISTORY_FILE)


def clear_history() -> None:
    save_history([])
```

## 7. main.py

```python
from llm import generate_response
from prompts import SYSTEM_INSTRUCTIONS
from history import load_history, save_history, clear_history


def main():
    print("=" * 55)
    print("             RAHIM AI ASSISTANT")
    print("=" * 55)
    print("Commands: /exit, /clear, /help")

    messages = load_history()

    while True:
        user_input = input("\\nYou: ").strip()

        if not user_input:
            continue

        command = user_input.lower()

        if command == "/exit":
            print("Rahim AI: Goodbye!")
            break

        if command == "/help":
            print("Rahim AI: /exit = quit, /clear = clear history, /help = help")
            continue

        if command == "/clear":
            messages = []
            clear_history()
            print("Rahim AI: Conversation history cleared.")
            continue

        messages.append({
            "role": "user",
            "content": user_input,
        })

        try:
            answer = generate_response(
                instructions=SYSTEM_INSTRUCTIONS,
                messages=messages,
            )

            messages.append({
                "role": "assistant",
                "content": answer,
            })

            save_history(messages)
            print("\\nRahim AI:", answer)

        except Exception as error:
            # Request ব্যর্থ হলে user message history থেকে সরানো হচ্ছে।
            messages.pop()
            print("Rahim AI: Request failed:", type(error).__name__)


if __name__ == "__main__":
    main()
```

## 8. Run

```bash
cd ~/rahim_ai
source .venv/bin/activate
python main.py
```

পরীক্ষা:

```text
You: আমার নাম Rahim।
You: আমি কী শিখছি?
You: /help
You: /clear
You: /exit
```

Model-এর exact উত্তর আলাদা হতে পারে।

## 9. Architecture walkthrough

```text
                 main.py
                    |
          +---------+---------+
          |                   |
       prompts.py           history.py
          |                   |
          |                JSON file
          |
        llm.py
          |
     OpenAI Responses API
          |
       AI output
          |
       main.py
          |
    save history + print
```

একটি প্রশ্ন এলে:
1. `main.py` input নেয়।
2. User message history-তে যোগ করে।
3. `prompts.py` থেকে instructions নেয়।
4. `llm.py` API request পাঠায়।
5. Model response ফেরত দেয়।
6. Assistant message history-তে যোগ হয়।
7. `history.py` JSON file-এ save করে।
8. Terminal-এ উত্তর দেখায়।

## 10. Testing checklist

- [ ] Program start হয়।
- [ ] বাংলায় প্রশ্নের উত্তর দেয়।
- [ ] একাধিক প্রশ্নে আগের context ব্যবহার করে।
- [ ] `/help` কাজ করে।
- [ ] `/clear` history মুছে দেয়।
- [ ] `/exit` program বন্ধ করে।
- [ ] Restart করলে history load হয়।
- [ ] API key source code-এ নেই।
- [ ] `.env` Git ignore করা আছে।

## 11. Known limitations

এটি learning project, production-ready নয়:
- JSON file single-user demo-এর জন্য।
- Token-aware history trimming নেই।
- Authentication ও user isolation নেই।
- Skill system নেই।
- Tool execution নেই।
- Long-term memory নেই।
- Logging, monitoring ও automated tests নেই।

## 12. Final homework

1. `/new` command যোগ করো।
2. Conversation ID তৈরি করো।
3. Assistant-এর নাম configuration থেকে পড়ো।
4. API failure হলে বাংলায় পরিষ্কার message দেখাও।
5. প্রতিটি file-এর দায়িত্ব ব্যাখ্যা করো।

## Phase 01 complete criteria

- [ ] AI, ML, DL, LLM ও Agent-এর পার্থক্য বুঝি।
- [ ] Token, Embedding, Context Window ও Hallucination বুঝি।
- [ ] Python থেকে LLM API call করতে পারি।
- [ ] Prompt ও Instructions তৈরি করতে পারি।
- [ ] Multi-turn conversation চালাতে পারি।
- [ ] Modular Basic AI Assistant নিজে তৈরি ও debug করতে পারি।

**পরবর্তী Phase 02:** Skill Engineering — Skill file, metadata, progressive loading, skill discovery এবং skill router।
