# Chapter 05 — Logging, Observability, Evaluation & Testing

## 1. Observability

- Logs: কী ঘটেছে।
- Metrics: কতবার/কত দ্রুত ঘটেছে।
- Traces: একটি request-এর end-to-end journey।

Agent ভুল tool বেছে নিলে বা latency বাড়লে এগুলো দিয়ে কারণ খুঁজবেন।

## 2. Structured JSON logging

`logging_demo.py`:

```python
import json
import logging
from datetime import datetime, timezone

class JsonFormatter(logging.Formatter):
    def format(self, record):
        data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        for key in ("run_id", "user_id", "tool_name", "duration_ms", "error_code"):
            if hasattr(record, key):
                data[key] = getattr(record, key)
        return json.dumps(data, ensure_ascii=False)

logger = logging.getLogger("agent")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger.addHandler(handler)

logger.info("Tool executed", extra={
    "run_id": "run-001",
    "user_id": "user-123",
    "tool_name": "list_tasks",
    "duration_ms": 45,
})
```

## 3. কী log করবেন?

Log করতে পারেন: run ID, event, tool name, latency, attempt, safe error code, model/provider identifier, token usage।

Log করবেন না বা redact করুন: API key, access token, password, salary, national ID, private HR record, raw private prompt/result।

Logs-এর access control ও retention policy রাখুন।

## 4. Timing decorator

```python
import time
import logging
from functools import wraps

logger = logging.getLogger(__name__)

def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            ms = (time.perf_counter() - start) * 1000
            logger.info("%s completed in %.2f ms", func.__name__, ms)
    return wrapper

@measure_time
def sample_tool():
    time.sleep(0.2)
    return "ok"
```

এটি synchronous function-এর decorator; async function-এর জন্য async decorator প্রয়োজন।

## 5. pytest fundamentals

`calculator.py`:

```python
def add(a: int, b: int) -> int:
    return a + b

def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

`test_calculator.py`:

```python
import pytest
from calculator import add, divide

def test_add():
    assert add(2, 3) == 5

def test_divide():
    assert divide(10, 2) == 5

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)
```

Run: `pytest -v`

## 6. Tool contract test

```python
import pytest
from pydantic import BaseModel, Field, ConfigDict, ValidationError

class SearchTasksInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    project_id: int = Field(gt=0)

def test_valid():
    assert SearchTasksInput.model_validate({"project_id": 5}).project_id == 5

def test_invalid_id():
    with pytest.raises(ValidationError):
        SearchTasksInput.model_validate({"project_id": 0})

def test_extra_field_rejected():
    with pytest.raises(ValidationError):
        SearchTasksInput.model_validate({"project_id": 5, "tenant_id": 999})
```

প্রতিটি tool-এ valid input, invalid input, permission, tenant boundary, unknown fields, safe errors এবং idempotency test করুন।

## 7. Agent evaluation

```python
CASES = [
    {
        "question": "আমার open task কয়টি?",
        "expected_tool": "list_open_tasks",
        "must_not_call": ["delete_project"],
    },
    {
        "question": "Project 12-এর task দেখাও",
        "expected_tool": "list_project_tasks",
        "must_not_call": ["send_email"],
    },
]
```

Measure করুন:
- task success rate
- correct tool selection
- argument correctness
- unauthorized attempt
- latency
- token/cost
- approval compliance

LLM output nondeterministic হতে পারে; exact text equality ছাড়াও structured criteria ও human review ব্যবহার করুন।

## 8. Tracing

```text
agent.run
  ├── context.build
  ├── llm.request
  ├── tool.authorize
  ├── tool.execute
  ├── llm.followup
  └── response.validate
```

OpenTelemetry instrumentation standard হিসেবে ব্যবহার করতে পারেন; compatible collector/backend দিয়ে trace পাঠান। Sensitive payload span attribute-এ রাখবেন না।

## 9. Homework

প্রতিটি log-এ run ID দিন, একটি tool-এর success/validation/permission test লিখুন, ১০টি evaluation case তৈরি করুন এবং unauthorized attempt-এর metric নির্ধারণ করুন।

**মূল কথা:** “Agent ভালো কাজ করছে” অনুভূতি দিয়ে নয়—logs, metrics, traces ও repeatable evaluation দিয়ে যাচাই করুন।
