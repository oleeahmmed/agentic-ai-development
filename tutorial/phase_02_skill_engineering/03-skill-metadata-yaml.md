# Chapter 03 — Skill Metadata & YAML

**সময়:** ৪ ঘণ্টা | **লক্ষ্য:** YAML frontmatter parse ও validate করা।

## 1. Metadata কী?

Metadata হলো content সম্পর্কে machine-readable তথ্য। আমাদের Skill-এর metadata-তে থাকবে:
- `name`: unique Skill identifier
- `description`: Skill কী করে এবং কখন ব্যবহার করতে হবে

`SKILL.md`-এর শুরুতে YAML frontmatter রাখব:

```yaml
---
name: company-assistant
description: Answer company-related questions. Use for office hours and company policies.
---
```

দুই পাশে `---` delimiter; মাঝখানে YAML, এরপর Markdown instructions।

## 2. YAML কী?

YAML configuration data লেখার human-readable format।

```yaml
name: task-manager
enabled: true
priority: 10
tags:
  - tasks
  - productivity
```

Indentation গুরুত্বপূর্ণ। Space ব্যবহার করবে, tab নয়।

## 3. Dependency install

```bash
cd ~/rahim_ai
source venv/bin/activate
pip install pyyaml
```

`requirements.txt`:

```text
openai
python-dotenv
pyyaml
```

## 4. Practical — metadata parser

```bash
nano inspect_skill.py
```

Code:

```python
from pathlib import Path
import yaml

skill_path = Path("skills/company-assistant/SKILL.md")
content = skill_path.read_text(encoding="utf-8")

parts = content.split("---", 2)

if len(parts) < 3 or parts[0].strip():
    raise ValueError("Invalid SKILL.md frontmatter")

metadata = yaml.safe_load(parts[1])
instructions = parts[2].strip()

if not isinstance(metadata, dict):
    raise ValueError("Metadata must be a YAML mapping")

name = metadata.get("name")
description = metadata.get("description")

if not isinstance(name, str) or not name.strip():
    raise ValueError("Skill name is required")

if not isinstance(description, str) or not description.strip():
    raise ValueError("Skill description is required")

print("Name:", name)
print("Description:", description)
print("Instruction characters:", len(instructions))
```

চালাও:

```bash
python3 inspect_skill.py
```

## 5. Error experiment

`SKILL.md`-এ সাময়িকভাবে `name` মুছে script চালাও। Validation error হবে। তারপর name ফিরিয়ে দাও।

এতে বোঝা যাবে metadata শুধু parse করলেই হবে না, required field validate-ও করতে হবে।

## 6. Reliability ও security

- Untrusted YAML-এর জন্য `yaml.safe_load()` ব্যবহার করো।
- Duplicate Skill name discovery পর্যায়ে আটকাও।
- Metadata-কে executable code মনে করো না।
- Skill instruction application-এর security policy override করতে পারবে না।

## Homework

1. `task-manager` metadata parse করো।
2. Missing description হলে error দেখাও।
3. Duplicate name হলে কী সমস্যা হবে ব্যাখ্যা করো।

## Completion checklist

- [ ] YAML frontmatter বুঝেছি
- [ ] safe_load ব্যবহার করেছি
- [ ] name ও description validate করেছি
- [ ] malformed metadata পরীক্ষা করেছি
