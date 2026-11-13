import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

sys.stdout.reconfigure(encoding="utf-8")

env_file = Path(__file__).parent / ".env"
load_dotenv(env_file)

api_key = os.getenv("LLM_API_KEY")
model = os.getenv("LLM_MODEL")
base_url = os.getenv("LLM_BASE_URL")

if not api_key or not model:
    print("00-setup/.env ফাইলে LLM_API_KEY আর LLM_MODEL দিন।")
    sys.exit()

client = OpenAI(api_key=api_key, base_url=base_url)

response = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "system",
            "content": "তুমি Little Office Ltd.-এর সহায়ক। সংক্ষেপে বাংলায় উত্তর দাও।",
        },
        {
            "role": "user",
            "content": "তুমি কে?",
        },
    ],
)

print(response.choices[0].message.content)
