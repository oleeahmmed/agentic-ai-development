# Chapter 01 — Agent Architecture Fundamentals

## 1. Assistant আর Agent-এর পার্থক্য

সাধারণ assistant:
1. User প্রশ্ন করে।
2. Model উত্তর তৈরি করে।
3. Conversation শেষ।

Agent:
1. User একটি goal দেয়।
2. Agent goal বুঝে।
3. প্রয়োজন হলে plan তৈরি করে।
4. একটি action নির্বাচন করে।
5. Tool execute করে।
6. Result পর্যবেক্ষণ করে।
7. দরকার হলে পরবর্তী action নেয়।
8. Goal পূরণ হলে থামে।

Agent মানে শুধু “LLM + Tool” নয়। Agent-এর controller, state, policy, loop এবং stopping condition-ও লাগে।

## 2. Core components

| Component | দায়িত্ব |
|---|---|
| LLM | ভাষা বোঝা, সিদ্ধান্তের প্রস্তাব, পরিকল্পনা |
| Controller | execution flow ও loop নিয়ন্ত্রণ |
| Tools | বাস্তব কাজ execute |
| State | চলমান কাজের অবস্থা |
| Memory | ভবিষ্যতের জন্য দরকারি তথ্য |
| Skills | নির্দিষ্ট কাজের নির্দেশনা |
| Guardrails | অনুমতি, সীমা ও নিরাপত্তা |
| Evaluator | ফলাফল goal পূরণ করেছে কি না যাচাই |

## 3. Basic architecture diagram

```text
                 +----------------+
                 |      User      |
                 +--------+-------+
                          |
                          v
                 +----------------+
                 | Agent Controller|
                 +--------+-------+
                          |
              +-----------+-----------+
              |                       |
              v                       v
       +-------------+          +-------------+
       |     LLM     |          | Agent State |
       +------+------+          +-------------+
              |
              v
       +-------------+
       | Tool Router |
       +------+------+
              |
       +------+------+
       |             |
       v             v
  Calculator      Task Tool
       |             |
       +------+------+
              |
              v
        Tool Result
              |
              v
       Controller updates state
```

## 4. Agent-এর lifecycle

### Step 1 — Goal intake
User-এর request থেকে goal ও constraints বের করো।

Example:
“একটি project তৈরি করো, তারপর তিনটি task যোগ করো।”

Goal:
- Project তৈরি
- তিনটি task তৈরি
- প্রতিটি task সঠিক project-এর সঙ্গে যুক্ত

### Step 2 — Planning
Goal-কে ছোট, যাচাইযোগ্য ধাপে ভাগ করো।

### Step 3 — Action
পরবর্তী প্রয়োজনীয় tool call করো।

### Step 4 — Observation
Tool result পড়ো। সফল হয়েছে কি না যাচাই করো।

### Step 5 — State update
কোন কাজ complete, কোনটি pending বা failed—তা state-এ রাখো।

### Step 6 — Stop
সব acceptance criteria পূরণ হলে শেষ করো। না হলে পরবর্তী action বা user clarification নাও।

## 5. Python-এ Agent State-এর প্রথম ধারণা

```python
agent_state = {
    "goal": "Create a project and two tasks",
    "status": "in_progress",
    "plan": [
        {"step": 1, "task": "Create project", "status": "pending"},
        {"step": 2, "task": "Create first task", "status": "pending"},
        {"step": 3, "task": "Create second task", "status": "pending"},
    ],
    "tool_calls": 0,
    "errors": [],
}
```

এটি plain Python dictionary। পরের chapter-এ state update function লিখবে।

## 6. Agent autonomy-এর স্তর

- **Level 0:** শুধু উত্তর দেয়।
- **Level 1:** একটি tool call করে।
- **Level 2:** একাধিক tool call করতে পারে।
- **Level 3:** plan করে, tool result দেখে plan update করে।
- **Level 4:** দীর্ঘ workflow চালায়, approval ও checkpoint রাখে।

উচ্চ autonomy মানেই ভালো নয়। কাজের ঝুঁকি অনুযায়ী autonomy নির্ধারণ করতে হবে।

## 7. Hands-on exercise

1. “একটি project বানিয়ে task যোগ করো”—এই goal-এর plan লিখো।
2. প্রতিটি step-এর expected result নির্ধারণ করো।
3. কোন step ব্যর্থ হলে পরের step বন্ধ হবে, তা চিহ্নিত করো।
4. `agent_state` dictionary-তে `created_project_id` যোগ করো।

## 8. Self-check

- Agent controller কেন দরকার?
- Tool এবং Agent-এর পার্থক্য কী?
- Agent কখন থামবে?
- State না রাখলে multi-step workflow-তে কী সমস্যা হবে?

**Chapter outcome:** Agent-এর architecture ও component-গুলোর দায়িত্ব বুঝতে পারবে।
