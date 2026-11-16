# Chapter 06 — MCP + Production Agent Capstone

## 1. MCP কী?

Model Context Protocol (MCP) AI application-কে external tools ও context source-এর সঙ্গে standard protocol-এ connect করার পদ্ধতি।

Native function calling-এ application model-কে tool schema দেয়; model call প্রস্তাব করলে application code execute করে। MCP-তে MCP server tools/resources/prompts expose করে এবং MCP client সেগুলো discover ও invoke করে।

```text
Agent Host
   |
MCP Client
   |  protocol
MCP Server
   |-- Tools
   |-- Resources
   |-- Prompts
   |
Database / Files / External APIs
```

## 2. Key concepts

- Host: AI application।
- Client: host-এর MCP connection handler।
- Server: capabilities expose করে।
- Tools: action/function।
- Resources: পড়ার context/data।
- Prompts: reusable prompt template।
- Transport: stdio বা supported HTTP transport-এর মতো যোগাযোগ পদ্ধতি।

MCP নিজে tool-কে নিরাপদ করে না। Authentication, authorization, validation, rate limit ও audit আপনার system-এ enforce করতে হবে।

## 3. Native function calling বনাম MCP

| বিষয় | Native tool calling | MCP |
|---|---|---|
| Schema | app model request-এ দেয় | server থেকে discover |
| Execution | app code | MCP client/server request |
| Reuse | integration-specific | compatible clients/servers-এ reusable |
| Security | app enforce করে | host ও server layer-এ enforce |

MCP মানেই model সরাসরি database access পায় না।

## 4. MCP SDK setup

MCP Python SDK দ্রুত evolve করে। Official Python SDK documentation দেখে Python-compatible version নির্বাচন ও pin করুন। সাধারণ installation:

```bash
pip install mcp
```

`requirements.txt`-এ আপনার পরীক্ষিত exact version লিখবেন।

## 5. Minimal MCP server pattern

নিচের decorator-based FastMCP pattern SDK release অনুযায়ী সামান্য বদলাতে পারে। Import/runner API ভিন্ন হলে official quickstart অনুসরণ করুন।

`mcp_server.py`:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("project-task-server")

@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """দুটি integer যোগ করে।"""
    return a + b

@mcp.tool()
def make_task_title(title: str) -> str:
    """Task title normalize ও validate করে।"""
    cleaned = " ".join(title.split())
    if len(cleaned) < 3:
        raise ValueError("Title must contain at least 3 characters")
    if len(cleaned) > 120:
        raise ValueError("Title is too long")
    return cleaned

if __name__ == "__main__":
    mcp.run()
```

stdio transport-এ stdout-এ debug print করবেন না; protocol stream নষ্ট হতে পারে। stderr বা proper logging ব্যবহার করুন।

## 6. MCP server test

Compatible MCP inspector/client দিয়ে:
1. Server connect করুন।
2. Tools list করুন।
3. `add_numbers` valid input দিয়ে call করুন।
4. Invalid input পাঠান।
5. Error response ও disconnect behavior দেখুন।

Production-এ authenticated identity, tool authorization, schema validation, rate limit, audit logging, transport security, timeout ও output filtering লাগবে।

## 7. Capstone — Project Assistant

Features:
1. User goal গ্রহণ।
2. LLM structured action proposal।
3. Tool allowlist ও argument validation।
4. Authenticated user context দিয়ে permission।
5. Read-only tool execution।
6. Sensitive write-এ approval।
7. Step limit ও timeout।
8. Structured logging।
9. Unit/evaluation tests।
10. MCP tools integration।

Suggested structure:

```text
production_project_agent/
├── app/
│   ├── main.py
│   ├── agent.py
│   ├── state.py
│   ├── llm_client.py
│   ├── tool_registry.py
│   ├── policies.py
│   ├── approvals.py
│   ├── schemas.py
│   ├── storage.py
│   └── observability.py
├── tests/
├── mcp_server.py
├── .env
├── .gitignore
└── requirements.txt
```

## 8. Integrated controller skeleton

এটি model-independent controller। `decide()` পরে OpenAI Responses API বা অন্য LLM adapter দিয়ে implement করবেন।

`agent.py`:

```python
from dataclasses import dataclass, field
from typing import Any, Callable
import logging
import time

logger = logging.getLogger("project_agent")

class AgentLimitError(Exception):
    pass

class ToolPermissionError(Exception):
    pass

@dataclass
class UserContext:
    user_id: str
    tenant_id: int
    role: str
    approved_actions: set[str] = field(default_factory=set)

@dataclass
class AgentState:
    run_id: str
    goal: str
    max_steps: int = 8
    step_count: int = 0
    observations: list[dict[str, Any]] = field(default_factory=list)
    status: str = "running"

TOOLS: dict[str, Callable[..., Any]] = {}

def register_tool(name: str):
    def decorator(func):
        TOOLS[name] = func
        return func
    return decorator

@register_tool("list_projects")
def list_projects(tenant_id: int) -> list[dict]:
    demo = [
        {"id": 1, "tenant_id": 10, "name": "HRM Platform"},
        {"id": 2, "tenant_id": 20, "name": "Other Tenant Project"},
    ]
    return [
        {"id": p["id"], "name": p["name"]}
        for p in demo if p["tenant_id"] == tenant_id
    ]

@register_tool("create_task")
def create_task(tenant_id: int, project_id: int, title: str) -> dict:
    if len(title.strip()) < 3:
        raise ValueError("Task title is too short")
    # Demo only: real DB transaction + idempotency প্রয়োজন।
    return {
        "task_id": 101, "tenant_id": tenant_id,
        "project_id": project_id, "title": title.strip(),
        "status": "created",
    }

READ_TOOLS = {"list_projects"}
WRITE_TOOLS = {"create_task"}

def authorize(name: str, context: UserContext, action_id: str | None = None):
    if name not in TOOLS:
        raise ToolPermissionError("Tool is not allowlisted")
    if context.role not in {"member", "admin"}:
        raise ToolPermissionError("Insufficient role")
    if name in WRITE_TOOLS:
        if context.role != "admin":
            raise ToolPermissionError("Admin role required")
        if not action_id or action_id not in context.approved_actions:
            raise ToolPermissionError("Approval required")

def execute_tool(name: str, arguments: dict, context: UserContext,
                 action_id: str | None = None):
    authorize(name, context, action_id)
    if not isinstance(arguments, dict):
        raise ValueError("Arguments must be a dictionary")
    safe_args = dict(arguments)
    # Tenant ID model arguments থেকে নেওয়া হচ্ছে না।
    safe_args["tenant_id"] = context.tenant_id
    return TOOLS[name](**safe_args)

def run_agent(state: AgentState, context: UserContext, decide: Callable):
    while state.status == "running":
        if state.step_count >= state.max_steps:
            state.status = "limit_reached"
            raise AgentLimitError("Maximum agent steps reached")

        state.step_count += 1
        decision = decide(state)

        if decision.get("type") == "final":
            state.status = "completed"
            return str(decision.get("answer", ""))

        if decision.get("type") != "tool":
            raise ValueError("Unknown decision type")

        name = decision.get("tool")
        args = decision.get("arguments", {})
        action_id = decision.get("action_id")
        started = time.perf_counter()

        try:
            result = execute_tool(name, args, context, action_id)
            state.observations.append({"tool": name, "ok": True, "result": result})
            logger.info("tool_succeeded run_id=%s tool=%s", state.run_id, name)
        except Exception as exc:
            state.observations.append({
                "tool": name, "ok": False, "error": type(exc).__name__
            })
            logger.warning(
                "tool_failed run_id=%s tool=%s error=%s",
                state.run_id, name, type(exc).__name__
            )
        finally:
            ms = (time.perf_counter() - started) * 1000
            logger.info("tool_duration run_id=%s tool=%s duration_ms=%.2f",
                        state.run_id, name, ms)
    return "Agent stopped"
```

`main.py`:

```python
import logging
from agent import AgentState, UserContext, run_agent

logging.basicConfig(level=logging.INFO)

def demo_decider(state):
    if not state.observations:
        return {"type": "tool", "tool": "list_projects", "arguments": {}}
    return {
        "type": "final",
        "answer": f"আপনার project list: {state.observations[-1]['result']}",
    }

if __name__ == "__main__":
    context = UserContext(user_id="user-1", tenant_id=10, role="member")
    state = AgentState(run_id="run-demo-001", goal="আমার project list দেখাও")
    print(run_agent(state, context, demo_decider))
```

একই directory-তে `agent.py` ও `main.py` রেখে run করুন:

```bash
python main.py
```

Expected: শুধু tenant 10-এর `HRM Platform` দেখা যাবে।

**গুরুত্বপূর্ণ সীমাবদ্ধতা:** এটি educational skeleton—demo data, simplified role, persistent approval নেই, real DB transaction নেই, API authentication নেই, actual LLM adapter নেই, MCP client integration নেই। `action_id` বাস্তব authenticated approval record-এর সঙ্গে verify করতে হবে; Pydantic validation, durable storage, idempotency, deadline, retry এবং tests যোগ করতে হবে।

## 9. Capstone acceptance checklist

- [ ] Unknown tool reject।
- [ ] Invalid arguments reject।
- [ ] Member write tool চালাতে পারে না।
- [ ] Admin approval ছাড়া sensitive action করতে পারে না।
- [ ] Tenant A, Tenant B-এর data দেখতে পায় না।
- [ ] Max step অতিক্রম হয় না।
- [ ] Retry policy আছে।
- [ ] Duplicate side effect idempotency দিয়ে আটকানো।
- [ ] Logs-এ secret/private HR data নেই।
- [ ] Unit test ও evaluation suite আছে।
- [ ] MCP tool discovery/invocation test হয়েছে।
- [ ] Failure-এ safe response আসে।

## 10. Final homework

1. SQLite persistence যোগ করুন।
2. প্রতিটি tool-এর Pydantic input schema তৈরি করুন।
3. `delete_project` approval gate দিয়ে যোগ করুন।
4. MCP server-এ read-only `list_projects` expose করুন।
5. MCP client দিয়ে tool discovery ও call করুন।
6. pytest-এ permission, tenant isolation, max steps ও invalid input test করুন।
7. ২০টি evaluation prompt দিয়ে tool selection accuracy মাপুন।

Phase 07-এ LangChain, LangGraph এবং Multi-Agent architecture শিখবেন।
