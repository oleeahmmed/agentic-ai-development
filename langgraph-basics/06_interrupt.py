import sys
from typing import TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

sys.stdout.reconfigure(encoding="utf-8")


class State(TypedDict):
    approved: bool
    result: str


def ask(state):
    answer = interrupt("রিপোর্ট লেখা হবে? (y/n)")
    print("ইউজার বলল:", answer)
    return {"approved": answer == "y"}


def finish(state):
    if state["approved"]:
        return {"result": "রিপোর্ট লেখা হয়েছে।"}
    return {"result": "রিপোর্ট লেখা হয়নি।"}


builder = StateGraph(State)
builder.add_node("ask", ask)
builder.add_node("finish", finish)
builder.add_edge(START, "ask")
builder.add_edge("ask", "finish")
builder.add_edge("finish", END)

graph = builder.compile(checkpointer=MemorySaver())

config = {"configurable": {"thread_id": "রিপোর্ট"}}

graph.invoke({"approved": False}, config)
print("গ্রাফ থেমেছে। পরের নোড:", graph.get_state(config).next)

result = graph.invoke(Command(resume="y"), config)
print("চূড়ান্ত ফল:", result)
