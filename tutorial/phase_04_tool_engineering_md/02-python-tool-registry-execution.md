# Chapter 02 — Python Tool Registry & Execution

এই Chapter-এ একাধিক Python function-কে registry-তে রাখব এবং নাম দিয়ে নিরাপদভাবে execute করব।

## 1. Structure

```text
rahim_ai/
├── main.py
└── tools/
    ├── __init__.py
    ├── calculator.py
    └── registry.py
```

```bash
mkdir -p tools
touch tools/__init__.py
```

## 2. Calculator tools

`tools/calculator.py`:

```python
def add_numbers(a: float, b: float) -> float:
    """দুটি সংখ্যার যোগফল বের করে।"""
    return a + b


def subtract_numbers(a: float, b: float) -> float:
    """প্রথম সংখ্যা থেকে দ্বিতীয় সংখ্যা বিয়োগ করে।"""
    return a - b


def multiply_numbers(a: float, b: float) -> float:
    """দুটি সংখ্যার গুণফল বের করে।"""
    return a * b


def divide_numbers(a: float, b: float) -> float:
    """প্রথম সংখ্যাকে দ্বিতীয় সংখ্যা দিয়ে ভাগ করে।"""
    if b == 0:
        raise ValueError("শূন্য দিয়ে ভাগ করা যায় না।")
    return a / b
```

## 3. Registry

`tools/registry.py`:

```python
from tools.calculator import (
    add_numbers,
    subtract_numbers,
    multiply_numbers,
    divide_numbers,
)

TOOL_REGISTRY = {
    "add_numbers": add_numbers,
    "subtract_numbers": subtract_numbers,
    "multiply_numbers": multiply_numbers,
    "divide_numbers": divide_numbers,
}


def execute_tool(tool_name: str, arguments: dict):
    """Allowlist registry থেকে tool execute করে।"""
    tool_function = TOOL_REGISTRY.get(tool_name)

    if tool_function is None:
        raise ValueError(f"Unknown tool: {tool_name}")

    if not isinstance(arguments, dict):
        raise TypeError("Tool arguments dictionary হতে হবে।")

    return tool_function(**arguments)
```

## 4. Test without AI

`main.py`:

```python
from tools.registry import execute_tool

def main():
    result = execute_tool("add_numbers", {"a": 12, "b": 8})
    print("Tool result:", result)

if __name__ == "__main__":
    main()
```

```bash
python main.py
```

Expected: `Tool result: 20`

## 5. Unknown tool

```python
execute_tool("delete_everything", {})
```

এটি `ValueError: Unknown tool` দেবে। Registry হলো allowlist; অচেনা function execute হবে না।

## 6. Error handling

```python
from tools.registry import execute_tool

try:
    result = execute_tool("divide_numbers", {"a": 10, "b": 0})
    print(result)
except (ValueError, TypeError, KeyError) as error:
    print("Tool failed:", error)
```

## 7. Production considerations
- প্রতিটি argument-এর schema validate করো।
- Tool execution timeout রাখো।
- Side-effect tool-এ confirmation ও permission রাখো।
- Sensitive data log করবে না।

## 8. Exercise
1. `get_tool_names()` লেখো।
2. `power_numbers(a, b)` যোগ করো।
3. Unknown tool এবং missing argument পরীক্ষা করো।

**Outcome:** AI ছাড়াই Python tool registry ও execution flow বুঝতে পারবে।
