# Phase 02 — Skill Engineering

এই Phase-এ আমরা Scratch থেকে Skill System তৈরি করব। প্রতিদিন প্রায় ৪ ঘণ্টা ধরে একটি করে Chapter পড়বে।

## Chapters
1. `01-skill-fundamentals.md` — Skill কী, কেন লাগে, Skill বনাম Tool
2. `02-skill-file-architecture.md` — Skill folder ও SKILL.md design
3. `03-skill-metadata-yaml.md` — YAML frontmatter, name ও description
4. `04-skill-loader-discovery.md` — Python দিয়ে Skill load ও discover
5. `05-skill-selection-router.md` — LLM দিয়ে Skill নির্বাচন
6. `06-skill-enabled-assistant.md` — সবকিছু একত্র করে Assistant তৈরি

## Setup

```bash
cd ~/rahim_ai
source venv/bin/activate
pip install openai python-dotenv pyyaml
mkdir -p skills/company-assistant skills/task-manager
```

## Final project structure

```text
rahim_ai/
├── main.py
├── skill_loader.py
├── router.py
├── .env
├── requirements.txt
└── skills/
    ├── company-assistant/SKILL.md
    └── task-manager/SKILL.md
```

## গুরুত্বপূর্ণ নিয়ম

- Skill হলো instruction package; executable Python function নয়।
- Tool বাস্তবে কাজ করে; Skill বলে দেয় কীভাবে কাজ করতে হবে।
- LLM Skill নির্বাচন করতে পারে, কিন্তু Python application selection validate করবে।
- Tool না থাকলে কোনো action সম্পন্ন হয়েছে বলে দাবি করা যাবে না।
- `.env` এবং API key কখনো Git-এ commit করবে না।

প্রতিটি Chapter-এর Practical নিজে চালিয়ে তারপর পরেরটিতে যাবে।
