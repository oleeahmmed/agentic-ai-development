# Chapter 04 — Multiple Tools, Arguments & Validation

একটি বাস্তব agent-এর একাধিক tool লাগে। এখানে calculator-এর পাশাপাশি note save ও read tool যোগ করব।

## 1. Note tools

`tools/notes.py`:

```python
from pathlib import Path

NOTES_FILE = Path("notes.txt")

def save_note(note: str) -> str:
    """একটি সাধারণ text note ফাইলে যোগ করে।"""
    if not isinstance(note, str):
        raise TypeError("note অবশ্যই text হতে হবে।")

    note = note.strip()
    if not note:
        raise ValueError("খালি note save করা যাবে না।")
    if len(note) > 2000:
        raise ValueError("Note সর্বোচ্চ ২০০০ character হতে পারবে।")

    with NOTES_FILE.open("a", encoding="utf-8") as file:
        file.write(note + "\\n")

    return "নোট সংরক্ষণ করা হয়েছে।"


def read_notes() -> str:
    """সংরক্ষিত সব note পড়ে।"""
    if not NOTES_FILE.exists():
        return "এখনো কোনো note নেই।"
    return NOTES_FILE.read_text(encoding="utf-8")
```

এটি learning example। Production app-এ user-specific storage, access control, database ও audit trail ব্যবহার করবে।

## 2. Registry update

`tools/registry.py`:

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
    function = TOOL_REGISTRY.get(tool_name)
    if function is None:
        raise ValueError(f"Unknown tool: {tool_name}")
    if not isinstance(arguments, dict):
        raise TypeError("Arguments অবশ্যই dictionary হতে হবে।")
    return function(**arguments)
```

## 3. Native tool schemas

`main.py`-তে tools list-এর মধ্যে এগুলো যোগ করো:

```python
{
    "type": "function",
    "name": "save_note",
    "description": "ব্যবহারকারীর দেওয়া সাধারণ text note সংরক্ষণ করে।",
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
    "description": "সংরক্ষিত note-গুলো পড়ে।",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False,
    },
    "strict": True,
}
```

`read_notes`-এর input নেই, তাই empty object পাঠানো হবে।

## 4. Validation-এর স্তর

JSON schema validation উপকারী, কিন্তু Python function-এর ভেতরেও validation রাখবে:
- Input string কি না
- Empty কি না
- Maximum length অতিক্রম করেছে কি না
- User-এর permission আছে কি না
- Resource-টি ঐ user-এর মালিকানাধীন কি না

## 5. Security warning

এমন unrestricted tool দেবে না:

```python
def read_file(path):
    return open(path).read()
```

এতে sensitive file পড়ার ঝুঁকি আছে। নির্দিষ্ট directory allowlist, path normalization ও permission check ছাড়া file access দেবে না।

## 6. Exercise
1. `count_notes()` লেখো।
2. ২০০০ character limit পরীক্ষা করো।
3. Unknown tool execute করে error দেখো।
4. `read_notes`-এ empty arguments পাঠাও।

**Outcome:** একাধিক tool schema, registry ও validation পরিচালনা করতে পারবে।
