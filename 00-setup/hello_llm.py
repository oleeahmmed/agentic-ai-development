"""Phase 0 — প্রথম LLM কল।

চালান:
    .venv/Scripts/python.exe 00-setup/hello_llm.py
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import APIConnectionError, AuthenticationError, OpenAI

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(ENV_PATH)

SYSTEM_PROMPT = (
    "তুমি Little Office Ltd.-এর একজন সহায়ক অফিস অ্যাসিস্ট্যান্ট। "
    "সংক্ষেপে বাংলায় উত্তর দাও।"
)
USER_PROMPT = "তুমি কে? এক বাক্যে বলো।"


def main() -> None:
    api_key = os.getenv("LLM_API_KEY", "").strip()
    model = os.getenv("LLM_MODEL", "gpt-4.1-mini").strip()
    base_url = os.getenv("LLM_BASE_URL", "").strip() or None

    if not api_key or api_key.startswith("sk-..."):
        print("LLM_API_KEY পাওয়া যায়নি বা এখনো placeholder আছে।")
        print("১) 00-setup/.env.example কপি করে 00-setup/.env বানান")
        print("২) সেখানে আসল key বসান")
        sys.exit(1)

    client = OpenAI(api_key=api_key, base_url=base_url)

    print(f"মডেল     : {model}")
    print(f"Base URL : {base_url or 'OpenAI ডিফল্ট'}")
    print(f"প্রশ্ন     : {USER_PROMPT}")
    print("-" * 55)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": USER_PROMPT},
            ],
        )
    except AuthenticationError:
        print("401: API key ভুল বা মেয়াদোত্তীর্ণ। .env আবার দেখুন।")
        sys.exit(1)
    except APIConnectionError:
        print("নেটওয়ার্ক সমস্যা: ইন্টারনেট বা LLM_BASE_URL ঠিক আছে কি না দেখুন।")
        sys.exit(1)
    except Exception as error:
        print(f"কল ব্যর্থ হয়েছে: {type(error).__name__}: {error}")
        sys.exit(1)

    print(response.choices[0].message.content)
    print("-" * 55)

    usage = response.usage
    if usage:
        print(
            "Tokens: "
            f"input={usage.prompt_tokens}, "
            f"output={usage.completion_tokens}, "
            f"total={usage.total_tokens}"
        )

    print("\nPhase 0 সফল। এখন README-এর ৯ নম্বর ধাপে যান।")


if __name__ == "__main__":
    main()
