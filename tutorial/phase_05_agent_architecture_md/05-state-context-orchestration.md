# Chapter 05 — State, Context & Orchestration

Multi-step Agent-এ state না রাখলে আগের কাজের ফল, plan progress ও error হারিয়ে যায়। এই Chapter-এ Agent state এবং orchestration-এর ভিত্তি তৈরি করব।

## 1. State কী?

State হলো বর্তমান execution-এর structured snapshot।

```python
state = {
    "run_id": "run_001",
    "goal": "Create project and tasks",
    "status": "in_progress",
    "plan": [],
    "artifacts": {
        "project_id": None,
        "task_ids": [],
    },
    "observations": [],
    "tool_calls": 0,
    "current_step": None,
    "error": None,
}
```

## 2. Context বনাম State বনাম Memory

| বিষয় | অর্থ |
|---|---|
| Context | এই model call-এ model যা দেখতে পাচ্ছে |
| State | চলমান workflow-এর structured data |
| Memory | ভবিষ্যৎ conversation বা run-এর জন্য সংরক্ষিত তথ্য |
| History | আগের message ও event-এর record |

সব history model-এ পাঠানোর দরকার নেই। প্রয়োজনীয় state ও relevant context বেছে পাঠাও।

## 3. State update function

```python
def record_tool_result(state: dict, tool_name: str, result):
    state["tool_calls"] += 1

    state["observations"].append({
        "tool": tool_name,
        "result": result,
    })

    return state


if __name__ == "__main__":
    agent_state = {
        "tool_calls": 0,
        "observations": [],
    }

    record_tool_result(agent_state, "add_numbers", 15)
    print(agent_state)
```

## 4. Orchestration-এর দায়িত্ব

Orchestrator/controller:
- Goal ও plan গ্রহণ করে
- Ready step নির্বাচন করে
- Model বা deterministic logic-কে next action জিজ্ঞাসা করে
- Tool allowlist যাচাই করে
- Permission ও confirmation check করে
- Tool execute করে
- State update করে
- Stop condition পরীক্ষা করে

LLM-কে সব control flow-এর মালিক বানাবে না। নিরাপত্তা ও deterministic নিয়ম Python controller-এ থাকবে।

## 5. Event log

State-এর পাশাপাশি event record রাখা উপকারী:

```python
event = {
    "event_type": "tool_completed",
    "tool_name": "create_project",
    "success": True,
    "timestamp": "2026-01-01T10:00:00Z",
}
```

বাস্তব application-এ timestamp current UTC time দিয়ে তৈরি করবে। Event log দিয়ে debugging ও audit করা যায়। Password, API key বা sensitive payload log করবে না।

## 6. Persistence

ছোট demo-তে memory-তে dictionary রাখা যায়। Process বন্ধ হলে state হারাবে। দীর্ঘ workflow-এর জন্য database-এ সংরক্ষণ দরকার:
- run metadata
- current status
- plan steps
- tool call records
- created resource IDs
- approval status

একই action retry হলে duplicate resource তৈরি হতে পারে। তাই idempotency key বা duplicate check design করো।

## 7. Context assembly

Model-কে পুরো database বা সব history পাঠিও না। প্রয়োজনীয় তথ্য দাও:

```python
model_context = {
    "goal": state["goal"],
    "current_step": state["current_step"],
    "completed_steps": [
        item for item in state["plan"]
        if item["status"] == "completed"
    ],
    "recent_observations": state["observations"][-5:],
}
```

## 8. Exercise

1. `state`-এ `created_at` ও `updated_at` যোগ করো।
2. Tool result record করার function লেখো।
3. সর্বশেষ পাঁচটি observation model context-এ রাখো।
4. একই tool action duplicate হলে কীভাবে চিনবে তা design করো।
5. Process restart-এর পর state recover করার জন্য SQLite table design করো।

**Chapter outcome:** State, context, history ও memory-এর পার্থক্য বুঝে Agent orchestration design করতে পারবে।
