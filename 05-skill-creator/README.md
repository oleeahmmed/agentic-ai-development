# 05 — Skill Creator

> অবস্থা: **অপেক্ষায় (Phase 7)।** ফেজ শুরু হলে এই ফাইলে Hermes সেটআপ, স্কিল ফরম্যাট ও দুই ট্র্যাকের গাইড যোগ হবে।

## লক্ষ্য

এমন এজেন্ট, যে পুনরাবৃত্ত কাজের অভিজ্ঞতা থেকে নতুন **skill** বানায়, টেস্ট করে, উন্নত করে।

## যা শিখবেন

- `SKILL.md` ফরম্যাট: YAML frontmatter + নির্দেশনা
- ভালো স্কিল লেখার নিয়ম: when-to-use, workflow, output, failure handling
- progressive disclosure — সব সময় পুরো স্কিল লোড নয়
- skill বনাম tool
- Hermes Agent: self-improving learning loop, `~/.hermes/skills/`, `hermes setup` / `hermes model`
- নিজের LangGraph-এ `skill_writer` গ্রাফ

## যা বানাবেন

- Track A: Hermes-এ একটি আসল পুনরাবৃত্ত কাজের স্কিল তৈরি, review, টেস্ট
- Track B: LangGraph-এ interview → draft → test → revise → **অনুমতির পরে** ফাইল লেখা
- `05-skill-creator/skills/`-এ তৈরি হওয়া স্কিল
- প্রতিটি স্কিলের টেস্ট কেস

## শেষ করার মানদণ্ড

- নতুন স্কিল ৩/৩ টেস্টে কাজ করে
- when-to-use ও failure handling আছে
- কোনো secret নেই
- ফাইল লেখার আগে মানুষের অনুমতি
- Hermes বনাম নিজের স্ট্যাক — কখন কোনটা, ব্যাখ্যা করতে পারেন

## শর্ত

Phase 0–6 সম্পন্ন (বিশেষত Phase 6 — Skills)।

## নিরাপত্তা

এজেন্টকে নিজের ইচ্ছায় ফাইল বদলাতে দেবেন না। স্কিল ফোল্ডার git-এ রাখুন, প্রতিটি পরিবর্তন review করুন।
