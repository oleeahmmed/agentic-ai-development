# Chapter 03 — Error Handling, Retry, Timeout & Rate Limits

## 1. Error অনুযায়ী strategy

| Error | Strategy |
|---|---|
| Validation | input ঠিক করুন, retry নয় |
| Authentication | fail fast |
| Permission | retry নয় |
| Timeout | সীমিত retry; side effect যাচাই |
| Rate limit | backoff + jitter |
| Temporary 5xx | সীমিত retry |
| Not found | সাধারণত retry নয় |

## 2. Exponential backoff

```text
attempt 1 -> 1s
attempt 2 -> 2s
attempt 3 -> 4s
attempt 4 -> 8s
```

Random jitter যোগ করলে বহু client একসঙ্গে retry করে না।

## 3. Tenacity example

Install: `pip install tenacity`

`retry_demo.py`:

```python
import logging
from tenacity import retry, stop_after_attempt, wait_exponential
from tenacity import retry_if_exception_type, before_sleep_log

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("agent.retry")

class TemporaryServiceError(Exception):
    pass

attempts = 0

@retry(
    retry=retry_if_exception_type(TemporaryServiceError),
    stop=stop_after_attempt(4),
    wait=wait_exponential(multiplier=1, min=1, max=8),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    reraise=True,
)
def unstable_service():
    global attempts
    attempts += 1
    print("Attempt", attempts)
    if attempts < 3:
        raise TemporaryServiceError("Temporary outage")
    return {"status": "ok", "value": 42}

if __name__ == "__main__":
    print(unstable_service())
```

শুধু temporary exception retry করুন। Permanent error retry করলে খরচ ও latency বাড়ে।

## 4. Timeout

```python
import requests

response = requests.get("https://example.com", timeout=(3, 10))
response.raise_for_status()
print(response.status_code)
```

OpenAI SDK example:

```python
from openai import OpenAI

client = OpenAI(timeout=30.0, max_retries=2)
response = client.responses.create(
    model="gpt-4.1-mini",
    input="Explain timeout in one sentence."
)
print(response.output_text)
```

SDK-এর retry-এর উপর বড় retry loop বসালে মোট wait অনেক বেড়ে যেতে পারে। Retry budget হিসাব করুন।

## 5. Idempotency

Network timeout-এর পর `create_invoice` আবার call হলে duplicate invoice হতে পারে। Unique idempotency key ব্যবহার করুন।

```python
import sqlite3

def create_invoice(db_path: str, key: str, amount: int):
    if amount <= 0:
        raise ValueError("amount must be positive")

    with sqlite3.connect(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idempotency_key TEXT UNIQUE NOT NULL,
                amount INTEGER NOT NULL
            )
        """)
        old = conn.execute(
            "SELECT id, amount FROM invoices WHERE idempotency_key = ?", (key,)
        ).fetchone()
        if old:
            return {"invoice_id": old[0], "amount": old[1], "reused": True}

        cur = conn.execute(
            "INSERT INTO invoices (idempotency_key, amount) VALUES (?, ?)",
            (key, amount),
        )
        return {"invoice_id": cur.lastrowid, "amount": amount, "reused": False}

if __name__ == "__main__":
    print(create_invoice("demo.db", "request-001", 5000))
    print(create_invoice("demo.db", "request-001", 5000))
```

একই key দ্বিতীয়বার দিলে একই invoice record ফেরত আসে।

## 6. Rate limiting

Rate limit হতে পারে per user, tenant, tool বা global। বহু worker/server-এ in-memory counter যথেষ্ট নয়; Redis বা API gateway ব্যবহার করুন।

## 7. Safe error response

```python
def safe_error_response(exc: Exception) -> dict:
    if isinstance(exc, PermissionError):
        return {"ok": False, "error_code": "PERMISSION_DENIED",
                "message": "এই কাজটি করার অনুমতি নেই।"}
    if isinstance(exc, TimeoutError):
        return {"ok": False, "error_code": "UPSTREAM_TIMEOUT",
                "message": "সেবা থেকে সময়মতো উত্তর পাওয়া যায়নি।"}
    return {"ok": False, "error_code": "INTERNAL_ERROR",
            "message": "একটি সমস্যা হয়েছে।"}
```

Stack trace, API key, DB URL user-facing response-এ দেবেন না।

## 8. Homework

1. Retry শুধু temporary error-এ সীমাবদ্ধ করুন।
2. সর্বোচ্চ attempt ও maximum delay দিন।
3. `create_task`-এ idempotency key যোগ করুন।
4. Timeout-এর পর side effect হয়েছে কি না যাচাই করার flow আঁকুন।

**মূল কথা:** Retry করার আগে বুঝুন operation safe to retry কি না।
