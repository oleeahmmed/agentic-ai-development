# Phase 05 — Agent Architecture, Agent Loop, ReAct & Planning

এই Phase-এ Tool ব্যবহার করতে পারে এমন Assistant-কে ধাপে ধাপে Agent হিসেবে গড়ে তুলবে। Agent শুধু একবার উত্তর দেয় না; প্রয়োজন অনুযায়ী লক্ষ্য বোঝে, কাজ ভাগ করে, tool ব্যবহার করে, ফলাফল যাচাই করে এবং পরবর্তী পদক্ষেপ নেয়।

## Chapters
1. Agent Architecture Fundamentals
2. The Agent Loop
3. ReAct Pattern — Reasoning and Acting
4. Planning & Task Decomposition
5. State, Context & Orchestration
6. Build a Goal-driven Project Agent

## Prerequisites
- Phase 01: LLM/API fundamentals
- Phase 02: Skill Engineering
- Phase 03: Memory Engineering
- Phase 04: Tool Engineering & Native Tool Calling
- Python basics, functions, dictionaries, JSON, exceptions

## Environment

আগের `rahim_ai` project ব্যবহার করো:

```bash
cd ~/rahim_ai
source venv/bin/activate
pip install --upgrade openai python-dotenv
```

`.env`:
```env
OPENAI_API_KEY=your_api_key_here
```

## Target architecture

```text
User Goal
   |
   v
Agent Controller
   |
   +--> Understand goal
   |
   +--> Create / update plan
   |
   +--> Select next action
   |
   +--> Call an allowed tool
   |
   +--> Observe tool result
   |
   +--> Update state
   |
   +--> Continue or finish
   |
   v
Final response
```

## Important distinction

- **LLM:** ভাষা বোঝে, সিদ্ধান্তের প্রস্তাব দেয়, plan তৈরি করে।
- **Agent controller:** loop, state, limits ও execution নিয়ন্ত্রণ করে।
- **Tools:** বাস্তব কাজ করে।
- **Memory:** প্রয়োজনীয় তথ্য সংরক্ষণ ও পুনরুদ্ধার করে।
- **Skills:** কাজের নিয়ম ও workflow নির্দেশ করে।

Agent-কে সম্পূর্ণ স্বাধীন করে দেবে না। Tool allowlist, permission, round limit, timeout এবং user confirmation রাখতে হবে।

## Learning outcome
Phase শেষে তুমি একটি goal-driven agent তৈরি করতে পারবে, যেটি plan বানায়, একাধিক tool ব্যবহার করে, state update করে এবং নির্দিষ্ট সীমার মধ্যে কাজ শেষ করে।
