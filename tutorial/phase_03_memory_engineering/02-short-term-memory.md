# Chapter 02 — Short-term Memory

**সময়:** ৪ ঘণ্টা  
**লক্ষ্য:** Conversation history ধরে রেখে একাধিক turn-এ AI Assistant-কে context দেওয়া।

## 1. সমস্যা

একটি stateless request:

```text
User: আমার নাম রাহিম।
Assistant: পরিচিত হয়ে ভালো লাগল।

User: আমার নাম কী?
Assistant: আমি জানি না।
```

দ্বিতীয় request-এ প্রথম message না পাঠালে model-এর কাছে আগের তথ্য থাকে না।

সমাধান: application conversation history ধরে রাখবে এবং প্রতিটি model call-এ প্রাসঙ্গিক history পাঠাবে।

## 2. Message structure

OpenAI Responses API-তে সাধারণভাবে input message-এ `role` ও `content` থাকে। আমরা সহজভাবে local Python list রাখব:

```python
history = [
    {"role": "user", "content": "আমার নাম রাহিম।"},
    {"role": "assistant", "content": "পরিচিত হয়ে ভালো লাগল।"},
]
```

## 3. Practical — short-term memory chatbot

`short_term_memory.py` তৈরি করো:

```bash
cd ~/rahim_ai
nano short_term_memory.py
```

সম্পূর্ণ code:

```python
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is missing from .env")

client = OpenAI(api_key=api_key)

# এই list শুধু program চলা পর্যন্ত থাকবে।
conversation_history = []

SYSTEM_INSTRUCTIONS = (
    "You are a helpful assistant. Reply in simple Bengali. "
    "Use the conversation history when answering."
)


def ask_ai(user_message: str) -> str:
    conversation_history.append({
        "role": "user",
        "content": user_message,
    })

    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions=SYSTEM_INSTRUCTIONS,
        input=conversation_history,
    )

    answer = response.output_text

    conversation_history.append({
        "role": "assistant",
        "content": answer,
    })

    return answer


def main():
    print("Short-term Memory Assistant")
    print("Type 'exit' to quit. Type 'show' to inspect history.")

    while True:
        message = input("\nYou: ").strip()

        if message.lower() in {"exit", "quit"}:
            break

        if message.lower() == "show":
            for item in conversation_history:
                print(item)
            continue

        if not message:
            continue

        try:
            print("AI:", ask_ai(message))
        except Exception as error:
            print("Error:", error)


if __name__ == "__main__":
    main()
```

চালাও:

```bash
python3 short_term_memory.py
```

পরীক্ষা:

```text
You: আমার নাম রাহিম।
You: আমার নাম কী?
```

দ্বিতীয় প্রশ্নে assistant আগের message-এর তথ্য ব্যবহার করতে পারবে।

## 4. কেন history-তে assistant message-ও রাখতে হয়?

শুধু user message রাখলে conversation-এর assistant response বাদ পড়ে যায়। ফলে আগের প্রশ্ন-উত্তরের পূর্ণ flow থাকে না। তাই সাধারণত user ও assistant উভয়ের message রাখা হয়।

## 5. Memory inspect

`show` লিখলে local history print হবে। এতে বোঝা যাবে Python list-টাই বর্তমান conversation state ধরে রেখেছে।

## 6. History সীমিত করা

Conversation দীর্ঘ হলে প্রতিটি message বারবার পাঠানো ব্যয়বহুল হতে পারে। শেখার জন্য recent message window ব্যবহার করো।

`ask_ai()`-এর আগে:

```python
MAX_MESSAGES = 12
```

API call-এ:

```python
input=conversation_history[-MAX_MESSAGES:],
```

এটি শুধু শেষ ১২টি message পাঠাবে। মনে রাখবে, এতে পুরোনো গুরুত্বপূর্ণ তথ্য বাদ পড়ে যেতে পারে। পরে summary বা long-term memory দিয়ে সেটি সামলাব।

## 7. Error handling-এর ছোট উন্নতি

API call ব্যর্থ হলে user message history-তে থেকে যেতে পারে। Production code-এ failed turn rollback, retry policy, request ID logging এবং rate-limit handling যোগ করতে হবে।

## 8. গুরুত্বপূর্ণ সীমাবদ্ধতা

এই memory:
- Program বন্ধ করলে হারিয়ে যাবে
- অন্য user-এর সঙ্গে share করা যাবে না
- কোনো session identifier নেই
- history size সীমিত করা দরকার
- sensitive তথ্য অকারণে রাখা উচিত নয়

## Homework

1. `show` দিয়ে history inspect করো।
2. `MAX_MESSAGES` ৪ করে পরীক্ষা করো।
3. Program বন্ধ করে আবার চালিয়ে আগের তথ্য মনে থাকে কি না দেখো।
4. Short-term memory-এর অন্তত চারটি limitation লেখো।

## Completion checklist

- [ ] Python list-এ conversation history রেখেছি
- [ ] User ও assistant message সংরক্ষণ করেছি
- [ ] History model call-এ পাঠিয়েছি
- [ ] Recent history limit করেছি
- [ ] Program restart করলে history হারায়—এটি বুঝেছি
