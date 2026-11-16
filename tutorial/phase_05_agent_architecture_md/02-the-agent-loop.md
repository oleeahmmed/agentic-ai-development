# Chapter 02 — The Agent Loop

এই Chapter-এ Agent-এর সবচেয়ে গুরুত্বপূর্ণ execution pattern শিখবে: Observe → Decide → Act → Observe।

## 1. Loop কী?

Agent একটি goal পেয়ে একবারেই সব কাজ করে না। Controller একটি bounded loop চালায়।

```text
        +------------------+
        | Read current state|
        +---------+--------+
                  |
                  v
        +------------------+
        | Ask model next step|
        +---------+--------+
                  |
                  v
        +------------------+
        | Tool call needed? |
        +----+---------+---+
             |         |
            Yes        No
             |         |
             v         v
        Execute tool  Final answer
             |
             v
        Observe result
             |
             v
        Update state
             |
             +-------> loop again
```

## 2. কেন bounded loop?

একটি model বারবার tool call চাইতে পারে। Loop limit না থাকলে:
- API cost বাড়তে পারে
- একই কাজ বারবার হতে পারে
- ভুল tool call চলতে পারে
- Agent কখনো শেষ নাও হতে পারে

তাই `MAX_STEPS` বা `MAX_TOOL_ROUNDS` রাখবে।

## 3. Simple controller without LLM

প্রথমে LLM ছাড়া loop বোঝো:

```python
tasks = [
    {"name": "Create project", "status": "pending"},
    {"name": "Create task A", "status": "pending"},
    {"name": "Create task B", "status": "pending"},
]

MAX_STEPS = 5

for step_number, task in enumerate(tasks, start=1):
    if step_number > MAX_STEPS:
        print("Step limit reached")
        break

    print("Working on:", task["name"])

    # এখানে বাস্তবে সংশ্লিষ্ট tool call হবে।
    task["status"] = "completed"

    print("Status:", task["status"])

print("Final state:", tasks)
```

## 4. Reusable state update

```python
def update_step_status(plan: list, step_number: int, status: str) -> list:
    allowed_statuses = {"pending", "in_progress", "completed", "failed"}

    if status not in allowed_statuses:
        raise ValueError("Invalid status")

    for step in plan:
        if step["step"] == step_number:
            step["status"] = status
            return plan

    raise ValueError(f"Step {step_number} not found")


plan = [
    {"step": 1, "task": "Create project", "status": "pending"},
    {"step": 2, "task": "Create task", "status": "pending"},
]

update_step_status(plan, 1, "completed")
print(plan)
```

## 5. Agent loop-এর pseudocode

```python
state = initialize_state(user_goal)

for step in range(MAX_STEPS):
    decision = ask_model(state)

    if decision["type"] == "final":
        return decision["message"]

    if decision["type"] == "tool_call":
        result = execute_allowed_tool(decision)
        state = update_state(state, decision, result)
        continue

    if decision["type"] == "need_user_input":
        return ask_user(decision["question"])

return "আমি নির্ধারিত step limit-এ পৌঁছেছি।"
```

এটি architecture pseudocode; `ask_model`, `execute_allowed_tool` ইত্যাদি বাস্তব function পরে implement করতে হবে।

## 6. Failure policy

Tool fail করলে সবসময় একইভাবে retry করবে না।

- Temporary network error: সীমিত retry করা যায়।
- Invalid arguments: model-কে error জানিয়ে সংশোধিত arguments চাইতে পারো।
- Permission denied: retry নয়; user/admin approval লাগবে।
- Resource not found: state update করে plan revise করতে হবে।
- Destructive operation: explicit confirmation ছাড়া execute নয়।

## 7. Stop conditions

Agent থামবে যখন:
- Goal-এর acceptance criteria পূরণ হয়েছে।
- User-এর clarification বা approval দরকার।
- Step/tool/time budget শেষ।
- নিরাপত্তার কারণে কাজ বন্ধ করতে হয়েছে।
- পুনরাবৃত্ত failure থেকে recover করা যাচ্ছে না।

## 8. Exercise

1. `MAX_STEPS = 3` দিয়ে task loop চালাও।
2. একটি task-কে ইচ্ছাকৃতভাবে failed করো।
3. failed task থাকলে পরের dependent task যেন execute না হয়, এমন logic লেখো।
4. loop শেষ হওয়ার কারণ state-এ রাখো (`completed`, `needs_input`, `limit_reached`)।

**Chapter outcome:** Agent controller-এর bounded execution loop লিখতে পারবে।
