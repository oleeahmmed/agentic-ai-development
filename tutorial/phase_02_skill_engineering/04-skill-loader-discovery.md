# Chapter 04 — Skill Loader & Discovery

**সময়:** ৪ ঘণ্টা | **লক্ষ্য:** Python দিয়ে Skill file খুঁজে বের করা, metadata parse করা এবং instruction load করা।

## 1. Discovery ও Loader

- **Discovery:** available Skill-গুলো খুঁজে বের করা।
- **Loader:** নির্দিষ্ট Skill-এর metadata ও instruction পড়া।

এই প্রথম version-এ discovery সব Skill-এর body-ও memory-তে load করবে। পরের উন্নতিতে metadata আগে scan করে নির্বাচিত Skill-এর body পরে load করব।

## 2. `skill_loader.py` তৈরি

```bash
cd ~/rahim_ai
nano skill_loader.py
```

সম্পূর্ণ code:

```python
from pathlib import Path
import yaml

SKILLS_DIR = Path(__file__).parent / "skills"


def parse_skill_file(skill_file: Path) -> dict:
    content = skill_file.read_text(encoding="utf-8")
    parts = content.split("---", 2)

    if len(parts) < 3 or parts[0].strip():
        raise ValueError(f"Invalid frontmatter: {skill_file}")

    metadata = yaml.safe_load(parts[1])
    instructions = parts[2].strip()

    if not isinstance(metadata, dict):
        raise ValueError(f"Metadata must be a mapping: {skill_file}")

    name = metadata.get("name")
    description = metadata.get("description")

    if not isinstance(name, str) or not name.strip():
        raise ValueError(f"Missing skill name: {skill_file}")

    if not isinstance(description, str) or not description.strip():
        raise ValueError(f"Missing skill description: {skill_file}")

    if not instructions:
        raise ValueError(f"Empty instructions: {skill_file}")

    return {
        "name": name.strip(),
        "description": description.strip(),
        "instructions": instructions,
        "path": str(skill_file),
    }


def discover_skills() -> list[dict]:
    if not SKILLS_DIR.exists():
        return []

    discovered = []
    seen_names = set()

    for skill_file in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        skill = parse_skill_file(skill_file)

        if skill["name"] in seen_names:
            raise ValueError(f"Duplicate skill name: {skill['name']}")

        seen_names.add(skill["name"])
        discovered.append(skill)

    return discovered


if __name__ == "__main__":
    skills = discover_skills()
    print(f"Discovered {len(skills)} skill(s)")

    for skill in skills:
        print(f"- {skill['name']}: {skill['description']}")
```

## 3. Run

```bash
python3 skill_loader.py
```

দুইটি Skill থাকলে output-এর ধরন:

```text
Discovered 2 skill(s)
- company-assistant: Answer questions about company information...
- task-manager: Help users organize tasks...
```

তোমার description অনুযায়ী output আলাদা হবে।

## 4. Code walkthrough

### Project-relative path

```python
SKILLS_DIR = Path(__file__).parent / "skills"
```

`__file__` বর্তমান Python file-এর path। `parent` তার containing folder। তাই terminal-এর current directory বদলালেও project-এর Skill directory খুঁজে পাওয়া যায়।

### File discovery

```python
SKILLS_DIR.glob("*/SKILL.md")
```

`skills` directory-এর এক স্তর নিচে প্রতিটি folder-এর `SKILL.md` খোঁজে।

### Duplicate detection

একই name একাধিকবার থাকলে router দ্বিধায় পড়তে পারে। তাই `seen_names` দিয়ে duplicate আটকানো হয়েছে।

## 5. Progressive loading

বড় system-এ সব Skill-এর full instruction সবসময় LLM-কে পাঠানো উচিত নয়।

```text
Startup -> Read Skill metadata
User request -> Select Skill
Selected Skill -> Load full SKILL.md
LLM -> Generate answer using selected instructions
```

## Homework

1. তৃতীয় Skill তৈরি করো।
2. Discovery-তে সেটি দেখা যাচ্ছে কি না পরীক্ষা করো।
3. Description মুছে validation error দেখো।
4. Duplicate name দিয়ে duplicate check পরীক্ষা করো।

## Completion checklist

- [ ] Discovery বুঝেছি
- [ ] Loader লিখেছি
- [ ] Duplicate validation পরীক্ষা করেছি
- [ ] Metadata ও instruction-এর পার্থক্য বুঝেছি
