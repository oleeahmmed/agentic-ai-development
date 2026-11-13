# 03 — Memory Friend

> অবস্থা: **অপেক্ষায় (Phase 4)।** ফেজ শুরু হলে এই ফাইলে পদে পদে গাইড, ডেটা মডেল ও পরীক্ষা যোগ হবে।

## লক্ষ্য

এমন এজেন্ট, যে আপনার পছন্দ ও প্রসঙ্গ মনে রাখে — প্রোগ্রাম বন্ধ করলেও ভোলে না।

## যা শিখবেন

- short-term বনাম long-term memory
- প্রোফাইল / episodic / semantic memory
- JSON → SQLite → vector store — ধাপে ধাপে
- embedding, cosine similarity, chunking
- RAG: retrieve → prompt → উত্তর + উৎস
- কী সেভ করবেন, কী করবেন না (memory policy)
- দ্বন্দ্ব সমাধান (পুরনো পছন্দ বনাম নতুন) ও `/forget`

## যা বানাবেন

- `agent.py` — চ্যাট + memory-aware উত্তর
- `memory.py` — সেভ/খোঁজা/মুছা
- প্রোফাইল: নাম, শহর, প্রিয় খাবার, লক্ষ্য, তারিখ
- কমান্ড: `/memory` (কী মনে আছে), `/forget`
- `user_id` দিয়ে আলাদা মানুষ আলাদা memory

## শেষ করার মানদণ্ড

- restart-এর পরেও পছন্দ মনে আছে
- দুই ইউজারের memory মেশে না
- "আমি কী কী বলেছিলাম?" → memory থেকে উত্তর
- অপ্রাসঙ্গিক memory প্রম্পটে ঢোকে না
- `/forget` কাজ করে

## শর্ত

Phase 0–3 সম্পন্ন। Stretch: পুরনো কথোপকথনে vector search।
