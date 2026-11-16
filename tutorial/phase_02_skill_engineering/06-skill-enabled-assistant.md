# Chapter 06 — Build a Skill-enabled AI Assistant

**সময়:** ৪–৬ ঘণ্টা | **লক্ষ্য:** Loader, Router ও LLM response একত্র করে Assistant তৈরি।

## 1. আমরা কী তৈরি করব?

1. Python available Skill discover করবে।
2. Router LLM উপযুক্ত Skill নির্বাচন করবে।
3. Python selected Skill খুঁজে বের করবে।
4. নির্বাচিত Skill-এর instruction final LLM call-এ পাঠানো হবে।
5. Assistant উত্তর দেবে।

এটি Skill-enabled Assistant; এখনো Tool-enabled Agent নয়। এখানে task save বা database update করার বাস্তব Tool নেই।

## 2. Project structure

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

## 3. `main.py`

```bash
nano main.py
```

সম্পূর্ণ code:

```python
import os

from dotenv import load_dotenv
from openai import OpenAI

from skill_loader import discover_skills
from router import select_skill

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is missing from .env")

client = OpenAI(api_key=api_key)


def find_skill(skills: list[dict], skill_name: str) -> dict | None:
    for skill in skills:
        if skill["name"] == skill_name:
            return skill
    return None


def generate_answer(user_request: str, skill: dict | None) -> str:
    if skill:
        instructions = skill["instructions"]
    else:
        instructions = (
            "You are a helpful general assistant. Reply in simple Bengali. "
            "Do not claim to perform actions unless a real tool confirms success."
        )

    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions=instructions,
        input=user_request,
    )
    return response.output_text


def main():
    print("Rahim AI — Skill-enabled Assistant")
    print("Type 'exit' to quit.\n")

    skills = discover_skills()

    while True:
        user_request = input("You: ").strip()

        if user_request.lower() in {"exit", "quit"}:
            print("Rahim AI: Goodbye!")
            break

        if not user_request:
            print("Rahim AI: Please enter a message.")
            continue

        try:
            selected_name = select_skill(user_request, skills)
            selected_skill = (
                find_skill(skills, selected_name)
                if selected_name else None
            )

            if selected_name and selected_skill is None:
                raise ValueError("Selected skill is not available.")

            answer = generate_answer(user_request, selected_skill)

            if selected_skill:
                print(f"\n[Skill: {selected_skill['name']}]")

            print(f"Rahim AI: {answer}\n")

        except Exception as error:
            print(f"Rahim AI: Something went wrong: {error}\n")


if __name__ == "__main__":
    main()
```

## 4. Run the Assistant

```bash
python3 main.py
```

Company test:

```text
You: আমাদের অফিস কয়টা থেকে কয়টা পর্যন্ত খোলা?
```

Assistant-এর উত্তর Skill-এ থাকা office hours-এর সঙ্গে মিলতে হবে।

Task test:

```text
You: আমার জন্য একটা task save করো।
```

Assistant-এর বলা উচিত যে এখনো বাস্তব Task Tool যুক্ত করা হয়নি। সে task-এর details সাজাতে পারে, কিন্তু save হয়েছে বলে দাবি করতে পারবে না।

## 5. Data flow

```text
main.py
  |
  +--> discover_skills()
  |       +--> skill_loader.py
  |               +--> SKILL.md files
  |
  +--> select_skill()
  |       +--> router.py
  |               +--> LLM selects skill name
  |
  +--> find_skill()
  |
  +--> generate_answer()
          +--> selected Skill instructions
          +--> LLM response
```

## 6. Engineering review

এটি learning project-এর প্রথম working architecture, production-ready Agent নয়।

পরবর্তী উন্নতিতে দরকার হবে:
- Router JSON schema validation
- API retry ও timeout
- Skill file size limit
- Prompt injection defense
- Metadata-only discovery ও on-demand loading
- Unit tests
- Conversation history
- Tool registry ও permission checks

Skill instruction application-এর security policy override করতে পারবে না।

## 7. Final homework

1. `hr-policy` নামে তৃতীয় Skill তৈরি করো।
2. Discovery-তে সেটি detect করো।
3. Router দিয়ে সেটি নির্বাচন পরীক্ষা করো।
4. Unknown request-এ general response পরীক্ষা করো।
5. Task save request-এ false success হচ্ছে কি না যাচাই করো।
6. পুরো data flow কাগজে এঁকে ব্যাখ্যা করো।

## 8. Phase 02 completion checklist

- [ ] Skill কী ও কেন লাগে ব্যাখ্যা করতে পারি
- [ ] Skill ও Tool-এর পার্থক্য বুঝি
- [ ] নিজে SKILL.md লিখেছি
- [ ] YAML metadata parse করেছি
- [ ] Python Skill Loader লিখেছি
- [ ] Skill Discovery লিখেছি
- [ ] LLM Skill Router লিখেছি
- [ ] Router output validate করেছি
- [ ] Skill-enabled Assistant চালিয়েছি
- [ ] Skill Tool execute করে না—এটি বুঝেছি

## এরপর কী?

পরবর্তী Phase: **Phase 03 — Memory Engineering**। সেখানে Short-term Memory, Long-term Memory, JSON/SQLite storage, Memory extraction, Embeddings, Vector Database ও RAG-এর ভিত্তি শিখব।
