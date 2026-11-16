# Chapter 06 — Build a Practical Tool-enabled Agent

এখন calculator ও notes tool একত্র করে একটি ছোট Tool-enabled Assistant তৈরি করব।

## 1. Structure

```text
rahim_ai/
├── .env
├── config.py
├── main.py
└── tools/
    ├── __init__.py
    ├── calculator.py
    ├── notes.py
    └── registry.py
```

## 2. `config.py`

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

## 3. `tools/calculator.py`

```python
def add_numbers(a: float, b: float) -> float:
    """দুটি সংখ্যা যোগ করে।"""
    return a + b

def subtract_numbers(a: float, b: float) -> float:
    """প্রথম সংখ্যা থেকে দ্বিতীয় সংখ্যা বিয়োগ করে।"""
    return a - b

def multiply_numbers(a: float, b: float) -> float:
    """দুটি সংখ্যা গুণ করে।"""
    return a * b

def divide_numbers(a: float, b: float) -> float:
    """প্রথম সংখ্যাকে দ্বিতীয় সংখ্যা দিয়ে ভাগ করে।"""
    if b == 0:
        raise ValueError("শূন্য দিয়ে ভাগ করা যায় না।")
    return a / b
```

## 4. `tools/notes.py`

```python
from pathlib import Path

NOTES_FILE = Path("notes.txt")

def save_note(note: str) -> str:
    """একটি note সংরক্ষণ করে।"""
    if not isinstance(note, str):
        raise TypeError("Note text হতে হবে।")
    note = note.strip()
    if not note:
        raise ValueError("খালি note save করা যাবে না।")
    if len(note) > 2000:
        raise ValueError("Note ২০০০ character-এর মধ্যে রাখো।")
    with NOTES_FILE.open("a", encoding="utf-8") as file:
        file.write(note + "\\n")
    return "Note saved."

def read_notes() -> str:
    """সব note পড়ে।"""
    if not NOTES_FILE.exists():
        return "No notes found."
    return NOTES_FILE.read_text(encoding="utf-8")
```

## 5. `tools/registry.py`

```python
from tools.calculator import (
    add_numbers, subtract_numbers, multiply_numbers, divide_numbers
)
from tools.notes import save_note, read_notes

TOOL_REGISTRY = {
    "add_numbers": add_numbers,
    "subtract_numbers": subtract_numbers,
    "multiply_numbers": multiply_numbers,
    "divide_numbers": divide_numbers,
    "save_note": save_note,
    "read_notes": read_notes,
}

def execute_tool(tool_name: str, arguments: dict):
    if tool_name not in TOOL_REGISTRY:
        raise ValueError(f"Tool অনুমোদিত নয়: {tool_name}")
    if not isinstance(arguments, dict):
        raise TypeError("Arguments object হতে হবে।")
    return TOOL_REGISTRY[tool_name](**arguments)
```

## 6. `main.py` — Complete Agent

```python
import json
from config import client
from tools.registry import execute_tool

MODEL = "gpt-4.1-mini"
MAX_TOOL_ROUNDS = 5

TOOLS = [
    {
        "type": "function",
        "name": "add_numbers",
        "description": "দুটি সংখ্যা যোগ করে।",
        "parameters": {
            "type": "object",
            "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
            "required": ["a", "b"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "subtract_numbers",
        "description": "প্রথম সংখ্যা থেকে দ্বিতীয় সংখ্যা বিয়োগ করে।",
        "parameters": {
            "type": "object",
            "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
            "required": ["a", "b"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "multiply_numbers",
        "description": "দুটি সংখ্যা গুণ করে।",
        "parameters": {
            "type": "object",
            "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
            "required": ["a", "b"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "divide_numbers",
        "description": "প্রথম সংখ্যাকে দ্বিতীয় সংখ্যা দিয়ে ভাগ করে।",
        "parameters": {
            "type": "object",
            "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
            "required": ["a", "b"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "save_note",
        "description": "ব্যবহারকারীর দেওয়া text note সংরক্ষণ করে।",
        "parameters": {
            "type": "object",
            "properties": {"note": {"type": "string"}},
            "required": ["note"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "read_notes",
        "description": "আগে সংরক্ষিত note-গুলো পড়ে।",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
        "strict": True,
    },
]

def run_agent(user_message: str) -> str:
    response = client.responses.create(
        model=MODEL,
        instructions=(
            "তুমি একটি সহায়ক assistant। হিসাবের জন্য calculator tool ব্যবহার করো। "
            "Note save বা read করতে বললে সংশ্লিষ্ট tool ব্যবহার করো। "
            "Tool result না পেয়ে কাজ সম্পন্ন হয়েছে বলবে না।"
        ),
        input=user_message,
        tools=TOOLS,
    )

    for _ in range(MAX_TOOL_ROUNDS):
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
                payload = {"success": False, "error": str(error)}

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

    return "Tool round limit শেষ হয়েছে। কাজটি ছোট ধাপে বলো।"


def main():
    print("Rahim AI Tool Agent")
    print("বন্ধ করতে 'exit' লিখো।")

    while True:
        user_message = input("\\nYou: ").strip()

        if user_message.lower() in {"exit", "quit"}:
            print("Agent: বিদায়!")
            break

        if not user_message:
            continue

        try:
            print("\\nAgent:", run_agent(user_message))
        except Exception as error:
            print("\\nAgent Error:", error)


if __name__ == "__main__":
    main()
```

## 7. Run and test

```bash
python main.py
```

পরীক্ষা:
```text
You: ২৫০ এবং ৭৫০ যোগ করো।
You: আমার নোটে লিখে রাখো, আগামীকাল Python practice করব।
You: আমার নোটগুলো দেখাও।
You: ১০০ কে ৪ দিয়ে ভাগ করো।
```

Model প্রয়োজনমতো tool নির্বাচন করবে। Tool execute না হলে সফল হয়েছে দাবি করা যাবে না।

## 8. Production checklist
- Per-user authentication ও authorization
- Database storage এবং transaction
- Tool input/output validation
- Destructive action-এর confirmation
- Timeout, retry ও rate limiting
- Structured logging ও audit log
- Secrets management
- Unit ও integration tests
- Per-tool permission এবং allowlist
- Sensitive data redaction

এটি learning prototype, production-ready system নয়।

## 9. Final exercises
1. `get_current_time` tool যোগ করো।
2. প্রতিটি tool-এর unit test লেখো।
3. `save_note`-এ user_id যোগ করে user অনুযায়ী note আলাদা করো।
4. `delete_note` যোগ করার আগে confirmation design করো।
5. Tool call সংখ্যা ও execution duration log করো।

## 10. Completion checklist
- [ ] Tool ও Skill-এর পার্থক্য বুঝি।
- [ ] Python function registry তৈরি করতে পারি।
- [ ] Native function schema লিখতে পারি।
- [ ] Model-এর function call parse করতে পারি।
- [ ] Function execute করে result ফেরত দিতে পারি।
- [ ] একাধিক tool call handle করতে পারি।
- [ ] Error ও tool round limit handle করতে পারি।
- [ ] Tool security-এর মৌলিক ঝুঁকি বুঝি।

**Phase 04 শেষ।** পরবর্তী Phase 05-এ Agent Loop, ReAct, Planning, task decomposition ও orchestration শেখা হবে।
