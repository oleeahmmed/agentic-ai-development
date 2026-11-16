# Chapter 03 — Long-term Memory: JSON & SQLite

**সময়:** ৪ ঘণ্টা  
**লক্ষ্য:** Program restart হলেও memory যেন থাকে—এমন persistent storage তৈরি করা।

## 1. Short-term বনাম Long-term

Short-term memory Python list-এ ছিল। Program বন্ধ হলে সেটি হারিয়ে যায়।

Long-term memory disk-এ save হয়। Program restart করলেও আবার load করা যায়।

এই Chapter-এ প্রথমে JSON, তারপর SQLite ব্যবহার করব।

## 2. JSON memory

JSON হলো structured text format। ছোট learning project-এ সহজে পড়া ও edit করা যায়।

### Practical A — `json_memory.py`

```bash
cd ~/rahim_ai
nano json_memory.py
```

সম্পূর্ণ code:

```python
import json
from pathlib import Path
from datetime import datetime, timezone

MEMORY_FILE = Path(__file__).parent / "memory.json"


def load_memories() -> list[dict]:
    if not MEMORY_FILE.exists():
        return []

    try:
        data = json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError("memory.json contains invalid JSON") from error

    if not isinstance(data, list):
        raise ValueError("Memory file must contain a JSON list")

    return data


def save_memories(memories: list[dict]) -> None:
    temporary_file = MEMORY_FILE.with_suffix(".tmp")

    temporary_file.write_text(
        json.dumps(memories, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    temporary_file.replace(MEMORY_FILE)


def add_memory(key: str, value: str) -> None:
    memories = load_memories()

    memory = {
        "key": key,
        "value": value,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }

    memories = [item for item in memories if item.get("key") != key]
    memories.append(memory)

    save_memories(memories)


def get_memory(key: str) -> dict | None:
    for item in load_memories():
        if item.get("key") == key:
            return item
    return None


def main():
    while True:
        print("\n1. Add/update memory")
        print("2. Read memory")
        print("3. Show all memories")
        print("4. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            key = input("Memory key: ").strip()
            value = input("Memory value: ").strip()

            if key and value:
                add_memory(key, value)
                print("Memory saved.")

        elif choice == "2":
            key = input("Memory key: ").strip()
            print(get_memory(key))

        elif choice == "3":
            print(json.dumps(load_memories(), ensure_ascii=False, indent=2))

        elif choice == "4":
            break


if __name__ == "__main__":
    main()
```

Run:

```bash
python3 json_memory.py
```

উদাহরণ:
- key: `project_name`
- value: `rahim_ai`

Program বন্ধ করে আবার চালিয়ে `project_name` read করো। এবার তথ্য থাকবে।

## 3. JSON-এর সীমাবদ্ধতা

- একসঙ্গে অনেক process write করলে conflict হতে পারে
- বড় data হলে পুরো file পড়া/লেখা ব্যয়বহুল
- relational query সুবিধা সীমিত
- access control ও multi-user separation নিজে design করতে হবে

তাই structured application data-এর জন্য SQLite শিখব।

## 4. SQLite কী?

SQLite হলো lightweight relational database। আলাদা database server চালাতে হয় না; একটি database file-এ data থাকে।

Python-এর `sqlite3` standard library-তেই আছে।

### Practical B — `sqlite_memory.py`

```bash
nano sqlite_memory.py
```

সম্পূর্ণ code:

```python
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path(__file__).parent / "memory.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                memory_key TEXT NOT NULL,
                memory_value TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                UNIQUE(user_id, memory_key)
            )
        """)


def save_memory(user_id: str, key: str, value: str):
    timestamp = datetime.now(timezone.utc).isoformat()

    with get_connection() as connection:
        connection.execute("""
            INSERT INTO memories (
                user_id, memory_key, memory_value, updated_at
            )
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id, memory_key)
            DO UPDATE SET
                memory_value = excluded.memory_value,
                updated_at = excluded.updated_at
        """, (user_id, key, value, timestamp))


def get_memory(user_id: str, key: str):
    with get_connection() as connection:
        row = connection.execute("""
            SELECT memory_key, memory_value, updated_at
            FROM memories
            WHERE user_id = ? AND memory_key = ?
        """, (user_id, key)).fetchone()

    return dict(row) if row else None


def list_memories(user_id: str):
    with get_connection() as connection:
        rows = connection.execute("""
            SELECT memory_key, memory_value, updated_at
            FROM memories
            WHERE user_id = ?
            ORDER BY updated_at DESC
        """, (user_id,)).fetchall()

    return [dict(row) for row in rows]


def delete_memory(user_id: str, key: str):
    with get_connection() as connection:
        connection.execute("""
            DELETE FROM memories
            WHERE user_id = ? AND memory_key = ?
        """, (user_id, key))


def main():
    initialize_database()
    user_id = "demo-user"

    while True:
        print("\n1. Save/update")
        print("2. Read")
        print("3. List")
        print("4. Delete")
        print("5. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            key = input("Key: ").strip()
            value = input("Value: ").strip()
            if key and value:
                save_memory(user_id, key, value)
                print("Saved.")

        elif choice == "2":
            key = input("Key: ").strip()
            print(get_memory(user_id, key))

        elif choice == "3":
            print(list_memories(user_id))

        elif choice == "4":
            key = input("Key: ").strip()
            delete_memory(user_id, key)
            print("Deleted if it existed.")

        elif choice == "5":
            break


if __name__ == "__main__":
    main()
```

চালাও:

```bash
python3 sqlite_memory.py
```

## 5. SQL injection কেন এড়ানো হলো?

দেখো:

```python
connection.execute(
    "SELECT * FROM memories WHERE user_id = ? AND memory_key = ?",
    (user_id, key)
)
```

এখানে `?` placeholder ব্যবহার হয়েছে। User input সরাসরি SQL string-এর সঙ্গে জোড়া লাগানো হয়নি। এটিই parameterized query।

## 6. JSON নাকি SQLite?

| বিষয় | JSON | SQLite |
|---|---|---|
| শুরু করা | খুব সহজ | সহজ |
| Query | সীমিত | SQL |
| Multi-user | নিজে manage | user_id দিয়ে পৃথক করা যায় |
| Concurrent writes | ঝুঁকিপূর্ণ | বেশি নির্ভরযোগ্য |
| Use case | prototype/config | structured persistent data |

## 7. Privacy ও data ownership

বাস্তব system-এ:
- প্রতিটি memory-তে user identity থাকতে হবে
- অন্য user-এর memory access করা যাবে না
- delete request বাস্তবে database-এ প্রয়োগ করতে হবে
- sensitive data সংরক্ষণ এড়িয়ে চলবে
- backup ও retention policy রাখতে হবে

`demo-user` শুধু tutorial placeholder। Production-এ authenticated user ID ব্যবহার করবে; user input থেকে arbitrary user_id বিশ্বাস করবে না।

## Homework

1. JSON file-এ project name save করো।
2. SQLite-এ একই তথ্য save করো।
3. Program restart করে read করো।
4. SQLite-এ দুইটি আলাদা user_id দিয়ে memory save করো এবং নিশ্চিত করো তারা একে অন্যের memory পায় না।
5. একটি memory delete করে আবার read করো।

## Completion checklist

- [ ] JSON persistent memory তৈরি করেছি
- [ ] SQLite database তৈরি করেছি
- [ ] Insert/update/read/delete করেছি
- [ ] Parameterized SQL বুঝেছি
- [ ] User separation বুঝেছি
