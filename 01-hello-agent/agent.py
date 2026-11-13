import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

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
total_tokens = 0

print("মিতুর সাথে কথা বলুন।")
print("/reset = নতুন কথোপকথন, exit = বন্ধ")

while True:
    question = input("তুমি: ").strip()

    if question == "exit":
        break

    if question == "/reset":
        messages = [{"role": "system", "content": system_prompt}]
        total_tokens = 0
        print("নতুন কথোপকথন শুরু হয়েছে।")
        continue

    if not question:
        continue

    messages.append({"role": "user", "content": question})

    response = client.chat.completions.create(model=model, messages=messages)
    answer = response.choices[0].message.content
    messages.append({"role": "assistant", "content": answer})

    print("মিতু:", answer)

    total_tokens = total_tokens + response.usage.total_tokens
    print(f"token: {response.usage.total_tokens} | মোট: {total_tokens}")

print("কথোপকথন বন্ধ হলো।")
