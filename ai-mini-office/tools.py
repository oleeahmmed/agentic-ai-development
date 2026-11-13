
from pathlib import Path

TASK_FILE = Path(__file__).parent / "tasks.txt"


def create_task(task: str):
    """Create and save a new task."""

    task = task.strip()

    if not task:
        return "Task cannot be empty."

    with open(TASK_FILE, "a", encoding="utf-8") as file:
        file.write(task + "\n")

    return f"Task created successfully: {task}"


def list_tasks():
    """Return all saved tasks."""

    if not TASK_FILE.exists():
        return []

    with open(TASK_FILE, "r", encoding="utf-8") as file:
        tasks = file.readlines()

    return [task.strip() for task in tasks if task.strip()]
