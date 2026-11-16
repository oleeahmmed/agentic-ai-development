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

editor = Agent(
    role="বাংলা সম্পাদক",
    goal="লেখার বানান, বাক্য ও স্পষ্টতা ঠিক করা",
    backstory="তুমি বাংলা ভাষার সম্পাদক। লেখা ছোট ও স্পষ্ট করতে জানো।",
    llm=llm,
    verbose=True,
)

draft = Task(
    description="কর্মীদের জানাও যে ২০ নভেম্বর সকাল ১০টায় টিম মিটিং হবে। ১০ লাইনের মধ্যে আনুষ্ঠানিক বাংলা নোটিশ লেখো।",
    expected_output="একটি বাংলা মিটিং নোটিশ।",
    agent=writer,
)

checked = Task(
    description="আগের নোটিশটি পড়ো। বানান ও বাক্য ঠিক করো। চূড়ান্ত নোটিশটি পুরোটা লেখো, তার নিচে আলাদা লাইনে 'সম্পাদিত' লেখো।",
    expected_output="সম্পাদিত ও পরিষ্কার বাংলা নোটিশ।",
    agent=editor,
    context=[draft],
)

crew = Crew(
    agents=[writer, editor],
    tasks=[draft, checked],
    process=Process.sequential,
    verbose=True,
    tracing=False,
)

print("\n--- শুরু ---")
result = crew.kickoff()
print("\n--- চূড়ান্ত ফল ---")
print(result)
