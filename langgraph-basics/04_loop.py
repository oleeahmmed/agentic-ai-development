import operator
import sys
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph

sys.stdout.reconfigure(encoding="utf-8")


class State(TypedDict):
    count: int
    log: Annotated[list[str], operator.add]


def work(state):
    count = state["count"] + 1
    print("কাজ চলছে — ধাপ", count)
    return {"count": count, "log": [f"ধাপ {count}"]}


def keep_going(state):
    if state["count"] < 3:
        return "again"
    return "done"


builder = StateGraph(State)
builder.add_node("work", work)
builder.add_edge(START, "work")
builder.add_conditional_edges(
    "work",
    keep_going,
    {"again": "work", "done": END},
)

graph = builder.compile()

result = graph.invoke({"count": 0, "log": []})
print("--- শেষ ফল ---")
print(result)
