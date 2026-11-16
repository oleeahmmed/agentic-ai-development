import operator
import sys
from typing import Annotated, TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

sys.stdout.reconfigure(encoding="utf-8")


class State(TypedDict):
    name: str
    notes: Annotated[list[str], operator.add]


def note(state):
    return {"notes": [f"{state['name']} এসেছে"]}


builder = StateGraph(State)
builder.add_node("note", note)
builder.add_edge(START, "note")
builder.add_edge("note", END)

graph = builder.compile(checkpointer=MemorySaver())

config = {"configurable": {"thread_id": "মিতু"}}

graph.invoke({"name": "মিতু", "notes": []}, config)
print("প্রথমবার:", graph.get_state(config).values)

graph.invoke({}, config)
print("দ্বিতীয়বার:", graph.get_state(config).values)
