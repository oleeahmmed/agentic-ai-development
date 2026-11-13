"""Phase 0 — পরিবেশ যাচাই। এটি কোনো নেটওয়ার্ক কল করে না।"""

import importlib.util
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).parent
ENV_PATH = BASE_DIR / ".env"

results: list[tuple[bool, str, str]] = []


def check(label: str, ok: bool, detail: str = "") -> None:
    results.append((ok, label, detail))


major, minor = sys.version_info[:2]
check("Python 3.11+", (major, minor) >= (3, 11), f"পাওয়া গেছে {major}.{minor}")

for package, import_name in [
    ("openai", "openai"),
    ("python-dotenv", "dotenv"),
    ("httpx", "httpx"),
]:
    found = importlib.util.find_spec(import_name) is not None
    check(
        f"প্যাকেজ: {package}",
        found,
        "" if found else "pip install -r 00-setup/requirements.txt",
    )

check(
    ".env ফাইল",
    ENV_PATH.exists(),
    "" if ENV_PATH.exists() else "নেই — .env.example কপি করে .env বানান",
)

if ENV_PATH.exists():
    load_dotenv(ENV_PATH)

key = os.getenv("LLM_API_KEY", "").strip()
model = os.getenv("LLM_MODEL", "").strip()

check(
    "LLM_API_KEY সেট",
    bool(key) and not key.startswith("sk-..."),
    "" if key else ".env-এ আসল key দিন",
)
check("LLM_MODEL সেট", bool(model), model or ".env-এ মডেলের নাম দিন")

print()
for ok, label, detail in results:
    status = "OK  " if ok else "FAIL"
    suffix = f" — {detail}" if detail else ""
    print(f"[{status}] {label}{suffix}")

failed = [item for item in results if not item[0]]
print()

if failed:
    print(f"{len(failed)}টি ধাপ বাকি। উপরের নির্দেশ দেখে ঠিক করুন।")
    sys.exit(1)

print("সব ঠিক আছে। এখন চালান:")
print("  .venv/Scripts/python.exe 00-setup/hello_llm.py")
