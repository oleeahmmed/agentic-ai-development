import os
import sys
from pathlib import Path

from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")

env_file = Path(__file__).parent / ".env"
load_dotenv(env_file)

print("Python:", sys.version.split()[0])
print(".env ফাইল:", "আছে" if env_file.exists() else "নেই")
print("LLM_API_KEY:", "আছে" if os.getenv("LLM_API_KEY") else "নেই")
print("LLM_BASE_URL:", os.getenv("LLM_BASE_URL", "নেই"))
print("LLM_MODEL:", os.getenv("LLM_MODEL", "নেই"))
print()

if os.getenv("LLM_API_KEY") and os.getenv("LLM_MODEL"):
    print("সব ঠিক আছে। এখন চালান: python 00-setup/hello_llm.py")
else:
    print("আগে 00-setup/.env ঠিক করুন।")
