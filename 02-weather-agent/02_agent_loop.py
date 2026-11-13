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

api_key = os.getenv("LLM_API_KEY")
model = os.getenv("LLM_MODEL")

if not api_key or not model:
    print("00-setup/.env ফাইলে LLM_API_KEY আর LLM_MODEL দিন।")
    sys.exit()

system_prompt = (base / "prompts" / "system.md").read_text(encoding="utf-8")

client = OpenAI(api_key=api_key, base_url=os.getenv("LLM_BASE_URL"))

messages = [{"role": "system", "content": system_prompt}]

print("আবহাওয়া এজেন্ট। exit = বন্ধ")

while True:
    question = input("তুমি: ").strip()

    if question == "exit":
        break

    if not question:
        continue

    messages.append({"role": "user", "content": question})

    for step in range(5):
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOLS,
        )
        message = response.choices[0].message
        messages.append(message)

        if not message.tool_calls:
            print("এজেন্ট:", message.content)
            break

        for call in message.tool_calls:
            name = call.function.name
            args = json.loads(call.function.arguments or "{}")
            result = run_tool(name, args)

            print("  [টুল]", name, args)
            print("  [ফলাফল]", result)

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": result,
                }
            )
    else:
        print("এজেন্ট: ৫ ধাপেও উত্তর মিলল না।")

print("বন্ধ হলো।")
