# AI Agent ল্যাব

শূন্য থেকে AI Agent বানানো শেখার ব্যবহারিক রিপো।
সিলেবাস: [ai-agent-syllabus-bangla.md](ai-agent-syllabus-bangla.md)

---

## নিয়ম

- প্রতিটি প্রজেক্টের নিজের ফোল্ডার, নিজের কোড, নিজের ডেটা।
- **প্রতিটি ফোল্ডারের `README.md` = সেই ফেজের হাতে-কলমে গাইড।** ফেজ শেষ হলে গাইডটি সম্পূর্ণ হয়, যাতে দেখে দেখে আবার বানানো যায়।
- প্রতিটি ফেজ শেষে git commit। `.env` কখনো commit নয়।

---

## ফোল্ডার ম্যাপ

| ফোল্ডার | প্রজেক্ট | ফেজ | অবস্থা |
|---|---|---|---|
| [00-setup](00-setup/README.md) | পরিবেশ, প্রথম LLM কল | Phase 0 | সম্পন্ন — লাইভ কল সফল |
| [python-basics](python-basics/README.md) | Python বেসিক | Phase 1 | সম্পন্ন — গাইড ও ৮টি পাঠ |
| [01-hello-agent](01-hello-agent/README.md) | Hello Agent | Phase 2 | সম্পন্ন — পার্সোনা, মেমোরি, `/reset` টেস্টেড |
| [02-weather-agent](02-weather-agent/README.md) | Weather Agent | Phase 3 | সম্পন্ন — ৩টি টুল, নিজের লেখা লুপ টেস্টেড |
| [03-memory-friend](03-memory-friend/README.md) | Memory Friend | Phase 4 | সম্পন্ন — স্মৃতি, `/memory`, `/forget` টেস্টেড |
| [04-research-buddy](04-research-buddy/README.md) | Research Buddy | Phase 5 | অপেক্ষায় |
| [05-skill-creator](05-skill-creator/README.md) | Skill Creator | Phase 7 | অপেক্ষায় |
| [06-company-helper](06-company-helper/README.md) | Company Helper | Phase 8 | অপেক্ষায় |
| [shared](shared/README.md) | কমন কোড (LLM client, skill loader) | সব ফেজ | অপেক্ষায় |
| [notes](notes/README.md) | দৈনিক শেখা ও ভুলের নোট | সব ফেজ | চলছে |
| [ai-mini-office](ai-mini-office/README.md) | আগের প্রোটোটাইপ (Phase 6-এ নতুন করে বানানো হবে) | ফেজের আগে | রাখা হয়েছে |

---

## দ্রুত শুরু

```bash
source .venv/Scripts/activate
python 00-setup/check_env.py
python 00-setup/hello_llm.py
```

প্রথমবার হলে [00-setup/README.md](00-setup/README.md) ধাপে ধাপে অনুসরণ করুন।

---

## অগ্রগতি

- [x] Phase 0 — পরিবেশ ও প্রথম LLM কল (লাইভ কল সফল)
- [x] Phase 1 — Python বেসিক (গাইড ও ৮টি পাঠ)
- [x] Phase 2 — Hello Agent (লাইভ টেস্ট সফল)
- [x] Phase 3 — Weather Agent (লাইভ টেস্ট সফল)
- [x] Phase 4 — Memory Friend (লাইভ টেস্ট সফল)
- [ ] Phase 5 — Research Buddy
- [ ] Phase 6 — Skills
- [ ] Phase 7 — Skill Creator (Hermes)
- [ ] Phase 8 — Company Helper
- [ ] Phase 9 — Production ও Capstone
