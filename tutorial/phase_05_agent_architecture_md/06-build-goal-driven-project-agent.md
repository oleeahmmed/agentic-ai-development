# Chapter 06 — Build a Goal-driven Project Agent

এই capstone-এ একটি ছোট Project Agent তৈরি করবে। Agent একটি goal পাবে, plan তৈরি করবে, project ও task tool ব্যবহার করবে এবং state update করবে।

এই tutorial-এ storage হিসেবে SQLite ব্যবহার করা হয়েছে। এটি learning prototype; production-এ authentication, authorization, migrations, audit ও stronger validation দরকার।

## 1. Project structure

```text
rahim_ai/
├── .env
├── config.py
├── main.py
├── agent/
│   ├── __init__.py
│   ├── controller.py
│   └── planner.py
└── tools/
    ├── __init__.py
    ├── project_tools.py
    └── registry.py
```

```bash
mkdir -p agent tools
touch agent/__init__.py tools/__init__.py
```

## 2. Database tools

`tools/project_tools.py`:

```python
import sqlite3
from pathlib import Path

DB_PATH = Path("projects.db")


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT NOT NULL DEFAULT ''
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                FOREIGN KEY(project_id) REFERENCES projects(id)
            )
        """)


def create_project(name: str, description: str = "") -> dict:
    name = name.strip()
    if len(name) < 3:
        raise ValueError("Project name কমপক্ষে ৩ character হতে হবে।")

    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO projects (name, description) VALUES (?, ?)",
            (name, description.strip()),
        )
        project_id = cursor.lastrowid

    return {"project_id": project_id, "name": name}


def create_task(project_id: int, title: str) -> dict:
    title = title.strip()
    if not title:
        raise ValueError("Task title খালি হতে পারবে না।")

    with get_connection() as connection:
        project = connection.execute(
            "SELECT id FROM projects WHERE id = ?",
            (project_id,),
        ).fetchone()

        if project is None:
            raise ValueError("Project পাওয়া যায়নি।")

        cursor = connection.execute(
            "INSERT INTO tasks (project_id, title) VALUES (?, ?)",
            (project_id, title),
        )

        task_id = cursor.lastrowid

    return {
        "task_id": task_id,
        "project_id": project_id,
        "title": title,
    }


def list_project_tasks(project_id: int) -> list:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, title, status
            FROM tasks
            WHERE project_id = ?
            ORDER BY id
            """,
            (project_id,),
        ).fetchall()

    return [dict(row) for row in rows]
```

## 3. Registry

`tools/registry.py`:

```python
from tools.project_tools import (
    create_project,
    create_task,
    list_project_tasks,
)

TOOL_REGISTRY = {
    "create_project": create_project,
    "create_task": create_task,
    "list_project_tasks": list_project_tasks,
}


def execute_tool(name: str, arguments: dict):
    function = TOOL_REGISTRY.get(name)

    if function is None:
        raise ValueError(f"অনুমোদিত নয় এমন tool: {name}")

    if not isinstance(arguments, dict):
        raise TypeError("Tool arguments object হতে হবে।")

    return function(**arguments)
```

## 4. Tool schemas

`agent/controller.py`-তে:

```python
TOOLS = [
    {
        "type": "function",
        "name": "create_project",
        "description": "নতুন project তৈরি করে।",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "description": {"type": "string"},
            },
            "required": ["name", "description"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "create_task",
        "description": "একটি project-এর মধ্যে task তৈরি করে।",
        "parameters": {
            "type": "object",
            "properties": {
                "project_id": {"type": "integer"},
                "title": {"type": "string"},
            },
            "required": ["project_id", "title"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "list_project_tasks",
        "description": "নির্দিষ্ট project-এর task তালিকা দেখায়।",
        "parameters": {
            "type": "object",
            "properties": {
                "project_id": {"type": "integer"},
            },
            "required": ["project_id"],
            "additionalProperties": False,
        },
        "strict": True,
    },
]
```

## 5. Controller

`config.py`:

```python
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("OPENAI_API_KEY পাওয়া যায়নি।")

client = OpenAI(api_key=api_key)
```

`agent/controller.py`-এর বাকি অংশ:

```python
import json

from config import client
from tools.registry import execute_tool
from tools.project_tools import initialize_database

MODEL = "gpt-4.1-mini"
MAX_ROUNDS = 6

TOOLS = [
    {
        "type": "function",
        "name": "create_project",
        "description": "নতুন project তৈরি করে।",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "description": {"type": "string"},
            },
            "required": ["name", "description"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "create_task",
        "description": "একটি project-এর মধ্যে task তৈরি করে।",
        "parameters": {
            "type": "object",
            "properties": {
                "project_id": {"type": "integer"},
                "title": {"type": "string"},
            },
            "required": ["project_id", "title"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "list_project_tasks",
        "description": "নির্দিষ্ট project-এর task তালিকা দেখায়।",
        "parameters": {
            "type": "object",
            "properties": {
                "project_id": {"type": "integer"},
            },
            "required": ["project_id"],
            "additionalProperties": False,
        },
        "strict": True,
    },
]


def run_agent(goal: str) -> str:
    initialize_database()

    response = client.responses.create(
        model=MODEL,
        instructions=(
            "তুমি project management agent। User-এর goal পূরণে project ও task tools ব্যবহার করো. "
            "Project তৈরি না করে task তৈরি করবে না। Tool result না পেলে success দাবি করবে না। "
            "যদি project name বা task details অস্পষ্ট হয়, clarification চাইবে। "
            "প্রয়োজনীয় কাজ শেষে created project ও task-এর summary দেবে।"
        ),
        input=goal,
        tools=TOOLS,
    )

    for _ in range(MAX_ROUNDS):
        calls = [
            item for item in response.output
            if item.type == "function_call"
        ]

        if not calls:
            return response.output_text

        outputs = []

        for call in calls:
            try:
                arguments = json.loads(call.arguments)
                result = execute_tool(call.name, arguments)
                payload = {"success": True, "result": result}
            except Exception as error:
                payload = {
                    "success": False,
                    "error": str(error),
                }

            outputs.append({
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": json.dumps(payload, ensure_ascii=False),
            })

        response = client.responses.create(
            model=MODEL,
            previous_response_id=response.id,
            input=outputs,
            tools=TOOLS,
        )

    return "Agent নির্ধারিত tool round limit-এ পৌঁছেছে।"


def main():
    print("Goal-driven Project Agent")
    print("বন্ধ করতে exit লিখো।")

    while True:
        goal = input("\\nতোমার Goal: ").strip()

        if goal.lower() in {"exit", "quit"}:
            break

        if not goal:
            continue

        try:
            print("\\nAgent:", run_agent(goal))
        except Exception as error:
            print("Error:", error)


if __name__ == "__main__":
    main()
```

## 6. Entry point

Root `main.py`:

```python
from agent.controller import main

if __name__ == "__main__":
    main()
```

## 7. Run

```bash
python main.py
```

উদাহরণ goal:

```text
একটি project তৈরি করো। নাম হবে Website Redesign।
Description হবে company website redesign করা।
এই project-এ তিনটি task তৈরি করো:
1. Requirement collect
2. UI design
3. Frontend development
```

Model project tool call করবে, returned project ID ব্যবহার করে task তৈরি করবে এবং শেষে summary দেবে।

## 8. Important limitation

এই capstone একটি learning prototype:
- SQLite connection-এ foreign key enforcement explicitly enable করা হয়নি; production-এ `PRAGMA foreign_keys = ON` প্রয়োগ করো।
- একই goal পুনরায় পাঠালে duplicate project/task হতে পারে; idempotency ও duplicate detection যোগ করো।
- এখানে user authentication ও company-level authorization নেই।
- Tool call-এর আগে user confirmation workflow নেই।
- Plan ও state process memory-তে; restart হলে execution resume হবে না।
- Model-এর tool-call sequence-কে trusted ধরে নেওয়া যাবে না; প্রতিটি call-এ permission ও business-rule validation প্রয়োজন।

## 9. Final exercises

1. Project duplicate হলে existing project ID ফেরত দেওয়ার design করো।
2. `get_project` tool যোগ করো।
3. Agent state-এ `goal`, `plan`, `completed_steps`, `tool_calls` রাখো।
4. Project creation-এর আগে confirmation যোগ করো।
5. `MAX_ROUNDS` ছাড়াও wall-clock timeout design করো।
6. Tool call history SQLite-এ সংরক্ষণ করো।

## 10. Phase 05 completion checklist

- [ ] Agent architecture-এর component বুঝি।
- [ ] Bounded agent loop লিখতে পারি।
- [ ] ReAct-এর action/observation cycle বুঝি।
- [ ] Goal-কে task ও subtask-এ ভাগ করতে পারি।
- [ ] Dependency-aware plan validate করতে পারি।
- [ ] State ও context আলাদা করতে পারি।
- [ ] Tool result অনুযায়ী state update করতে পারি।
- [ ] Goal-driven tool agent তৈরি করতে পারি।

**Phase 05 সম্পন্ন।** পরবর্তী Phase 06-এ production agent engineering: security, retries, async, logging, testing ও MCP শিখবে।
