import json
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from langgraph.types import interrupt
from openai import OpenAI

import tools

base = Path(__file__).parent
load_dotenv(base.parent / "00-setup" / ".env")

api_key = os.getenv("LLM_API_KEY")
model = os.getenv("LLM_MODEL")

if not api_key or not model:
    raise SystemExit("00-setup/.env ফাইলে LLM_API_KEY আর LLM_MODEL দিন।")

client = OpenAI(api_key=api_key, base_url=os.getenv("LLM_BASE_URL"))
system_prompt = (base / "prompts" / "system.md").read_text(encoding="utf-8")


def ask(prompt):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content.strip()


def ask_json(prompt):
    text = ask(prompt).strip()
    text = text.strip("`").strip()

    if text.startswith("json"):
        text = text[4:].strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def source_text(sources, limit=2500):
    parts = []

    for number, source in enumerate(sources, 1):
        parts.append(f"[{number}] {source['title']}\n{source['text'][:limit]}")

    return "\n\n".join(parts)


def plan_node(state):
    question = state["question"]

    data = ask_json(
        f"প্রশ্ন: {question}\n\n"
        "এই প্রশ্নের উত্তর খুঁজতে উইকিপিডিয়ায় ব্যবহারের জন্য ২–৩টি ছোট ইংরেজি সার্চ প্রশ্ন লেখো। "
        'শুধু JSON তালিকা দাও, যেমন: ["query one", "query two"]'
    )

    if not isinstance(data, list) or not data:
        queries = [question]
    else:
        queries = [str(item) for item in data[:3]]

    return {"queries": queries}


def search_node(state):
    sources = list(state["sources"])
    seen = {source["url"] for source in sources}
    log = []

    for query in state["queries"]:
        log.append(query)

        for page in tools.search_and_read(query, limit=2):
            if page["url"] in seen:
                continue

            seen.add(page["url"])
            sources.append(page)

    return {"sources": sources, "search_log": log}


def summarize_node(state):
    if not state["sources"]:
        return {"summary": ""}

    summary = ask(
        f"প্রশ্ন: {state['question']}\n\n"
        f"উৎস:\n{source_text(state['sources'])}\n\n"
        "শুধু উৎসের তথ্য দিয়ে বাংলায় ২৫০ শব্দের মধ্যে সারাংশ লেখো। "
        "প্রতিটি তথ্যের পাশে [1], [2] এভাবে উৎস নম্বর দাও।"
    )

    return {"summary": summary}


def critique_node(state):
    if not state["sources"]:
        return {"enough": False, "gaps": "কোনো উৎস পাওয়া যায়নি।"}

    data = ask_json(
        f"প্রশ্ন: {state['question']}\n\n"
        f"সারাংশ:\n{state['summary']}\n\n"
        "এই সারাংশ প্রশ্নের সম্পূর্ণ উত্তর দেয় কি? না দিলে কী তথ্য বাকি, সংক্ষেপে লেখো। "
        'শুধু JSON: {"enough": true অথবা false, "gaps": "বাকি তথ্য"}'
    )

    if not isinstance(data, dict):
        return {"enough": True, "gaps": ""}

    return {
        "enough": bool(data.get("enough", True)),
        "gaps": str(data.get("gaps", "")),
    }


def revise_node(state):
    data = ask_json(
        f"মূল প্রশ্ন: {state['question']}\n\n"
        f"ঘাটতি: {state['gaps']}\n\n"
        f"আগে যা খোঁজা হয়েছে: {', '.join(state['search_log'])}\n\n"
        "ঘাটতি ভরাতে উইকিপিডিয়ায় ১–২টি নতুন ইংরেজি সার্চ প্রশ্ন লেখো। "
        "শুধু JSON তালিকা দাও।"
    )

    if isinstance(data, list) and data:
        queries = [str(item) for item in data[:2]]
    else:
        queries = [state["question"] + " details"]

    return {"queries": queries, "rounds": state["rounds"] + 1}


def approve_node(state):
    answer = interrupt("রিপোর্ট লেখা হবে? (y/n)")

    return {"approved": str(answer).strip().lower().startswith("y")}


def write_node(state):
    body = ask(
        f"প্রশ্ন: {state['question']}\n\n"
        f"উৎস:\n{source_text(state['sources'])}\n\n"
        "এই প্রশ্নের উত্তর দিয়ে বাংলায় ৪০০–৬০০ শব্দের একটি রিপোর্ট লেখো। "
        "প্রতিটি দাবির পাশে [1], [2] এভাবে উৎস নম্বর দাও। "
        "উৎসে না থাকা কোনো তথ্য লিখো না।"
    )

    lines = [f"# {state['question']}", "", body, "", "## উৎস", ""]

    for number, source in enumerate(state["sources"], 1):
        lines.append(f"{number}. [{source['title']}]({source['url']})")

    folder = base / "reports"
    folder.mkdir(exist_ok=True)

    name = "report-" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".md"
    file = folder / name
    file.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return {"report_path": str(file)}
