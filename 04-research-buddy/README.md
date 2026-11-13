# 04 — Research Buddy

> অবস্থা: **অপেক্ষায় (Phase 5)।** ফেজ শুরু হলে এই ফাইলে গ্রাফ আঁকা, নোডের কোড ও ডিবাগ গাইড যোগ হবে।

## লক্ষ্য

LangGraph দিয়ে বহু-ধাপের গবেষণা এজেন্ট — প্রশ্ন ভাঙে, খোঁজে, সারাংশ করে, নিজের উত্তর সমালোচনা করে, দরকার হলে আবার খোঁজে, শেষে সোর্সসহ রিপোর্ট দেয়।

## যা শিখবেন

- কেন গ্রাফ (state, শাখা, লুপ, persistence, HITL)
- `StateGraph`, `TypedDict`, reducer (`add_messages`)
- node, edge, conditional edge, `START`/`END`
- checkpointer ও `thread_id` — থামিয়ে আবার চালানো
- `interrupt` দিয়ে মানুষের অনুমতি
- `recursion_limit`, streaming
- `create_agent` শর্টকাট বনাম নিজের গ্রাফ

## গ্রাফের আকার

```
START → plan → search → summarize → critique ─(যথেষ্ট?)→ write_report → END
                     ↑                    │
                     └────── revise ←──────┘
```

## যা বানাবেন

- `graph.py`, `nodes.py`, `tools.py`
- সার্চ: Tavily বা DuckDuckGo
- সোর্সসহ `.md` রিপোর্ট `reports/`-এ
- ১০টি টপিকে eval

## শেষ করার মানদণ্ড

- লুপ অনন্ত হয় না
- প্রতিটি দাবির পাশে আসল URL
- তথ্য না পেলে বানিয়ে বলে না
- interrupt-এর পরে resume হয়
- গ্রাফ কাগজে এঁকে ব্যাখ্যা করতে পারেন

## শর্ত

Phase 0–4 সম্পন্ন।
