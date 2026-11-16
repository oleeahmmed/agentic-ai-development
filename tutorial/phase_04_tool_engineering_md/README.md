# Phase 04 — Tool Engineering & Native Tool Calling

এই Phase-এ AI Assistant-কে বাস্তব কাজ করানো শিখবে। LLM tool call প্রস্তাব করে; Python application arguments যাচাই করে function execute করে এবং ফলাফল model-কে ফেরত দেয়।

## Chapters
1. Tool Engineering Fundamentals
2. Python Tool Registry & Execution
3. Native Tool Calling — প্রথম Tool
4. Multiple Tools, Arguments & Validation
5. Tool Loop, Results & Error Handling
6. Build a Practical Tool-enabled Agent

## Setup

```bash
cd ~/rahim_ai
source venv/bin/activate
pip install --upgrade openai python-dotenv
```

`.env`:
```env
OPENAI_API_KEY=your_api_key_here
```

`.gitignore`:
```gitignore
.env
venv/
__pycache__/
```

## Project structure

```text
rahim_ai/
├── .env
├── config.py
├── main.py
└── tools/
    ├── __init__.py
    ├── calculator.py
    ├── notes.py
    └── registry.py
```

## Security rules
- API key source code-এ লিখবে না।
- Model-এর arguments untrusted input হিসেবে ধরবে।
- Allowlist ছাড়া arbitrary Python বা shell command execute করবে না।
- File path, database, টাকা-পয়সা ও destructive action-এ validation এবং permission রাখবে।
- Side-effect tool-এ user confirmation লাগতে পারে।
- Tool execution-এর সীমা, timeout ও logging রাখবে।
