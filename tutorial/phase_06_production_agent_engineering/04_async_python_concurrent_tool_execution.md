# Chapter 04 — Async Python & Concurrent Tool Execution

## 1. Async কেন?

Independent I/O task sequential করলে wait time যোগ হয়। Concurrent execution-এ অপেক্ষাগুলো overlap করতে পারে।

```text
Sequential: A 2s + B 3s + C 1s = প্রায় 6s
Concurrent: A, B, C একসঙ্গে = প্রায় 3s
```

এটি কেবল independent কাজের জন্য; dependency থাকলে sequential চালান।

## 2. async / await

```python
import asyncio

async def fetch_data(name: str, delay: float):
    print(name, "started")
    await asyncio.sleep(delay)
    print(name, "finished")
    return {"name": name, "delay": delay}

async def main():
    results = await asyncio.gather(
        fetch_data("employees", 2),
        fetch_data("departments", 1),
        fetch_data("shifts", 3),
    )
    print(results)

if __name__ == "__main__":
    asyncio.run(main())
```

## 3. Sequential বনাম concurrent timing

```python
import asyncio
import time

async def job(name, seconds):
    await asyncio.sleep(seconds)
    return f"{name} done"

async def sequential():
    return [await job("A", 2), await job("B", 3), await job("C", 1)]

async def concurrent():
    return await asyncio.gather(
        job("A", 2), job("B", 3), job("C", 1)
    )

async def main():
    start = time.perf_counter()
    print(await sequential())
    print("Sequential:", round(time.perf_counter() - start, 2))
    start = time.perf_counter()
    print(await concurrent())
    print("Concurrent:", round(time.perf_counter() - start, 2))

asyncio.run(main())
```

## 4. Failure handling

```python
import asyncio

async def safe_tool(name):
    await asyncio.sleep(0.2)
    if name == "bad":
        raise RuntimeError("Service unavailable")
    return f"{name}: success"

async def main():
    results = await asyncio.gather(
        safe_tool("employees"),
        safe_tool("bad"),
        safe_tool("projects"),
        return_exceptions=True,
    )
    for result in results:
        if isinstance(result, Exception):
            print("Failed:", type(result).__name__)
        else:
            print("Result:", result)

asyncio.run(main())
```

## 5. Concurrency limit

```python
import asyncio

semaphore = asyncio.Semaphore(3)

async def limited_tool(item):
    async with semaphore:
        print("Starting", item)
        await asyncio.sleep(1)
        return item * 10

async def main():
    results = await asyncio.gather(*(limited_tool(i) for i in range(10)))
    print(results)

asyncio.run(main())
```

একবারে সর্বোচ্চ ৩টি task semaphore-এর ভিতরে চলবে।

## 6. Async tool registry

```python
import asyncio
from collections.abc import Awaitable, Callable
from typing import Any

async def get_employee_count(company_id: int) -> dict:
    await asyncio.sleep(0.3)  # বাস্তবে async DB/API call
    return {"company_id": company_id, "employee_count": 125}

async def get_open_tasks(company_id: int) -> dict:
    await asyncio.sleep(0.5)
    return {"company_id": company_id, "open_tasks": 18}

TOOLS: dict[str, Callable[..., Awaitable[Any]]] = {
    "get_employee_count": get_employee_count,
    "get_open_tasks": get_open_tasks,
}

async def execute_tool(name: str, arguments: dict):
    tool = TOOLS.get(name)
    if tool is None:
        raise ValueError("Unknown tool")
    return await tool(**arguments)

async def main():
    company_id = 7
    results = await asyncio.gather(
        execute_tool("get_employee_count", {"company_id": company_id}),
        execute_tool("get_open_tasks", {"company_id": company_id}),
    )
    print(results)

asyncio.run(main())
```

## 7. সতর্কতা

- Async I/O-bound কাজের জন্য; CPU-heavy কাজে process pool বিবেচনা করুন।
- Blocking function async loop-এর ভিতরে চালালে loop block হয়।
- Provider-এর async SDK interface ব্যবহার করুন।
- Parallel write-এর ordering/consistency ভাবুন।
- Cancellation, timeout ও concurrency limit দিন।
- User-controlled unlimited task তৈরি হতে দেবেন না।

## 8. Homework

তিনটি read-only tool async করুন, semaphore দিয়ে concurrency 2 করুন, একটি tool fail করলেও অন্য result সংগ্রহ করুন এবং parallel-safe বনাম sequential tool-এর তালিকা লিখুন।

**মূল কথা:** Async হলো I/O waiting overlap করার কৌশল; সব code স্বয়ংক্রিয়ভাবে দ্রুত হয় না।
