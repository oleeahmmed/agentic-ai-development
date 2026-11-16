# Chapter 03 — Native Tool Calling: প্রথম Tool

এখন OpenAI API-কে tool-এর description দেব। Model প্রয়োজন মনে করলে function call request দেবে। Python সেটি execute করে result ফেরত পাঠাবে।

## 1. Setup

```bash
pip install --upgrade openai python-dotenv
```

`.env`:
```env
OPENAI_API_KEY=your_api_key_here
```

`config.py`:

```python
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("OPENAI_API_KEY পাওয়া যায়নি। .env পরীক্ষা করো।")

client = OpenAI(api_key=api_key)
```

## 2. Tool definition ও প্রথম request

`main.py`:

```python
import json
from config import client
from tools.registry import execute_tool

tools = [
    {
        "type": "function",
        "name": "add_numbers",
        "description": "দুটি সংখ্যার যোগফল বের করে।",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "প্রথম সংখ্যা"},
                "b": {"type": "number", "description": "দ্বিতীয় সংখ্যা"},
            },
            "required": ["a", "b"],
            "additionalProperties": False,
        },
        "strict": True,
    }
]

def main():
    response = client.responses.create(
        model="gpt-4.1-mini",
        input="৪৫ এবং ৫৫ যোগ করে দাও।",
        tools=tools,
    )

    found_call = False

    for item in response.output:
        if item.type == "function_call":
            found_call = True
            arguments = json.loads(item.arguments)
            result = execute_tool(item.name, arguments)

            print("Tool:", item.name)
            print("Arguments:", arguments)
            print("Python result:", result)

    if not found_call:
        print(response.output_text)

if __name__ == "__main__":
    main()
```

## 3. কী ঘটল?
1. Python tool schema model-কে পাঠাল।
2. User হিসাব করতে বলল।
3. Model `function_call` তৈরি করল।
4. Python arguments parse করল।
5. Registry থেকে function execute হলো।

এখনো tool result model-কে ফেরত পাঠানো হয়নি; Chapter 05-এ complete cycle হবে।

## 4. Definition বনাম implementation
- `tools` list model-কে জানায় কোন tool আছে ও কী input লাগে।
- `TOOL_REGISTRY` বাস্তবে কোন Python function চলবে তা নির্ধারণ করে।
- দুই জায়গার নাম ও schema সামঞ্জস্যপূর্ণ রাখতে হবে।

Model সবসময় tool call করবে না। সে সরাসরি উত্তরও দিতে পারে, তাই `function_call` না থাকলে `output_text` দেখাতে হবে।

## 5. Exercise
- User message বদলে “১২৩ এবং ৭৭ যোগ করো” দাও।
- Tool call ও Python result আলাদা করে print করো।
- `strict` ও `additionalProperties`-এর উদ্দেশ্য বোঝার চেষ্টা করো।

**নোট:** SDK/API version অনুযায়ী response item-এর details পরিবর্তিত হতে পারে। Error হলে installed SDK version ও বর্তমান API documentation মিলিয়ে দেখবে।
