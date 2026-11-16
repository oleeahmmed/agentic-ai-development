# Chapter 04 — Prompt Engineering & Message Architecture

**সময়:** ৪ ঘণ্টা  
**লক্ষ্য:** Instructions, context, examples এবং output format ব্যবহার করে model-কে স্পষ্ট task দেওয়া।

## 1. Prompt কী?

Prompt হলো model-কে দেওয়া input বা নির্দেশনা। ভালো prompt-এ থাকে:
- Objective
- Context
- Constraints
- Expected output format
- প্রয়োজন হলে examples

অস্পষ্ট:

```text
Explain Django.
```

আরও নির্দিষ্ট:

```text
তুমি একজন Django শিক্ষক।
Beginner-কে Django Model ব্যাখ্যা করো।
বাংলায় একটি runnable example দাও।
Code-এর গুরুত্বপূর্ণ line ব্যাখ্যা করো।
শেষে ৩টি practice question দাও।
```

## 2. Message roles

সাধারণ conversation-এ:
- **System/Developer instructions:** Assistant-এর আচরণ ও নিয়ম নির্ধারণ।
- **User:** ব্যবহারকারীর অনুরোধ।
- **Assistant:** Model-এর উত্তর।

Responses API-তে আমরা `instructions` এবং `input` ব্যবহার করব। API-র role ও message format documentation অনুযায়ী বদলাতে পারে।

## 3. Practical — Prompt comparison

`prompt_compare.py`:

```python
from openai import OpenAI
from config import OPENAI_API_KEY, MODEL_NAME

client = OpenAI(api_key=OPENAI_API_KEY)
question = "Explain Python function."

prompts = {
    "basic": "Explain Python function.",
    "structured": """
তুমি একজন beginner-friendly Python শিক্ষক।
বাংলায় Python function ব্যাখ্যা করো।
1. সংজ্ঞা দাও
2. বাস্তব উদাহরণ দাও
3. সম্পূর্ণ Python code দাও
4. Code-এর গুরুত্বপূর্ণ line ব্যাখ্যা করো
5. শেষে ২টি practice task দাও
"""
}

for label, instructions in prompts.items():
    print("\\n", "=" * 50)
    print("PROMPT:", label)

    response = client.responses.create(
        model=MODEL_NAME,
        instructions=instructions,
        input=question,
    )
    print(response.output_text)
```

চালাও:

```bash
python prompt_compare.py
```

দুটি output তুলনা করো। Structured prompt সাধারণত output-এর কাঠামো স্পষ্ট করে; exact ফল model অনুযায়ী বদলাবে।

## 4. Zero-shot ও Few-shot

**Zero-shot:** উদাহরণ ছাড়াই কাজ দেওয়া।

```text
এই বাক্যটি positive না negative?
আজকের দিনটি খুব সুন্দর।
```

**Few-shot:** কয়েকটি example দেখিয়ে pattern দেওয়া।

```text
বাক্য: আমি খুব খুশি। -> Positive
বাক্য: আজ মন খারাপ। -> Negative

বাক্য: পরীক্ষায় ভালো ফল করেছি। ->
```

## 5. Prompt template

`prompts.py`:

```python
TUTOR_INSTRUCTIONS = """
তুমি একজন ধৈর্যশীল Python শিক্ষক।
সহজ বাংলায় ব্যাখ্যা করবে।
Beginner-friendly runnable code দেবে।
অনিশ্চিত হলে তা স্পষ্ট করবে।
"""

def build_learning_prompt(topic: str, level: str = "beginner") -> str:
    return f"""
বিষয়: {topic}
শিক্ষার্থীর স্তর: {level}

এই ক্রমে উত্তর দাও:
1. সংজ্ঞা
2. বাস্তব উদাহরণ
3. Python code
4. Code walkthrough
5. Practice task
"""
```

`prompt_template_demo.py`:

```python
from openai import OpenAI
from config import OPENAI_API_KEY, MODEL_NAME
from prompts import TUTOR_INSTRUCTIONS, build_learning_prompt

client = OpenAI(api_key=OPENAI_API_KEY)

topic = input("কোন বিষয় শিখতে চাও? ").strip()

response = client.responses.create(
    model=MODEL_NAME,
    instructions=TUTOR_INSTRUCTIONS,
    input=build_learning_prompt(topic),
)

print(response.output_text)
```

## 6. Structured output-এর ধারণা

যদি JSON দরকার হয়, prompt-এ format চাওয়া যায়; তবে prompt একা valid JSON নিশ্চিত করে না। API-এর supported structured-output feature এবং Python validation ব্যবহার করা উচিত।

JSON parse-এর ছোট example:

```python
import json

raw = '{"name": "Rahim", "skills": ["Python", "Django"], "beginner": true}'
data = json.loads(raw)

print(data["name"])
print(data["skills"])
```

Invalid JSON হলে `json.JSONDecodeError` হবে। Model output untrusted data হিসেবে validate করবে।

## 7. Prompt injection-এর প্রাথমিক ধারণা

User বা external document-এ এমন instruction থাকতে পারে যা application-এর উদ্দেশ্যের বিরোধী।

সতর্কতা:
- User input-কে trusted system instruction ধরে নিও না।
- Retrieved document-কে data হিসেবে বিবেচনা করো।
- Secret prompt-এ রাখলেই নিরাপদ হয় না।
- Tool permission Python application-এ enforce করো।
- Destructive action-এর আগে confirmation রাখো।

## 8. Homework
1. Basic ও structured prompt তুলনা করো।
2. Zero-shot এবং Few-shot example লেখো।
3. `prompts.py`-তে দুটি template যোগ করো।
4. JSON parse করে error handle করো।
5. Prompt injection-এর একটি উদাহরণ এবং প্রতিরোধের উপায় লেখো।

## Completion checklist
- [ ] `instructions` ও `input` ব্যবহার করেছি।
- [ ] Prompt comparison করেছি।
- [ ] Zero-shot ও Few-shot বুঝেছি।
- [ ] Prompt template তৈরি করেছি।
- [ ] JSON validation করেছি।
