# Phase 03 — Memory Engineering

**কোর্স:** Scratch থেকে Python AI Agent Engineering  
**ভাষা:** বাংলা ব্যাখ্যা + English technical terms  
**পরিবেশ:** Ubuntu, Python 3, OpenAI API  
**সময়:** প্রতিদিন প্রায় ৪ ঘণ্টা  
**Project:** `rahim_ai`

## Phase-এর লক্ষ্য

এই Phase শেষে তুমি বুঝবে AI Agent কীভাবে আগের কথোপকথন মনে রাখে, কোন তথ্য অস্থায়ীভাবে রাখে, কোন তথ্য দীর্ঘমেয়াদে সংরক্ষণ করে, কীভাবে প্রাসঙ্গিক তথ্য retrieve করে এবং বড় knowledge collection থেকে relevant তথ্য বের করে।

## Chapters

1. `01-memory-fundamentals.md` — Memory কী, কেন দরকার, Context বনাম Memory
2. `02-short-term-memory.md` — Conversation history ও short-term memory
3. `03-long-term-memory-json-sqlite.md` — JSON ও SQLite দিয়ে persistent memory
4. `04-memory-extraction-update.md` — কথোপকথন থেকে memory extract, validate, update ও forget
5. `05-embeddings-semantic-search.md` — Embeddings ও semantic similarity
6. `06-vector-database-rag.md` — Vector store, retrieval এবং RAG-এর প্রথম বাস্তব implementation

## Setup

আগের Phase-এর `rahim_ai` project-ই ব্যবহার করবে:

```bash
cd ~/rahim_ai
source venv/bin/activate
pip install openai python-dotenv pyyaml
```

`requirements.txt`:

```text
openai
python-dotenv
pyyaml
```

`.env`-এ API key থাকবে:

```env
OPENAI_API_KEY=your_api_key_here
```

API key কখনো code, screenshot, public repository বা shared file-এ দেবে না।

## Phase-এর Architecture

```text
User message
    |
    v
Memory Manager
    |
    +--> Short-term conversation history
    |
    +--> Long-term user facts (JSON / SQLite)
    |
    +--> Semantic retrieval (embeddings / vector store)
    |
    v
Relevant context builder
    |
    v
LLM
    |
    v
Assistant response
```

## শেখার গুরুত্বপূর্ণ নিয়ম

- Conversation history আর long-term memory এক জিনিস নয়।
- সব user message চিরদিন সংরক্ষণ করা উচিত নয়।
- Memory-তে sensitive তথ্য অকারণে রাখা যাবে না।
- User-এর অনুরোধ অনুযায়ী তথ্য সংশোধন বা ভুলে যাওয়ার ব্যবস্থা থাকতে হবে।
- Retrieved memory-কে trusted instruction হিসেবে বিবেচনা করবে না।
- LLM memory প্রস্তাব করতে পারে; Python application validate করে store করবে।
- Embedding হলো text-এর numerical representation; এটি নিজে database নয়।
- RAG হলো retrieval করে relevant content model context-এ দেওয়ার pattern।

## Completion checklist

- [ ] Memory ও context-এর পার্থক্য বুঝি
- [ ] Short-term conversation history তৈরি করেছি
- [ ] JSON-এ memory persist করেছি
- [ ] SQLite-এ memory persist করেছি
- [ ] Memory extraction ও validation করেছি
- [ ] Memory update ও delete করেছি
- [ ] Embedding তৈরি করেছি
- [ ] Semantic search বুঝেছি
- [ ] Vector retrieval ও RAG pipeline তৈরি করেছি
