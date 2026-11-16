# Chapter 02 — LangGraph: Stateful Workflow, Nodes, Edges & Persistence

## 1. LangGraph কেন?

সাধারণ chain সাধারণত একদিকে data flow করে। Agent workflow-তে branching, loop, retry, approval, state update ও pause/resume দরকার হয়। LangGraph graph-based orchestration দেয়।

```text
START -> classify -> plan -> execute -> review
                         ^          |
                         |----------|
                              |
                             END
```

LangGraph-এর মূল building blocks:
- **State:** পুরো workflow-এর shared data।
- **Node:** একটি Python function, state নেয় এবং update ফেরত দেয়।
- **Edge:** কোন node-এর পরে কোন node চলবে।
- **Conditional edge:** state দেখে route নির্বাচন।
- **Checkpoint:** execution state persist করা।
- **Interrupt:** human input/approval-এর জন্য pause করা।

## 2. Installation

```bash
pip install langgraph langchain langchain-openai python-dotenv
```

## 3. প্রথম graph

`01_hello_graph.py`:

```python
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    message: str


def greet(state: State):
    return {"message": f"Hello, {state['message']}!"}


builder = StateGraph(State)
builder.add_node("greet", greet)
builder.add_edge(START, "greet")
builder.add_edge("greet", END)

graph = builder.compile()

result = graph.invoke({"message": "Agent Engineer"})
print(result)
```

Run:

```bash
python 01_hello_graph.py
```

## 4. State কীভাবে কাজ করে?

State হলো graph-এর চলমান shared context। Node সাধারণত সম্পূর্ণ state replace না করে যে field update করে তা return করে।

`02_multi_node_graph.py`:

```python
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    topic: str
    outline: str
    lesson: str


def create_outline(state: State):
    return {
        "outline": f"{state['topic']}: definition, example, practice"
    }


def write_lesson(state: State):
    return {
        "lesson": f"Lesson based on: {state['outline']}"
    }


builder = StateGraph(State)
builder.add_node("outline", create_outline)
builder.add_node("lesson", write_lesson)

builder.add_edge(START, "outline")
builder.add_edge("outline", "lesson")
builder.add_edge("lesson", END)

graph = builder.compile()

result = graph.invoke({
    "topic": "Python function",
    "outline": "",
    "lesson": "",
})
print(result)
```

## 5. Conditional edges

এবার state-এর value অনুযায়ী route বেছে নেব।

`03_conditional_graph.py`:

```python
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    request: str
    category: str
    answer: str


def classify(state: State):
    text = state["request"].lower()
    if "bug" in text or "error" in text:
        category = "debug"
    elif "plan" in text:
        category = "planning"
    else:
        category = "general"
    return {"category": category}


def debug_node(state: State):
    return {"answer": "Debug workflow selected."}


def planning_node(state: State):
    return {"answer": "Planning workflow selected."}


def general_node(state: State):
    return {"answer": "General assistant workflow selected."}


def route(state: State):
    return state["category"]


builder = StateGraph(State)
builder.add_node("classify", classify)
builder.add_node("debug", debug_node)
builder.add_node("planning", planning_node)
builder.add_node("general", general_node)

builder.add_edge(START, "classify")
builder.add_conditional_edges(
    "classify",
    route,
    {
        "debug": "debug",
        "planning": "planning",
        "general": "general",
    },
)
builder.add_edge("debug", END)
builder.add_edge("planning", END)
builder.add_edge("general", END)

graph = builder.compile()
print(graph.invoke({
    "request": "আমার Django bug fix করার plan দাও",
    "category": "",
    "answer": "",
}))
```

## 6. Loop এবং termination condition

Agent workflow-তে review fail হলে আবার execute করা যেতে পারে। কিন্তু loop-এর stop condition বাধ্যতামূলক।

`04_review_loop.py`:

```python
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    attempts: int
    max_attempts: int
    draft: str
    approved: bool


def create_draft(state: State):
    return {
        "attempts": state["attempts"] + 1,
        "draft": f"Draft version {state['attempts'] + 1}",
    }


def review(state: State):
    # Demo: দ্বিতীয় draft-এ approve
    return {"approved": state["attempts"] >= 2}


def route_after_review(state: State):
    if state["approved"]:
        return "done"
    if state["attempts"] >= state["max_attempts"]:
        return "stop"
    return "revise"


builder = StateGraph(State)
builder.add_node("draft", create_draft)
builder.add_node("review", review)

builder.add_edge(START, "draft")
builder.add_edge("draft", "review")
builder.add_conditional_edges(
    "review",
    route_after_review,
    {
        "done": END,
        "stop": END,
        "revise": "draft",
    },
)

graph = builder.compile()
print(graph.invoke({
    "attempts": 0,
    "max_attempts": 3,
    "draft": "",
    "approved": False,
}))
```

## 7. ToolNode এবং model tool calling

LangGraph-এ `ToolNode` tool execution node হিসেবে ব্যবহৃত হয়। Model tool call তৈরি করে, ToolNode তা execute করে এবং tools result message state-এ যোগ হয়।

`05_tool_graph.py`:

```python
from typing import Annotated
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition


@tool
def add_numbers(a: int, b: int) -> int:
    """দুটি integer যোগ করে।"""
    return a + b


tools = [add_numbers]
model = ChatOpenAI(model="gpt-4.1-mini", temperature=0).bind_tools(tools)


class State(TypedDict):
    messages: Annotated[list, add_messages]


def assistant(state: State):
    response = model.invoke(state["messages"])
    return {"messages": [response]}


builder = StateGraph(State)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")

graph = builder.compile()

result = graph.invoke({
    "messages": [{"role": "user", "content": "৪৫ + ৫৫ কত?"}]
})

for message in result["messages"]:
    print(message.type, message.content)
```

**Security note:** এই minimal example-এ permission/approval layer দেখানো হয়নি। Real project-এ `ToolNode`-এ tool দেওয়ার আগেই allowlist, authenticated user context, argument validation ও policy enforce করুন। Sensitive write tool সরাসরি unrestricted `ToolNode`-এ expose করবেন না।

## 8. Persistence / checkpointing

Checkpointing workflow state save করে, যাতে conversation/run resume করা যায়। In-memory saver development-এর জন্য; process restart হলে data হারাতে পারে।

```python
from langgraph.checkpoint.memory import InMemorySaver

# graph = builder.compile(checkpointer=InMemorySaver())
# config = {"configurable": {"thread_id": "conversation-001"}}
# first = graph.invoke(initial_state, config=config)
# later = graph.invoke(next_input, config=config)
```

Production-এ supported persistent checkpointer (যেমন PostgreSQL integration) ব্যবহার করুন এবং official LangGraph docs অনুযায়ী package/setup configure করুন। `thread_id` user/tenant access control-এর বিকল্প নয়; প্রতিবার authenticated owner verify করুন।

## 9. Human-in-the-loop / interrupt

High-impact action-এর আগে graph pause করে human approval নেওয়া যায়। LangGraph-এর `interrupt` ও resume pattern ব্যবহার করতে পারেন। Checkpointer এবং stable `thread_id` প্রয়োজন।

Conceptual flow:

```text
plan action -> validate -> interrupt("Approve delete?")
                         |
                    human decision
                    /          \
                 approve       reject
                   |             |
                execute        stop
```

Approval decision server-side authenticated user-এর কাছ থেকে নিন। Model-generated “approved=true” বিশ্বাস করবেন না।

## 10. Homework

1. `classify -> plan -> execute -> review` graph বানান।
2. `max_attempts` দিয়ে loop bound করুন।
3. একটি read-only tool `ToolNode`-এ যোগ করুন।
4. `thread_id` দিয়ে conversation resume করুন।
5. একটি destructive action-এর আগে human interrupt design করুন।
6. Graph-এর প্রতিটি node-এর unit test লিখুন।

**Chapter takeaway:** LangGraph agent-কে stateful, branching, resumable workflow হিসেবে সাজাতে সাহায্য করে।
