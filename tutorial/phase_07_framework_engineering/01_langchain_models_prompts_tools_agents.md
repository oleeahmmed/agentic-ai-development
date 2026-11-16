# Chapter 01 — LangChain: Models, Prompts, Tools & Agents

## 1. LangChain কী এবং কেন?

LangChain হলো LLM application তৈরির framework ecosystem। এটি model provider, prompt, structured output, tools ও agent loop এক জায়গায় compose করতে সাহায্য করে।

Scratch implementation-এ আপনি নিজে লিখেছেন:

```text
prompt -> LLM API -> parse response -> choose tool
       -> execute tool -> send result -> final answer
```

LangChain এসবের কিছু অংশের reusable abstraction দেয়। তবে framework আপনার business rule, permission বা security নিজে থেকে নিশ্চিত করে না।

## 2. Installation

```bash
pip install langchain langchain-openai python-dotenv pydantic
```

`requirements.txt`-এ কাজ করা version pin করুন:

```bash
pip freeze > requirements.txt
```

## 3. Environment configuration

`.env`:

```env
OPENAI_API_KEY=your_api_key_here
```

`config.py`:

```python
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is missing")
```

API key source code-এ hardcode করবেন না।

## 4. প্রথম LangChain model call

`01_model.py`:

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

model = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0,
)

response = model.invoke([
    HumanMessage(content="AI Agent কী? বাংলায় ৩ লাইনে বোঝাও।")
])

print(response.content)
```

Run:

```bash
python 01_model.py
```

`invoke()` synchronous call। Async application-এ `ainvoke()` ব্যবহার করতে পারেন:

```python
import asyncio
from langchain_openai import ChatOpenAI

async def main():
    model = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
    response = await model.ainvoke("Explain LangChain briefly.")
    print(response.content)

asyncio.run(main())
```

## 5. PromptTemplate

Prompt-কে code থেকে আলাদা ও reusable রাখা যায়।

`02_prompt.py`:

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

model = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "তুমি একজন experienced Python teacher. সহজ বাংলায় শেখাবে।"),
    ("human", "বিষয়: {topic}\nশিক্ষার্থীর level: {level}\nএকটি practical example দাও।"),
])

chain = prompt | model

result = chain.invoke({
    "topic": "Python function",
    "level": "beginner",
})

print(result.content)
```

এখানে `|` হলো Runnable composition: prompt-এর output model-এর input হয়।

## 6. Structured output with Pydantic

Agent-এর output plain text হলে parse করা কঠিন। Structured output দিলে application নির্দিষ্ট schema পায়।

`03_structured_output.py`:

```python
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI


class TaskPlan(BaseModel):
    goal: str = Field(description="User-এর মূল লক্ষ্য")
    steps: list[str] = Field(description="কাজের ordered steps")
    needs_approval: bool = Field(description="মানুষের approval দরকার কি না")


model = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0,
)

structured_model = model.with_structured_output(TaskPlan)

plan = structured_model.invoke(
    "একটি Django project-এ login API তৈরি করার পরিকল্পনা দাও।"
)

print(plan)
print(plan.model_dump())
```

Structured output মানেই plan নিরাপদ বা সঠিক নয়। Application-এ schema validation, business rule ও permission check করতে হবে।

## 7. Tool তৈরি করা

Tool হলো model/application-এর জন্য callable capability। Tool-এর docstring ও schema model-কে tool-এর কাজ বুঝতে সাহায্য করে।

`04_tools.py`:

```python
from langchain_core.tools import tool


@tool
def add_numbers(a: int, b: int) -> int:
    """দুটি integer যোগ করে ফলাফল ফেরত দেয়।"""
    return a + b


@tool
def word_count(text: str) -> int:
    """একটি text-এ whitespace অনুযায়ী word count করে।"""
    return len(text.split())


if __name__ == "__main__":
    print(add_numbers.invoke({"a": 15, "b": 25}))
    print(word_count.invoke({"text": "AI Agent Engineering"}))
```

খেয়াল করুন:
- Tool-এর description স্পষ্ট রাখুন।
- Argument type/schema নির্দিষ্ট করুন।
- Tool-এর ভিতরেও validation করুন।
- External side effect-এ permission ও approval enforce করুন।

## 8. Model-কে tools bind করা

`05_bind_tools.py`:

```python
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool


@tool
def calculate_total(price: float, quantity: int) -> float:
    """একটি পণ্যের মোট দাম হিসাব করে।"""
    if price < 0 or quantity < 0:
        raise ValueError("price এবং quantity negative হতে পারবে না")
    return price * quantity


model = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
model_with_tools = model.bind_tools([calculate_total])

response = model_with_tools.invoke(
    "প্রতি পিস ২৫০ টাকা, ৪টি কিনলে মোট কত?"
)

print("Text:", response.content)
print("Tool calls:", response.tool_calls)
```

এই ধাপে model tool call প্রস্তাব করতে পারে। Tool bind করলেই সব ক্ষেত্রে tool execute হয়েছে ধরে নেবেন না। `response.tool_calls` inspect করতে হবে, তারপর application বা agent runtime execute করবে।

## 9. Tool execution manually

`06_manual_tool_execution.py`:

```python
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool


@tool
def add_numbers(a: int, b: int) -> int:
    """দুটি সংখ্যা যোগ করে।"""
    return a + b


tools = [add_numbers]
tool_map = {tool.name: tool for tool in tools}

model = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
model_with_tools = model.bind_tools(tools)

messages = [
    ("system", "প্রয়োজনে calculator tool ব্যবহার করো।"),
    ("human", "১৯৫ + ২৭৫ কত?"),
]

ai_message = model_with_tools.invoke(messages)
messages.append(ai_message)

for tool_call in ai_message.tool_calls:
    name = tool_call["name"]
    args = tool_call["args"]

    if name not in tool_map:
        raise ValueError("Unknown tool")

    result = tool_map[name].invoke(args)

    messages.append({
        "role": "tool",
        "tool_call_id": tool_call["id"],
        "content": str(result),
    })

final_response = model.invoke(messages)
print(final_response.content)
```

এই manual pattern শিক্ষার জন্য। Production-এ tool-call protocol, error handling, tool result message format এবং provider-specific behavior framework-এর agent/tool node দিয়ে manage করাই ভালো।

## 10. Agent abstraction

LangChain ecosystem-এ agent creation API release অনুযায়ী পরিবর্তিত হয়েছে। নতুন project-এ LangChain-এর current agent documentation অনুসরণ করুন; stateful, resumable workflow দরকার হলে পরের chapter-এর LangGraph ব্যবহার করুন।

Conceptual agent loop:

```text
User request
   |
Model decides
   |
   +-- final answer -> return
   |
   +-- tool call -> validate -> authorize -> execute
                         |
                         v
                    tool result
                         |
                         +----> model decides again
```

Agent loop-এর safety:
- maximum steps;
- tool allowlist;
- validated arguments;
- authenticated user context;
- write-action approval;
- timeout and retry budget;
- audit logs.

## 11. কখন LangChain ব্যবহার করবেন?

ভালো fit:
- একাধিক model/provider abstraction দরকার;
- prompt + model + parser composition;
- tool schema ও integration manage করতে চান;
- দ্রুত LLM application prototype করতে চান।

শুধু plain Python যথেষ্ট হতে পারে:
- একটিমাত্র API call;
- simple deterministic business logic;
- framework abstraction complexity বাড়িয়ে দেবে।

## 12. Homework

1. `ChatPromptTemplate` দিয়ে Python tutor prompt তৈরি করুন।
2. `TaskPlan`-এ `estimated_hours` যোগ করুন।
3. `search_projects` নামে read-only tool তৈরি করুন।
4. Tool call-এর আগে allowlist check করুন।
5. `bind_tools()` response-এর tool call ও ordinary text response আলাদা করে handle করুন।

**Chapter takeaway:** LangChain আপনার LLM application compose করতে সাহায্য করে; agent-এর নিরাপত্তা ও business logic আপনার দায়িত্ব।
