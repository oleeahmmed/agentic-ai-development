# Chapter 03 — Multi-Agent Systems: Supervisor, Specialists & Coordination

## 1. Multi-Agent system কী?

একটি agent-এর মধ্যে সব দায়িত্ব না দিয়ে কয়েকটি specialist agent-এ কাজ ভাগ করলে সেটি multi-agent architecture হতে পারে।

উদাহরণ: AI Software Development Company

```text
User
 |
Supervisor / Project Manager Agent
 |--------- Requirements Analyst
 |--------- Architect Agent
 |--------- Developer Agent
 |--------- Tester Agent
 |--------- Reviewer Agent
 |
Final response / deliverables
```

কিন্তু বেশি agent মানেই ভালো ফল নয়। প্রতিটি agent-এর LLM call, latency, token cost, failure ও coordination complexity বাড়ে।

## 2. কখন multi-agent ব্যবহার করবেন?

ব্যবহার করতে পারেন যখন:
- task-এর আলাদা specialist capability দরকার;
- subtask-গুলো স্পষ্টভাবে ভাগ করা যায়;
- independent research parallel করা যায়;
- একটি agent-এর context খুব বড় হয়ে যাচ্ছে;
- আলাদা permission boundary দরকার।

ব্যবহার করবেন না যখন:
- কাজটি এক tool call-এ হয়;
- task ছোট ও deterministic;
- agents-এর মধ্যে dependency অস্পষ্ট;
- extra LLM call-এর benefit নেই।

## 3. Common patterns

### A. Supervisor pattern

একটি supervisor task ভেঙে specialist-দের delegate করে এবং ফলাফল একত্র করে।

```text
             Supervisor
             /   |    \
        Analyst Architect Tester
             \   |    /
              Results
                 |
              Supervisor
```

### B. Sequential pipeline

```text
Requirements -> Architecture -> Code -> Test -> Review
```

### C. Parallel specialists

```text
                 -> Security review -
User -> Supervisor -> Performance review -> Combine
                 -> Code review ------
```

### D. Handoff

এক agent নির্দিষ্ট condition-এ control অন্য agent-কে দেয়। Handoff-এর সঙ্গে context, task scope ও permission পাঠাতে হবে।

## 4. Agent contract design

প্রতিটি specialist-এর দায়িত্ব ও output schema স্পষ্ট রাখুন।

`contracts.py`:

```python
from pydantic import BaseModel, Field


class SpecialistResult(BaseModel):
    specialist: str
    summary: str
    findings: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)
    status: str = Field(pattern="^(complete|blocked|needs_input)$")
```

এতে supervisor সব specialist-এর output একই format-এ পাবে।

## 5. Simple multi-agent simulation (without LLM)

প্রথমে LLM ছাড়াই orchestration বুঝি।

`01_multi_agent_demo.py`:

```python
from dataclasses import dataclass


@dataclass
class Task:
    title: str
    description: str


def analyst_agent(task: Task) -> dict:
    return {
        "specialist": "analyst",
        "summary": f"Requirements analyzed for: {task.title}",
        "findings": ["User login", "Role-based access", "Audit trail"],
        "risks": ["Requirements may be incomplete"],
    }


def architect_agent(task: Task, analysis: dict) -> dict:
    return {
        "specialist": "architect",
        "summary": "Architecture proposal created",
        "findings": [
            "Django REST API",
            "PostgreSQL database",
            "Service layer",
        ],
        "risks": ["Deployment architecture needs confirmation"],
    }


def tester_agent(task: Task, architecture: dict) -> dict:
    return {
        "specialist": "tester",
        "summary": "Test plan created",
        "findings": [
            "Authentication tests",
            "Permission tests",
            "Tenant isolation tests",
        ],
        "risks": [],
    }


def supervisor(task: Task) -> dict:
    analysis = analyst_agent(task)
    architecture = architect_agent(task, analysis)
    testing = tester_agent(task, architecture)

    return {
        "task": task.title,
        "analysis": analysis,
        "architecture": architecture,
        "testing": testing,
        "status": "completed",
    }


if __name__ == "__main__":
    task = Task(
        title="Build HRM login module",
        description="Create secure multi-tenant login API",
    )
    print(supervisor(task))
```

এখানে specialist-গুলো Python function, LLM agent নয়। আগে orchestration বুঝে তারপর LLM যুক্ত করা সহজ।

## 6. LLM specialist pattern with LangChain

নিচের উদাহরণে একই model ব্যবহার করে আলাদা role prompt দেওয়া হয়েছে। এটি specialist role simulation; আলাদা model বা autonomous agent বাধ্যতামূলক নয়।

`02_specialists.py`:

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

model = ChatOpenAI(model="gpt-4.1-mini", temperature=0)


def make_specialist(system_prompt: str):
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "Project request:\n{request}"),
    ])
    return prompt | model


analyst = make_specialist(
    "তুমি requirements analyst. Functional ও non-functional requirements বের করো।"
)

architect = make_specialist(
    "তুমি software architect. Component, data flow ও technology design করো।"
)

tester = make_specialist(
    "তুমি QA engineer. Test scenario, edge case ও acceptance criteria লেখো।"
)


def main():
    request = "একটি multi-tenant HRM SaaS-এর employee login module তৈরি করতে হবে।"

    analysis = analyst.invoke({"request": request})
    architecture = architect.invoke({
        "request": request + "\n\nAnalyst findings:\n" + analysis.content
    })
    testing = tester.invoke({
        "request": request + "\n\nArchitecture:\n" + architecture.content
    })

    print("\n=== ANALYSIS ===\n", analysis.content)
    print("\n=== ARCHITECTURE ===\n", architecture.content)
    print("\n=== TEST PLAN ===\n", testing.content)


if __name__ == "__main__":
    main()
```

এটি sequential pipeline। প্রতিটি specialist-এর output যাচাই করুন; পরের agent-এ raw untrusted text পাঠানোর সময় instruction injection-এর ঝুঁকি বিবেচনা করুন।

## 7. Supervisor routing design

Supervisor-এর কাজ:
1. user goal বুঝবে;
2. task decomposition করবে;
3. specialist বেছে নেবে;
4. specialist-এর output schema validate করবে;
5. missing information বা conflict শনাক্ত করবে;
6. দরকার হলে specialist-কে revise করতে বলবে;
7. final result assemble করবে।

Supervisor-কে সব tools ও সব data access দেবেন না। Least privilege অনুসরণ করুন।

## 8. Parallel specialist execution

Independent review parallel করা যায়। নিচে asyncio দিয়ে specialist function-গুলোর concurrent orchestration দেখানো হয়েছে। LangChain Runnable হলে async invoke support অনুযায়ী `ainvoke()` ব্যবহার করুন।

```python
import asyncio


async def security_review(request: str):
    await asyncio.sleep(1)
    return {"type": "security", "findings": ["Check authorization", "Audit writes"]}


async def performance_review(request: str):
    await asyncio.sleep(1)
    return {"type": "performance", "findings": ["Add database indexes"]}


async def code_review(request: str):
    await asyncio.sleep(1)
    return {"type": "code", "findings": ["Add input validation"]}


async def main():
    request = "Review the proposed HRM login module"
    results = await asyncio.gather(
        security_review(request),
        performance_review(request),
        code_review(request),
        return_exceptions=True,
    )
    for result in results:
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
```

Parallel কেবল independent subtask-এর জন্য। Database write বা dependent workflow blindly parallel করবেন না।

## 9. Failure, disagreement ও quality control

Multi-agent system-এ সমস্যা হতে পারে:
- Specialist ভুল বা fabricated finding দেয়।
- দুই specialist পরস্পরবিরোধী recommendation দেয়।
- Supervisor ভুলভাবে result summarize করে।
- Agent cycle বা repeated delegation তৈরি হয়।
- Token/cost budget শেষ হয়ে যায়।

সমাধান:
- প্রতিটি agent-এর max turns;
- global deadline ও token/cost budget;
- typed output schema;
- evidence/reference field;
- independent validator/test;
- escalation to human;
- conflict explicitly report;
- tool permission per specialist;
- trace ID ও per-agent metrics।

এক specialist-এর output-কে verified fact হিসেবে ধরবেন না। Code execution/test result বা trusted source দিয়ে verify করুন।

## 10. Multi-agent permission matrix

| Agent | Read project | Create task | Delete project | Deploy |
|---|---:|---:|---:|---:|
| Supervisor | Yes | Request only | No | No |
| Analyst | Yes | No | No | No |
| Architect | Yes | No | No | No |
| Developer | Scoped | Approval | No | No |
| Tester | Scoped | No | No | No |
| Release manager | Scoped | No | No | Approval |

“Request only” মানে supervisor action propose করতে পারে; execution policy gate-এ হবে।

## 11. Phase 08-এর জন্য target architecture

AI Software Development Company project-এ সম্ভাব্য team:

```text
Client / User
     |
Project Manager / Supervisor
     |
     +-- Business Analyst Agent
     +-- Product Manager Agent
     +-- Software Architect Agent
     +-- Backend Developer Agent
     +-- Frontend Developer Agent
     +-- Database Engineer Agent
     +-- QA / Test Engineer Agent
     +-- Security Reviewer Agent
     +-- DevOps Agent
     |
Shared project state + task board + artifact store
     |
Human approval gates
     |
Deliverables: requirements, design, code, tests, deployment plan
```

প্রথম সংস্করণে সব agent autonomous করবেন না। একটি supervisor, ২–৩টি specialist, সীমিত tools এবং human approval দিয়ে শুরু করুন।

## 12. Homework

1. Analyst, Architect, Tester—এই ৩টি specialist তৈরি করুন।
2. প্রতিটি output `SpecialistResult` schema-তে validate করুন।
3. Supervisor-কে final summary তৈরি করতে দিন।
4. Security ও performance review parallel চালান।
5. একটি specialist fail করলে graceful fallback দিন।
6. প্রতিটি agent-এর tool permission matrix লিখুন।
7. ১০টি test request দিয়ে task routing ও output quality evaluate করুন।

**Chapter takeaway:** Multi-agent মানে অনেক chatbot নয়; এটি role, state, delegation, permission, budget এবং verification-সহ coordinated workflow।
