import json
from pathlib import Path

file = Path(__file__).parent / "tasks.json"

if file.exists():
    tasks = json.loads(file.read_text(encoding="utf-8"))
else:
    tasks = []

while True:
    command = input("কমান্ড (add / list / exit): ").strip()

    if command == "add":
        task = input("নতুন কাজ: ").strip()
        if task:
            tasks.append(task)
            text = json.dumps(tasks, ensure_ascii=False, indent=2)
            file.write_text(text, encoding="utf-8")
            print("সেভ হয়েছে।")
        else:
            print("খালি কাজ সেভ হবে না।")

    elif command == "list":
        if tasks:
            for number, task in enumerate(tasks, start=1):
                print(number, "-", task)
        else:
            print("কোনো কাজ নেই।")

    elif command == "exit":
        break

    else:
        print("add, list বা exit লিখুন।")
