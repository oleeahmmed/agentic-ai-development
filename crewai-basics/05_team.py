import os
import sys
from pathlib import Path

from crewai import Agent, Crew, LLM, Process, Task
from crewai.tools import tool
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv(Path(__file__).parent.parent / "00-setup" / ".env")
os.environ["NO_PROXY"] = "localhost,127.0.0.1"

llm = LLM(
    model=f"openai/{os.getenv('LLM_MODEL')}",
    base_url=os.getenv("LLM_BASE_URL"),
    api_key=os.getenv("LLM_API_KEY"),
)

OUTPUT = Path(__file__).parent / "notice.md"


@tool("read_office_note")
def read_office_note() -> str:
    """অফিসের নোট ফাইলটি পড়ে লেখা ফেরত দেয়।"""
    note = Path(__file__).parent / "office_note.txt"
    return note.read_text(encoding="utf-8")


reader = Agent(
    role="নোট পাঠক",
    goal="অফিসের নোট পড়ে মূল কথা বের করা",
    backstory="তুমি ফাইল পড়ে সংক্ষেপে সারমর্ম বলতে পারো।",
    tools=[read_office_note],
    llm=llm,
    verbose=True,
)

writer = Agent(
    role="অফিস লেখক",
    goal="কর্মীদের জন্য ছোট ও পরিষ্কার বাংলা লেখা",
    backstory="তুমি Little Office Ltd.-এর অভিজ্ঞ লেখক।",
    llm=llm,
    verbose=True,
)

summary = Task(
    description="read_office_note টুল দিয়ে অফিসের নোটটি পড়ো। তারপর ৩টি বুলেটে মূল কথা বাংলায় লেখো।",
    expected_output="৩টি বাংলা বুলেট।",
    agent=reader,
)

notice = Task(
    description="আগের সারমর্ম থেকে কর্মীদের জন্য ৫ বাক্যের একটি বাংলা নোটিশ লেখো।",
    expected_output="৫ বাক্যের বাংলা নোটিশ।",
    agent=writer,
    context=[summary],
    output_file=str(OUTPUT),
)

crew = Crew(
    agents=[reader, writer],
    tasks=[summary, notice],
    process=Process.sequential,
    verbose=True,
    tracing=False,
)

print("\n--- শুরু ---")
result = crew.kickoff()
print("\n--- চূড়ান্ত ফল ---")
print(result)
print("\nসেভ হয়েছে:", OUTPUT)
