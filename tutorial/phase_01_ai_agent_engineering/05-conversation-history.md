# Chapter 05 — Conversation History & Context Management

**সময়:** ৪ ঘণ্টা  
**লক্ষ্য:** একাধিক প্রশ্নের context ধরে রাখা এবং JSON file-এ conversation সংরক্ষণ করা।

## 1. Stateless API ও Stateful Application

অনেক API call নিজে থেকে আগের request-এর conversation মনে রাখে না। Application-কে প্রয়োজনীয় history পরবর্তী request-এ পাঠাতে হয়, অথবা API-র supported conversation-state feature ব্যবহার করতে হয়।

উদাহরণ:

```text
User: আমার নাম Rahim।
Assistant: তোমার সঙ্গে পরিচিত হয়ে ভালো লাগল।

User: আমার নাম কী?
Assistant: তোমার নাম Rahim।
```

দ্বিতীয় প্রশ্নের সময় প্রথম কথোপকথনের message context-এ থাকতে হবে।

## 2. Message history data structure

```python
history = [
    {"role": "user", "content": "আমার নাম Rahim"},
    {"role": "assistant", "content": "তোমার সঙ্গে পরিচিত হয়ে ভালো লাগল।"},
]
```

এটি Python list-এর ভেতরে dictionary।

## 3. Practical — Multi-turn chat

`history_chat.py`:

```python
from openai import OpenAI
from config import OPENAI_API_KEY, MODEL_NAME

client = OpenAI(api_key=OPENAI_API_KEY)

INSTRUCTIONS = """
তুমি Rahim-এর সহায়ক AI assistant।
সহজ বাংলায় উত্তর দেবে।
আগের conversation context ব্যবহার করবে।
তথ্য না থাকলে অনুমান করবে না।
"""

history = []

def ask_ai(user_text: str) -> str:
    history.append({"role": "user", "content": user_text})

    response = client.responses.create(
        model=MODEL_NAME,
        instructions=INSTRUCTIONS,
        input=history,
    )

    answer = response.output_text
    history.append({"role": "assistant", "content": answer})
    return answer


def main():
    print("Rahim AI — type 'exit' to quit")

    while True:
        question = input("\\nYou: ").strip()

        if question.lower() == "exit":
            break

        if not question:
            continue

        try:
            print("\\nAI:", ask_ai(question))
        except Exception as error:
            print("Error:", type(error).__name__)


if __name__ == "__main__":
    main()
```

চালাও:

```bash
python history_chat.py
```

পরীক্ষা করো:

```text
You: আমার নাম Rahim।
You: আমার নাম কী?
```

Model আগের message context-এ পেলে নামটি বলতে পারবে। Exact wording আলাদা হতে পারে।

## 4. JSON file-এ history save/load

`history_storage.py`:

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
        raise RuntimeError("History JSON corrupted.") from error

    if not isinstance(data, list):
        raise ValueError("History must be a list.")

    return data


def save_history(history: list) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    temp_file = HISTORY_FILE.with_suffix(".tmp")

    temp_file.write_text(
        json.dumps(history, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temp_file.replace(HISTORY_FILE)
```

`history_chat.py`-তে:

```python
from history_storage import load_history, save_history

history = load_history()
```

Assistant answer history-তে যোগ করার পর:

```python
save_history(history)
```

এটি local single-user learning demo। একাধিক user বা concurrent process-এর জন্য JSON file নিরাপদ database নয়। Production-এ SQLite/PostgreSQL, access control ও user isolation প্রয়োজন।

## 5. Conversation ID

```python
import uuid

conversation_id = str(uuid.uuid4())
print(conversation_id)
```

এটি একটি unique identifier। বাস্তবে conversation ID-এর সঙ্গে owner/user ID যাচাই করতে হবে।

## 6. Context window management

History বড় হলে token usage ও context limit বাড়ে। প্রাথমিক কৌশল:
- শেষ কয়েকটি message রাখা
- পুরোনো message summary করা
- গুরুত্বপূর্ণ facts আলাদা memory-তে রাখা
- প্রয়োজনীয় তথ্য retrieval করা

সরল message-count limit:

```python
def keep_recent_messages(messages: list, max_messages: int = 10) -> list:
    return messages[-max_messages:]
```

এটি token count মাপে না; শুধু message সংখ্যা কমায়।

## 7. Homework
1. Multi-turn chat চালাও।
2. Program restart করলেও history load করো।
3. `/clear` command যোগ করো।
4. `keep_recent_messages()` পরীক্ষা করো।
5. Conversation ID তৈরি করো।
6. Stateless API ও Stateful application-এর পার্থক্য লেখো।

## Completion checklist
- [ ] Multi-turn conversation করেছি।
- [ ] History পরের request-এ পাঠিয়েছি।
- [ ] JSON save/load করেছি।
- [ ] Conversation ID বুঝেছি।
- [ ] Context management কেন দরকার বুঝেছি।
