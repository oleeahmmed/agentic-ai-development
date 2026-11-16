# Chapter 01 — Skill Fundamentals

**সময়:** ৪ ঘণ্টা | **লক্ষ্য:** Skill-এর ধারণা এবং Skill বনাম Tool পরিষ্কারভাবে বোঝা।

## 1. বাস্তব উদাহরণ

ধরো Rahim AI-কে কেউ জিজ্ঞেস করল, “আমাদের অফিস কয়টায় খোলে?” আরেকজন বলল, “আমার জন্য একটা task save করো।”

প্রথম প্রশ্নের জন্য company policy জানা দরকার। দ্বিতীয়টির জন্য task save করার বাস্তব ক্ষমতা দরকার। এ দুটো এক জিনিস নয়।

## 2. Skill কী?

Skill হলো একটি সংগঠিত instruction package। এতে থাকে:
- Skill-এর নাম ও পরিচিতি
- কখন ব্যবহার করতে হবে
- কাজের নিয়ম
- ধাপে ধাপে workflow
- সীমাবদ্ধতা ও উদাহরণ

সাধারণত Markdown ফাইলে রাখা যায়: `SKILL.md`।

## 3. Skill কী নয়?

Skill নিজে Python code চালায় না, Database-এ data লেখে না, Email পাঠায় না, বা File তৈরি করে না। এগুলোর জন্য Tool এবং execution runtime দরকার।

## 4. Skill বনাম Tool

| Skill | Tool |
|---|---|
| নির্দেশনা | Executable function/API |
| কীভাবে কাজ করতে হবে বলে | বাস্তবে কাজ করে |
| `SKILL.md` হতে পারে | Python function হতে পারে |
| নিজে execute করে না | Python runtime execute করে |

উদাহরণ:
- Skill: “Task তৈরির আগে title ও deadline সংগ্রহ করো।”
- Tool: `create_task(title, deadline)`।

## 5. Agent-এর মধ্যে Skill-এর অবস্থান

```text
User request
    |
    v
Agent Controller
    |
    v
Skill Router
    |
    v
Selected Skill instructions
    |
    v
LLM prepares response / proposes next action
    |
    v
If action needed -> Tool request
    |
    v
Python runtime validates and executes Tool
```

এই Phase-এ আমরা Skill discovery ও routing তৈরি করব। Tool execution পরের Tools Engineering Phase-এ হবে।

## 6. Practical — দুটি Skill তৈরি

```bash
cd ~/rahim_ai
mkdir -p skills/company-assistant skills/task-manager
nano skills/company-assistant/SKILL.md
```

লিখো:

```markdown
---
name: company-assistant
description: Answer questions about company information, office hours, working days, and company policies. Use when the user asks about company operations.
---

# Company Assistant Skill

## Role
You are a helpful assistant for ABC Software.

## When to Use
Use for company profile, office hours, working days, and company policies.

## Company Information
- Company: ABC Software
- Office hours: 9:00 AM to 6:00 PM
- Working days: Sunday to Thursday
- Weekly holidays: Friday and Saturday

## Rules
1. Reply in simple Bengali unless asked otherwise.
2. Use only information supplied in this skill.
3. Never invent company policies.
4. If information is missing, say it is unavailable.

## Workflow
1. Understand the company-related question.
2. Find relevant information in this skill.
3. Answer clearly.
4. If information is missing, explain the limitation.
```

দ্বিতীয় Skill:

```bash
nano skills/task-manager/SKILL.md
```

```markdown
---
name: task-manager
description: Help users organize tasks and prepare task details. Use when users ask about creating, viewing, updating, or deleting tasks.
---

# Task Manager Skill

## Role
You help users organize their tasks.

## When to Use
Use for task creation, viewing, updating, and deletion requests.

## Rules
1. Reply in simple Bengali.
2. Collect required task details.
3. Never claim a task was saved unless a real tool confirms success.
4. If no task tool exists, explain that you can prepare details but cannot save them.

## Workflow
1. Understand the requested operation.
2. Identify missing details.
3. Prepare a task summary.
4. If a real task tool is available, request the appropriate action.
5. Report only the actual tool result.
```

## 7. Test

```bash
find skills -name SKILL.md
```

দুটি `SKILL.md` path দেখতে পাবে।

## Homework

1. `hr-policy` নামে তৃতীয় Skill folder তৈরি করো।
2. `SKILL.md`-এ Role, When to Use, Rules, Workflow লেখো।
3. Skill ও Tool-এর পার্থক্য নিজের ভাষায় লেখো।

## Completion checklist

- [ ] Skill কী বুঝেছি
- [ ] Skill বনাম Tool বুঝেছি
- [ ] দুটি Skill file তৈরি করেছি
- [ ] Tool ছাড়া action complete দাবি করিনি
