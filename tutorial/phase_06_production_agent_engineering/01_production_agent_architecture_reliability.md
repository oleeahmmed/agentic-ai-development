# Chapter 01 — Production Agent Architecture & Reliability

## 1. Prototype বনাম production

Prototype-এ user → LLM → tool → result → LLM loop থাকলেই চলে। Production system-এ জানতে হবে: duplicate request হলে কী হবে, tool fail করলে কী হবে, permission না থাকলে কী হবে, restart হলে state থাকবে কি না।

| বিষয় | Prototype | Production-minded design |
|---|---|---|
| Tool access | সব tool | allowlist + permission |
| Execution | unbounded | max steps + deadline |
| Error | print | typed error + retry policy |
| State | variable | durable storage |
| Security | prompt | code-level enforcement |
| Monitoring | print | logs + metrics + traces |
| Side effects | immediate | approval + idempotency |

## 2. Architecture

```text
User -> API/CLI -> Authentication -> Authorization
    -> Request validation / Rate limit
    -> Agent Orchestrator
         | Context builder
         | Policy / approval gate
         | LLM adapter
         | Tool registry -> DB / APIs / MCP
         | State / memory store
    -> Result validation -> Response
    -> Logs / Metrics / Traces / Evaluation
```

LLM সিদ্ধান্ত প্রস্তাব করে; application code policy enforce করে।

## 3. Reliability principles

1. Bounded execution: সর্বোচ্চ step/tool call নির্ধারণ।
2. Deadline: request কতক্ষণ চলবে তার সীমা।
3. Idempotency: retry হলেও duplicate side effect নয়।
4. Explicit state: run ID, user ID, status, result, error।
5. Fail safely: uncertain অবস্থায় destructive action নয়।
6. Human approval: delete, email, payment, deployment-এর আগে approval।
7. Graceful degradation: optional tool unavailable হলে পরিষ্কারভাবে জানানো।

## 4. Minimal bounded runner

`agent_runner.py`:

```python
from dataclasses import dataclass, field
from typing import Any, Callable

@dataclass
class AgentState:
    user_id: str
    goal: str
    step_count: int = 0
    max_steps: int = 5
    status: str = "running"
    observations: list[str] = field(default_factory=list)

def run_agent(state: AgentState, decide: Callable, tools: dict) -> str:
    while state.status == "running":
        if state.step_count >= state.max_steps:
            state.status = "limit_reached"
            return "সর্বোচ্চ step limit শেষ হয়েছে।"

        state.step_count += 1
        decision = decide(state)

        if decision.get("action") == "final":
            state.status = "completed"
            return str(decision.get("answer", ""))

        name = decision.get("tool")
        arguments = decision.get("arguments", {})
        if name not in tools or not isinstance(arguments, dict):
            state.observations.append("Invalid or unknown tool call")
            continue

        try:
            result = tools[name](**arguments)
            state.observations.append(f"{name}: {result}")
        except Exception as exc:
            state.observations.append(f"{name} failed: {type(exc).__name__}")

    return "Agent stopped"

def add_numbers(a: int, b: int) -> int:
    return a + b

def demo_decider(state):
    if not state.observations:
        return {"action": "tool", "tool": "add", "arguments": {"a": 12, "b": 30}}
    return {"action": "final", "answer": state.observations[-1]}

if __name__ == "__main__":
    s = AgentState(user_id="user-1", goal="12 + 30")
    print(run_agent(s, demo_decider, {"add": add_numbers}))
```

Run: `python agent_runner.py`

## 5. Durable run state

Database-এ রাখার মতো field:
- `run_id`, `user_id`, `tenant_id`, `goal`
- `status`: queued/running/waiting_approval/completed/failed
- `step_count`, `created_at`, `updated_at`
- `result`, `error_code`, `idempotency_key`

Sensitive prompt বা ব্যক্তিগত তথ্য অকারণে log করবেন না।

## 6. Homework

1. `deadline_seconds` যোগ করুন।
2. `waiting_approval` status implement করুন।
3. `delete_file`-এর আগে approval gate বসান।
4. একই request দুইবার এলে duplicate project তৈরি হওয়া ঠেকান।

**মূল কথা:** Production reliability আসে deterministic application code, bounded execution এবং explicit policy থেকে।
