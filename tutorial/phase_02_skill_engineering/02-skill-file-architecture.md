# Chapter 02 — Skill File Architecture

**সময়:** ৪ ঘণ্টা | **লক্ষ্য:** Skill-কে maintainable folder-based package হিসেবে সাজানো।

## 1. Folder-based design কেন?

একটি Skill-এর instruction বড় হলে reference, examples বা templates দরকার হতে পারে। তাই প্রতিটি Skill-এর আলাদা folder রাখব।

```text
skills/
├── company-assistant/
│   ├── SKILL.md
│   ├── references/
│   │   └── company-policy.md
│   └── examples/
│       └── sample-answers.md
└── task-manager/
    ├── SKILL.md
    └── references/
        └── task-rules.md
```

প্রথমে শুধু `SKILL.md` দিয়ে শুরু করব।

## 2. SKILL.md-এর সাধারণ sections

| Section | উদ্দেশ্য |
|---|---|
| YAML frontmatter | machine-readable metadata |
| Role | Assistant-এর দায়িত্ব |
| When to Use | কখন Skill ব্যবহার হবে |
| Rules | কী করতে হবে/হবে না |
| Workflow | কাজের ধাপ |
| Examples | প্রত্যাশিত আচরণের নমুনা |
| Error Handling | তথ্য বা capability না থাকলে কী হবে |

সব Skill-এ সব section বাধ্যতামূলক নয়। প্রয়োজন অনুযায়ী রাখবে।

## 3. Practical — reference file তৈরি

```bash
cd ~/rahim_ai
mkdir -p skills/company-assistant/references
nano skills/company-assistant/references/company-policy.md
```

লিখো:

```markdown
# ABC Software — Company Policy

## Office
- Office hours: 9:00 AM to 6:00 PM
- Working days: Sunday to Thursday
- Weekly holidays: Friday and Saturday

## Attendance
- Employees should arrive on time.
- Attendance corrections must be reviewed by HR.

## Unknown Information
This document does not define salary, leave allowance, or disciplinary policy.
Do not guess these values.
```

এবার `SKILL.md`-এ এই অংশ যোগ করো:

```markdown
## Reference
Detailed policy may be available in `references/company-policy.md`.
If the application has not loaded that file into the model context, do not pretend you have read it.
```

**খুব গুরুত্বপূর্ণ:** Markdown-এ reference path লিখলেই LLM ফাইলটি পড়ে না। Python application-কে file load করে model context-এ দিতে হবে।

## 4. Skill design principles

1. **One Skill, one responsibility:** Company policy ও Task management আলাদা রাখো।
2. **Clear trigger:** Description-এ কখন Skill ব্যবহার হবে তা বলো।
3. **Testable rules:** “Be careful” না লিখে নির্দিষ্ট নিয়ম লেখো।
4. **Honest capability:** Tool না থাকলে “Task saved” বলা যাবে না।
5. **Small and focused:** অপ্রয়োজনীয় instruction যোগ করবে না।

## 5. Inspect the structure

```bash
find skills -maxdepth 4 -type f -print
cat skills/company-assistant/SKILL.md
```

## Homework

1. `employee-onboarding` Skill-এর folder design করো।
2. Role, When to Use, Rules ও Workflow লেখো।
3. Company Skill এবং Task Skill-এর দায়িত্ব যেন overlap না করে তা যাচাই করো।

## Completion checklist

- [ ] Folder-based structure বুঝেছি
- [ ] SKILL.md sections বুঝেছি
- [ ] Reference file-এর সীমাবদ্ধতা বুঝেছি
- [ ] Skill-এর দায়িত্ব আলাদা রাখতে পেরেছি
