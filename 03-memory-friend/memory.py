import json
from pathlib import Path

FILE = Path(__file__).parent / "memories.json"


def load_all():
    if not FILE.exists():
        return {}

    return json.loads(FILE.read_text(encoding="utf-8"))


def save_all(data):
    text = json.dumps(data, ensure_ascii=False, indent=2)
    FILE.write_text(text, encoding="utf-8")


def get_memory(user_id):
    return load_all().get(user_id, {})


def save_memory(user_id, key, value):
    key = key.strip()
    value = value.strip()

    if not key or not value:
        return "key আর value দুটোই দরকার।"

    data = load_all()
    data.setdefault(user_id, {})[key] = value
    save_all(data)

    return f"মনে রাখলাম: {key} = {value}"


def forget_all(user_id):
    data = load_all()
    data[user_id] = {}
    save_all(data)

    return "সব স্মৃতি মুছে ফেলা হয়েছে।"
