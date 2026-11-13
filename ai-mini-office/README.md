# ai-mini-office — আগের প্রোটোটাইপ

> অবস্থা: **আগের পরীক্ষা।** এটি কোনো ফেজের গাইড নয় — ফেজের কোড এখানে নকল করবেন না।
> Phase 6-এ এই ধারণাগুলোই (skill + tool + agent) নতুন করে, বাংলা গাইডসহ বানানো হবে।
> সিলেবাস: [ai-agent-syllabus-bangla.md](../ai-agent-syllabus-bangla.md)

## এখানে কী আছে

| ফাইল | কাজ |
|---|---|
| `agent.py` | `create` / `list` / `exit` কমান্ডে চলে; নিয়মিত LLM কল করে না |
| `tools.py` | `create_task(task)`, `list_tasks()` — `tasks.txt`-এ সেভ ও পড়া |
| `skill_loader.py` | `skills/<name>/SKILL.md` পড়ে, YAML frontmatter বাদ দিয়ে নির্দেশনা ফেরত দেয় |
| `skills/task-manager/SKILL.md` | টাস্ক সহকারীর নিয়ম: কখন ব্যবহার, কীভাবে কাজ, কী বলবে না |
| `tasks.txt` | সেভ করা টাস্কের নমুনা (প্লেইন টেক্সট, প্রতি লাইনে একটি) |

## কী শেখা যায়

- **tool** = আসল কাজ করা Python function (`create_task`)
- **skill** = লেখা নির্দেশনা (`SKILL.md`) — কোড নয়
- `skill_loader.py` কীভাবে frontmatter আলাদা করে

## চালান

প্রথমে venv চালু করুন, তারপর এই ফোল্ডারে যান (ফাইলগুলো একে অপরকে পাশে খোঁজে):

```bash
source .venv/Scripts/activate
cd ai-mini-office
python skill_loader.py
python agent.py
```

> `agent.py` শুধু কমান্ড ধরে টুল ডাকে। এতে LLM নেই — তাই এটি "বুদ্ধিমান" নয়, শুধু কাঠামো দেখানোর নমুনা।

## ফেজের সাথে সম্পর্ক

| এখানে যা দেখেছেন | ফেজে কোথায় নতুন করে শিখবেন |
|---|---|
| `tools.py` + টুল ডাকা | Phase 3 — Weather Agent |
| স্মৃতি ফাইলে রাখা | Phase 4 — Memory Friend |
| `SKILL.md` পড়া | Phase 6 — Skills |
| LLM + skill + tool একসাথে | Phase 8 — Company Helper |

## পরের ধাপ

আসল গাইড শুরু করতে: [00-setup](../00-setup/README.md) → [python-basics](../python-basics/README.md) → [01-hello-agent](../01-hello-agent/README.md)।
