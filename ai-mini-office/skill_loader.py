
from pathlib import Path

# সব Skill এই Folder-এর ভিতরে থাকবে
SKILLS_DIR = Path(__file__).parent / "skills"


def load_skill(skill_name: str) -> str:
    """
    নির্দিষ্ট Skill-এর SKILL.md পড়বে
    এবং মূল Instructions ফেরত দেবে।
    """

    # Skill-এর Folder খুঁজে বের করা
    skill_file = SKILLS_DIR / skill_name / "SKILL.md"

    # Skill না থাকলে Error
    if not skill_file.exists():
        raise FileNotFoundError(
            f"Skill পাওয়া যায়নি: {skill_name}"
        )

    # সম্পূর্ণ ফাইল পড়া
    content = skill_file.read_text(
        encoding="utf-8"
    )

    # YAML Frontmatter বাদ দেওয়া
    if content.startswith("---"):

        frontmatter_end = content.find("\n---", 3)

        if frontmatter_end != -1:
            content = content[frontmatter_end + 4:]

    # মূল Instructions ফেরত
    return content.strip()


if __name__ == "__main__":

    skill = load_skill("task-manager")

    print("Skill সফলভাবে Load হয়েছে!")
    print("-" * 40)

    print(skill)
