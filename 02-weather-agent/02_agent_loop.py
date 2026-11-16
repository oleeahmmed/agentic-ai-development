import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from tools import TOOLS, run_tool

sys.stdout.reconfigure(encoding="utf-8")

base = Path(__file__).parent
load_dotenv(base.parent / "00-setup" / ".env")

model = os.getenv("LLM_MODEL")

if not os.getenv("LLM_API_KEY") or not model:
    print("00-setup/.env ফাইলে LLM_API_KEY আর LLM_MODEL দিন।")
    sys.exit()

system_prompt = (base / "prompts" / "system.md").read_text(encoding="utf-8")

client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL"),
)

messages = [{"role": "system", "content": system_prompt}]

print("আবহাওয়া এজেন্ট। mem = মেমোরি দেখো, exit = বন্ধ")

while True:
    question = input("\nতুমি: ").strip()

    if question == "exit":
        break

    if question == "mem":
        for number, item in enumerate(messages, 1):
            role = item["role"] if isinstance(item, dict) else item.role
            print(number, role)
        continue

    if not question:
        continue

    messages.append({"role": "user", "content": question})
    answer = None

    for step in range(1, 5):
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOLS,
        )
        message = response.choices[0].message
        messages.append(message)

        if not message.tool_calls:
            answer = message.content
            break

        for call in message.tool_calls:
            name = call.function.name
            args = json.loads(call.function.arguments or "{}")
            result = run_tool(name, args)

            print(f"[ধাপ {step}] মডেল বাছাই করল: {name} {args}")
            print(f"[ধাপ {step}] টুলের ফল: {result}")

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": result,
                }
            )

    print("এজেন্ট:", answer or "৪ ধাপেও উত্তর পাওয়া যায়নি।")
    print(f"[মেমোরি] এখন {len(messages)}টি মেসেজ জমেছে")

print("বন্ধ হলো।")
