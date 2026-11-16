import operator
import sys
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph

sys.stdout.reconfigure(encoding="utf-8")


class State(TypedDict):
    name: str
    greeting: str
    steps: Annotated[list[str], operator.add]


def greet(state):
    print("greet পেল:", state)
    return {"greeting": f"হ্যালো {state['name']}!", "steps": ["greet"]}


def plan(state):
    print("plan পেল:", state)
    return {"steps": ["plan"]}


builder = StateGraph(State)
builder.add_node("greet", greet)
builder.add_node("plan", plan)
builder.add_edge(START, "greet")
builder.add_edge("greet", "plan")
builder.add_edge("plan", END)

graph = builder.compile()

result = graph.invoke({"name": "মিতু", "steps": []})
print("--- শেষ ফল ---")
print(result)
