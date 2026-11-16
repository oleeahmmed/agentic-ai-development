import sys
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

sys.stdout.reconfigure(encoding="utf-8")


class State(TypedDict):
    question: str
    need_tool: bool
    answer: str


def decide(state):
    need_tool = "আবহাওয়া" in state["question"]
    print("প্রশ্ন:", state["question"])
    print("টুল লাগবে?", need_tool)
    return {"need_tool": need_tool}


def router(state):
    return "yes" if state["need_tool"] else "no"


def use_tool(state):
    return {"answer": "ঢাকায় এখন ২৫°C (টুল থেকে পাওয়া)।"}


def answer(state):
    return {"answer": "এটি সাধারণ প্রশ্ন, টুল লাগে না।"}


builder = StateGraph(State)
builder.add_node("decide", decide)
builder.add_node("use_tool", use_tool)
builder.add_node("answer", answer)
builder.add_edge(START, "decide")
builder.add_conditional_edges(
    "decide",
    router,
    {"yes": "use_tool", "no": "answer"},
)
builder.add_edge("use_tool", END)
builder.add_edge("answer", END)

graph = builder.compile()

print("--- প্রশ্ন ১ ---")
print(graph.invoke({"question": "আজ ঢাকার আবহাওয়া কেমন?"}))

print("\n--- প্রশ্ন ২ ---")
print(graph.invoke({"question": "তুমি কে?"}))
