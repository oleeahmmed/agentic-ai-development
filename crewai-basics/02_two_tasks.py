import os
import sys
from pathlib import Path

from crewai import Agent, Crew, LLM, Process, Task
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv(Path(__file__).parent.parent / "00-setup" / ".env")
os.environ["NO_PROXY"] = "localhost,127.0.0.1"

llm = LLM(
    model=f"openai/{os.getenv('LLM_MODEL')}",
    base_url=os.getenv("LLM_BASE_URL"),
    api_key=os.getenv("LLM_API_KEY"),
)

writer = Agent(
    role="অফিস লেখক",
    goal="কর্মীদের জন্য ছোট ও পরিষ্কার বাংলা লেখা",
    backstory="তুমি Little Office Ltd.-এর অভিজ্ঞ লেখক।",
    llm=llm,
    verbose=True,
)

outline = Task(
    description="কর্মীদের জন্য 'সাপ্তাহিক মিটিং' নিয়ে ৩টি পয়েন্টের খসড়া বাংলায় লেখো।",
    expected_output="৩টি সংক্ষিপ্ত পয়েন্ট।",
    agent=writer,
)

notice = Task(
    description="আগের খসড়ার ৩টি পয়েন্ট নিয়ে ৪ বাক্যের একটি পরিষ্কার বাংলা নোটিশ লেখো।",
    expected_output="৪ বাক্যের বাংলা নোটিশ।",
    agent=writer,
    context=[outline],
)

crew = Crew(
    agents=[writer],
    tasks=[outline, notice],
    process=Process.sequential,
    verbose=True,
    tracing=False,
)

print("\n--- শুরু ---")
result = crew.kickoff()
print("\n--- চূড়ান্ত ফল ---")
print(result)
