from tools import create_task, list_tasks
from skill_loader import load_skill

# Skill Load
task_skill = load_skill("task-manager")

# System Instructions
SYSTEM_INSTRUCTIONS = f"""
You are an AI Personal Task Assistant.

Follow these skill instructions:

{task_skill}
"""

# Available Tools
AVAILABLE_TOOLS = {
    "create_task": create_task,
    "list_tasks": list_tasks
}

while True:
    command = input("create, list, or exit: ").strip().lower()

    if command == "create":
        task = input("Task: ")
        print(AVAILABLE_TOOLS["create_task"](task))
    elif command == "list":
        tasks = AVAILABLE_TOOLS["list_tasks"]()
        if tasks:
            for task in tasks:
                print(task)
        else:
            print("No tasks yet.")
    elif command == "exit":
        break
    else:
        print("Please enter create, list, or exit.")
