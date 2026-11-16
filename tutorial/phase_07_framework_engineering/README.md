# Phase 07 — Framework Engineering

এই Phase-এ scratch থেকে তৈরি করা agent fundamentals-কে industry framework দিয়ে implement করা শিখবেন। Framework আপনার agent-এর logic-এর বিকল্প নয়; এগুলো orchestration, state, tool integration ও multi-step workflow manage করতে সাহায্য করে।

## Chapter list

1. **LangChain — Models, Prompts, Tools & Agents**
2. **LangGraph — Stateful Workflow, Nodes, Edges & Persistence**
3. **Multi-Agent Systems — Supervisor, Specialists & Coordination**

## Learning outcomes

এই Phase শেষে আপনি পারবেন:
- LangChain দিয়ে model, prompt, structured output এবং tool integration করতে;
- LangGraph দিয়ে stateful graph-based agent workflow তৈরি করতে;
- conditional edge, checkpoint, interrupt/approval ও human-in-the-loop বুঝতে;
- specialist agent এবং supervisor pattern design করতে;
- কখন framework ব্যবহার করবেন আর কখন plain Python যথেষ্ট—সিদ্ধান্ত নিতে;
- Phase 08-এর AI Software Development Company capstone-এর architecture প্রস্তুত করতে।

## Ubuntu setup

```bash
mkdir phase07_frameworks
cd phase07_frameworks
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

প্রতিটি chapter-এর package আলাদা করে install করুন। LangChain ecosystem দ্রুত evolve করে, তাই compatible package versions একসঙ্গে pin করুন এবং official documentation-এর current quickstart অনুসরণ করুন।

Suggested initial packages:

```bash
pip install langchain langchain-openai python-dotenv pydantic
pip install langgraph
```

`.env`:

```env
OPENAI_API_KEY=your_api_key_here
```

`.gitignore`:

```gitignore
.venv/
.env
__pycache__/
.pytest_cache/
*.db
```

**Version note:** LangChain/LangGraph-এর API ও package organization release অনুযায়ী পরিবর্তিত হতে পারে। এই tutorial-এ বর্তমান বহুল ব্যবহৃত `ChatOpenAI`, `@tool`, `StateGraph`, `START`, `END`, `ToolNode` pattern শেখানো হয়েছে। আপনার installed version-এ কোনো import বদলে গেলে official docs-এর matching version দেখুন এবং tested dependency version pin করুন।

**গুরুত্বপূর্ণ:** Framework ব্যবহার করলেও Phase 06-এর security, permission, validation, approval, retry, observability ও evaluation principles অপরিহার্য।
