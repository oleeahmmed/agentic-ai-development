# Chapter 01 — Tool Engineering Fundamentals

## 1. Tool কেন দরকার?

LLM ভাষা বুঝতে, পরিকল্পনা করতে ও উত্তর লিখতে পারে। কিন্তু শুধু prompt দিয়ে তোমার computer-এর calculator, database বা filesystem-এ বাস্তব কাজ করতে পারে না। Tool হলো application-এর লেখা একটি নির্দিষ্ট function, যেটি model প্রয়োজন হলে ব্যবহার করার অনুরোধ করে।

উদাহরণ: `calculate`, `get_current_time`, `save_note`, `search_employee`, `create_task`।

## 2. Architecture

```text
User -> Python Application -> LLM
              ^                |
              |<-- tool call --|
              |
        Validate arguments
              |
        Execute Python function
              |
        Tool result -> LLM -> Final answer
```

Model সিদ্ধান্ত ও arguments তৈরি করে। Function execute করে Python application।

## 3. Skill বনাম Tool

| বিষয় | Skill | Tool |
|---|---|---|
| কাজ | কাজের নিয়ম শেখায় | বাস্তব কাজ execute করে |
| ধরন | Instructions / workflow | Python function / API |
| উদাহরণ | task তৈরির নিয়ম | `create_task()` |
| নিজে action করে? | না | হ্যাঁ |

Skill বলতে পারে কখন `create_task` ব্যবহার করতে হবে। কিন্তু function না থাকলে task তৈরি হবে না।

## 4. প্রথম Python Tool

`calculator.py`:

```python
def add_numbers(a: float, b: float) -> float:
    """দুটি সংখ্যার যোগফল ফেরত দেয়।"""
    return a + b


if __name__ == "__main__":
    print("Result:", add_numbers(10, 25))
```

চালাও:

```bash
python calculator.py
```

Expected output: `Result: 35`

এটি এখনো সাধারণ Python function, AI tool নয়।

## 5. Tool Contract

প্রতিটি tool-এর contract নির্দিষ্ট করো:
1. নাম: `add_numbers`
2. কাজ: দুটি সংখ্যা যোগ করা
3. Input: `a`, `b`
4. Type: number
5. Output: number
6. Failure: invalid input হলে পরিষ্কার error

একটি tool ছোট ও একক দায়িত্বের হওয়া ভালো। `calculate_and_save_and_email()` না বানিয়ে আলাদা function রাখো।

## 6. Exercise
- `subtract_numbers(a, b)` লেখো।
- `multiply_numbers(a, b)` লেখো।
- `divide_numbers(a, b)` লেখো এবং শূন্য দিয়ে ভাগের error handle করো।
- প্রতিটি function-এ type hint ও docstring দাও।

## 7. Self-check
- LLM কি নিজে Python function execute করে?
- Tool definition ও implementation-এর পার্থক্য কী?
- Skill কেন Tool-এর বিকল্প নয়?

**লক্ষ্য:** AI application-এ model ও Python application-এর দায়িত্ব আলাদা করে বোঝা।
