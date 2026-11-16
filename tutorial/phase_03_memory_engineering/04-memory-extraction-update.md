# Chapter 04 — Memory Extraction, Validation & Update

**সময়:** ৪ ঘণ্টা  
**লক্ষ্য:** Conversation থেকে candidate memory বের করা, validate করা, SQLite-এ save/update/delete করা।

## 1. Memory extraction কী?

User-এর প্রতিটি sentence memory-তে রাখা উচিত নয়। Application-কে বুঝতে হবে কোন তথ্য ভবিষ্যতে কাজে লাগতে পারে।

উদাহরণ:

- “আমার project-এর নাম rahim_ai” — candidate project fact
- “আজ বৃষ্টি হচ্ছে” — সাধারণত short-lived fact
- “এই password মনে রেখো” — sensitive; সাধারণ memory-তে রাখা উচিত নয়

LLM candidate fact প্রস্তাব করতে পারে। কিন্তু application schema ও policy validate করে তারপর save করবে।

## 2. Extraction pipeline

```text
User message
    |
    v
LLM extracts candidate facts
    |
    v
JSON parse
    |
    v
Schema validation
    |
    v
Privacy / safety policy
    |
    v
User-scoped database write
```

## 3. Practical — structured extraction

`memory_extractor.py` তৈরি করো:

```bash
nano memory_extractor.py
```

Code:

```python
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is missing from .env")

client = OpenAI(api_key=api_key)

ALLOWED_CATEGORIES = {
    "preference",
    "project",
    "learning_goal",
}


def extract_candidate_memories(user_message: str) -> list[dict]:
    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions=(
            "Extract only stable, useful, non-sensitive facts explicitly "
            "stated by the user. Do not infer personal facts. Do not extract "
            "passwords, API keys, financial secrets, health details, or other "
            "sensitive information. Return JSON: "
            '{"memories":[{"key":"...","value":"...","category":"..."}]}. '
            "If nothing qualifies, return an empty memories list."
        ),
        input=user_message,
    )

    payload = json.loads(response.output_text)
    memories = payload.get("memories", [])

    if not isinstance(memories, list):
        raise ValueError("memories must be a list")

    validated = []

    for item in memories:
        if not isinstance(item, dict):
            continue

        key = item.get("key")
        value = item.get("value")
        category = item.get("category")

        if not all(isinstance(x, str) and x.strip()
                   for x in (key, value, category)):
            continue

        if category not in ALLOWED_CATEGORIES:
            continue

        if len(key) > 80 or len(value) > 500:
            continue

        validated.append({
            "key": key.strip(),
            "value": value.strip(),
            "category": category,
        })

    return validated


if __name__ == "__main__":
    message = input("User message: ")
    print(json.dumps(
        extract_candidate_memories(message),
        ensure_ascii=False,
        indent=2,
    ))
```

Run:

```bash
python3 memory_extractor.py
```

Test:

```text
আমার project-এর নাম rahim_ai এবং আমি Python শিখতে চাই।
```

Model-এর output-এ project ও learning goal candidate হিসেবে আসতে পারে। Exact output model-এর ওপর নির্ভর করবে।

## 4. Extracted memory সরাসরি save করবে না

Extraction output LLM-generated এবং ভুল হতে পারে। তাই:
- JSON parse করবে
- field type validate করবে
- allowed category যাচাই করবে
- value length সীমিত করবে
- sensitive তথ্য বাদ দেবে
- প্রয়োজন হলে user confirmation নেবে

বিশেষত user সম্পর্কে দীর্ঘমেয়াদি fact save করার আগে explicit consent/clear expectation থাকা জরুরি।

## 5. SQLite-এ extraction result save

আগের `sqlite_memory.py` থেকে `save_memory(user_id, key, value)` import করা যায়। তবে category রাখার জন্য table schema বাড়াতে হবে।

একটি migration বা নতুন table-এর উদাহরণ:

```sql
CREATE TABLE IF NOT EXISTS user_memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    memory_key TEXT NOT NULL,
    memory_value TEXT NOT NULL,
    category TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE(user_id, memory_key)
);
```

Python insert:

```python
import sqlite3
from datetime import datetime, timezone


def store_candidate(db_path, user_id, memory):
    with sqlite3.connect(db_path) as connection:
        connection.execute("""
            INSERT INTO user_memories (
                user_id, memory_key, memory_value, category, updated_at
            )
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id, memory_key)
            DO UPDATE SET
                memory_value = excluded.memory_value,
                category = excluded.category,
                updated_at = excluded.updated_at
        """, (
            user_id,
            memory["key"],
            memory["value"],
            memory["category"],
            datetime.now(timezone.utc).isoformat(),
        ))
```

এখানে `user_id` অবশ্যই authenticated application session থেকে আসবে।

## 6. Memory update

User বলল:
> আমার project-এর নাম এখন rahim_agent।

এটি পুরোনো `project_name` key-এর value replace করতে পারে। একই key-তে upsert করলে duplicate record হবে না।

তবে conflicting fact এলে policy ঠিক করতে হবে:
- নতুন তথ্য কি পুরোনোটিকে replace করবে?
- User কি correction স্পষ্ট করেছে?
- তথ্যটি কখন update হয়েছে?
- আগের value audit history-তে রাখা দরকার কি?

## 7. Memory delete / forget

Delete function:

```python
def forget_memory(connection, user_id: str, key: str):
    connection.execute(
        "DELETE FROM user_memories WHERE user_id = ? AND memory_key = ?",
        (user_id, key),
    )
    connection.commit()
```

“Forget” request শুধু LLM-কে বললে যথেষ্ট নয়। সংশ্লিষ্ট database/vector store/cache/backup retention policy-তেও deletion process থাকতে হবে। এই tutorial-এর function শুধু নির্দিষ্ট SQLite row delete করে।

## 8. Homework

1. Extractor চালিয়ে project name extract করো।
2. “আজ আমার মন ভালো” ধরনের transient statement পরীক্ষা করো।
3. Password/API key-এর মতো secret extract না হওয়ার পরীক্ষা করো—কোনো real secret ব্যবহার করবে না।
4. Extracted fact SQLite-এ store করো।
5. একই key-এর value update করো।
6. Forget function দিয়ে delete করে যাচাই করো।

## Completion checklist

- [ ] LLM থেকে candidate memory extract করেছি
- [ ] JSON ও field validation করেছি
- [ ] Allowed categories enforce করেছি
- [ ] User-scoped storage বুঝেছি
- [ ] Update ও delete implement করেছি
- [ ] Extraction আর trusted fact এক নয় বুঝেছি
