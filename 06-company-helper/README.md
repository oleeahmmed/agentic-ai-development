# 06 — Company Helper

> অবস্থা: **অপেক্ষায় (Phase 8)।** ফেজ শুরু হলে এই ফাইলে ডেটাবেস, টুল, গ্রাফ, পলিসি ও eval-এর সম্পূর্ণ গাইড যোগ হবে।

## লক্ষ্য

সবকিছু একসাথে — LangGraph + skills + tools + memory + approval + eval + deploy। কাল্পনিক কোম্পানি **Little Office Ltd.**-এর কাস্টমার সাপোর্ট।

## যা শিখবেন

- আসল ডেটার সাথে এজেন্ট (SQLite)
- read-only টুল থেকে write টুলে ধাপে ধাপে যাওয়া
- পলিসি RAG ও টোন স্কিল
- মানুষের অনুমতি (approval) — ইমেইল/রিফান্ডের আগে
- guardrail: রিফান্ড সীমা, ইমেইল whitelist, অন্য কাস্টমারের তথ্য নয়, prompt injection ব্লক
- structured log, trace, cost
- ২৫টি কেসের eval
- FastAPI + Streamlit + cron

## যা বানাবেন

- `db/seed.py` — customers, orders, order_items, tickets (২০টি ভুয়া অর্ডার)
- `tools/` — find_customer, get_order, search_products, check_refund_eligibility, create_ticket, send_email (টেস্ট SMTP), escalate_to_human
- `graph.py` — intake/guard → classify → skill → tool loop → policy_check → approval → respond → log
- `skills/` — support-tone, refund-policy, escalation-rules, email-template
- `evals/cases.json` — ২০টি সাধারণ + ৫টি প্রতারক কেস
- `app.py` — Streamlit/FastAPI

## শেষ করার মানদণ্ড

- ১০টি লিখিত সিনারিও সফল
- ভুল অর্ডার নাম্বারে ভদ্র ব্যর্থতা
- অনুমতি ছাড়া রিফান্ড/ইমেইল নয়
- "ignore your rules" ব্লক ও লগ
- অন্য কাস্টমারের তথ্য ফাঁস নয়
- প্রতি উত্তরে টুল প্রমাণ
- ২৫টি eval-এ ৯০%+ pass

## শর্ত

Phase 0–7 সম্পন্ন।
