import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

import memory

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

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "save_memory",
            "description": "ব্যবহারকারী সম্পর্কে স্থায়ী তথ্য মনে রাখে।",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "যেমন নাম, শহর, প্রিয় খাবার"},
                    "value": {"type": "string", "description": "মনে রাখার মান"},
                },
                "required": ["key", "value"],
            },
        },
    },
]


def start_messages(user_id):
    facts = memory.get_memory(user_id)

    if facts:
        lines = [f"- {key}: {value}" for key, value in facts.items()]
        facts_text = "\n".join(lines)
    else:
        facts_text = "এখনো কিছু জানা নেই।"

    content = system_prompt + "\n\n## যা মনে আছে\n\n" + facts_text

    return [{"role": "system", "content": content}]


def show_memory(user_id):
    facts = memory.get_memory(user_id)

    if not facts:
        print("এখনো কিছু মনে নেই।")
        return

    for key, value in facts.items():
        print(f"- {key}: {value}")


user_id = input("User id (Enter = rafi): ").strip() or "rafi"
messages = start_messages(user_id)

print(f"মিতুর সাথে কথা বলুন ({user_id})।")
print("/memory = স্মৃতি দেখা, /forget = মুছে ফেলা, /reset = কথোপকথন নতুন, exit = বন্ধ")

while True:
    question = input("তুমি: ").strip()

    if question == "exit":
        break

    if question == "/memory":
        show_memory(user_id)
        continue

    if question == "/forget":
        print(memory.forget_all(user_id))
        messages = start_messages(user_id)
        continue

    if question == "/reset":
        messages = start_messages(user_id)
        print("কথোপকথন রিসেট হলো। স্মৃতি ঠিক আছে।")
        continue

    if not question:
        continue

    messages[0] = start_messages(user_id)[0]
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
            print("মিতু:", message.content)
            break

        for call in message.tool_calls:
            args = json.loads(call.function.arguments or "{}")
            result = memory.save_memory(
                user_id,
                args.get("key", ""),
                args.get("value", ""),
            )

            print("  [স্মৃতি]", result)

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": result,
                }
            )
    else:
        print("মিতু: উত্তর তৈরিতে সমস্যা হলো।")

print("বন্ধ হলো।")
