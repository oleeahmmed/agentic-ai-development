# Chapter 04 — Planning & Task Decomposition

বড় goal সরাসরি execute করা কঠিন। Planning-এর মাধ্যমে goal-কে ছোট, নির্ভরশীল ও যাচাইযোগ্য task-এ ভাগ করা হয়।

## 1. Goal, task ও subtask

Goal:
“একটি ছোট website project তৈরি করে কাজগুলো assign করার জন্য প্রস্তুত করো।”

Task:
- Project information সংগ্রহ
- Project তৈরি
- প্রয়োজনীয় task তৈরি
- Task details যাচাই

Subtask:
- Project name validate
- Description তৈরি
- Project tool call
- Returned project ID সংরক্ষণ

## 2. Dependency graph

```text
Collect requirements
        |
        v
Validate project details
        |
        v
Create project
        |
        v
Receive project_id
        |
   +----+----+
   |         |
   v         v
Create task A  Create task B
   |         |
   +----+----+
        |
        v
Verify created tasks
        |
        v
Final summary
```

Task A ও B তৈরি করতে project ID প্রয়োজন। তাই project তৈরি হওয়ার আগে task creation করা যাবে না।

## 3. Plan data structure

```python
plan = [
    {
        "id": "step_1",
        "description": "Validate project details",
        "depends_on": [],
        "status": "pending",
        "required_tool": None,
    },
    {
        "id": "step_2",
        "description": "Create project",
        "depends_on": ["step_1"],
        "status": "pending",
        "required_tool": "create_project",
    },
    {
        "id": "step_3",
        "description": "Create task A",
        "depends_on": ["step_2"],
        "status": "pending",
        "required_tool": "create_task",
    },
]
```

## 4. Ready tasks বের করা

```python
def get_ready_tasks(plan: list) -> list:
    completed_ids = {
        task["id"]
        for task in plan
        if task["status"] == "completed"
    }

    ready = []

    for task in plan:
        if task["status"] != "pending":
            continue

        dependencies_done = all(
            dependency in completed_ids
            for dependency in task["depends_on"]
        )

        if dependencies_done:
            ready.append(task)

    return ready


if __name__ == "__main__":
    sample_plan = [
        {
            "id": "a",
            "description": "Validate",
            "depends_on": [],
            "status": "completed",
        },
        {
            "id": "b",
            "description": "Create project",
            "depends_on": ["a"],
            "status": "pending",
        },
        {
            "id": "c",
            "description": "Create task",
            "depends_on": ["b"],
            "status": "pending",
        },
    ]

    print(get_ready_tasks(sample_plan))
```

Expected: শুধু `Create project` ready হবে।

## 5. Plan validation

Plan execute করার আগে:
- প্রতিটি task-এর unique ID আছে কি?
- Dependency ID বাস্তবে আছে কি?
- Task নিজেকেই dependency করেছে কি?
- Circular dependency আছে কি?
- প্রতিটি action-এর জন্য অনুমোদিত tool আছে কি?
- Goal-এর completion criteria আছে কি?

শুধু model-generated plan বিশ্বাস করবে না। Python-এ validate করবে।

## 6. Replanning

পরিকল্পনা সবসময় ঠিক হবে না। যেমন:
- Project name আগে থেকেই আছে।
- Tool error দিয়েছে।
- User requirement বদলেছে।
- Task create করার permission নেই।

তখন:
1. বর্তমান state পড়ো।
2. Completed কাজগুলো অক্ষত রাখো।
3. Failed step ও কারণ চিহ্নিত করো।
4. নতুন plan তৈরি বা পুরোনো plan সংশোধন করো।
5. Dependency আবার validate করো।

## 7. Acceptance criteria

Goal complete বলার আগে measurable criteria রাখো।

উদাহরণ:
- Project ID পাওয়া গেছে।
- প্রত্যাশিত সংখ্যক task তৈরি হয়েছে।
- প্রতিটি task সঠিক project ID-এর সঙ্গে যুক্ত।
- Tool result-এ success পাওয়া গেছে।

## 8. Exercise

1. “একটি project এবং তিনটি task তৈরি” goal-এর plan লেখো।
2. Dependency graph আঁকো।
3. `get_ready_tasks()` চালিয়ে দেখো।
4. Project creation fail করলে task creation আটকে দাও।
5. Completion criteria লিখে verification function তৈরি করো।

**Chapter outcome:** বড় goal-কে dependency-aware, testable task-এ ভাঙতে পারবে।
