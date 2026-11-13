import json
from pathlib import Path

file = Path(__file__).parent / "customer.json"

customer = {
    "name": "রাফি",
    "city": "চট্টগ্রাম",
    "orders": 3,
}

text = json.dumps(customer, ensure_ascii=False, indent=2)
file.write_text(text, encoding="utf-8")

text = file.read_text(encoding="utf-8")
data = json.loads(text)

print(data)
print("নাম:", data["name"])
