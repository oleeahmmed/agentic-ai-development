import sys
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

sys.stdout.reconfigure(encoding="utf-8")


class State(TypedDict):
    reply: str


def hello(state):
    print("নোড পেল:", state)
    return {"reply": "হ্যালো, আমি মিতু।"}


builder = StateGraph(State)
builder.add_node("hello", hello)
builder.add_edge(START, "hello")
builder.add_edge("hello", END)

graph = builder.compile()

print("--- গ্রাফ শুরু ---")
result = graph.invoke({})
print("--- গ্রাফ শেষ ---")
print(result)
