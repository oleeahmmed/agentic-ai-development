import operator
import sys
import uuid
from typing import Annotated, TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command

import nodes

sys.stdout.reconfigure(encoding="utf-8")


class ResearchState(TypedDict):
    question: str
    queries: list[str]
    search_log: Annotated[list[str], operator.add]
    sources: list[dict]
    summary: str
    enough: bool
    gaps: str
    rounds: int
    approved: bool
    report_path: str


def next_step(state):
    if state["enough"] or state["rounds"] >= 3:
        return "approve"

    return "revise"


def after_approval(state):
    if state["approved"] and state["sources"]:
        return "write_report"

    return END


builder = StateGraph(ResearchState)
builder.add_node("plan", nodes.plan_node)
builder.add_node("search", nodes.search_node)
builder.add_node("summarize", nodes.summarize_node)
builder.add_node("critique", nodes.critique_node)
builder.add_node("revise", nodes.revise_node)
builder.add_node("approve", nodes.approve_node)
builder.add_node("write_report", nodes.write_node)

builder.add_edge(START, "plan")
builder.add_edge("plan", "search")
builder.add_edge("search", "summarize")
builder.add_edge("summarize", "critique")
builder.add_conditional_edges("critique", next_step)
builder.add_edge("revise", "search")
builder.add_conditional_edges("approve", after_approval)
builder.add_edge("write_report", END)

graph = builder.compile(checkpointer=MemorySaver())


def show(chunk):
    for name, update in chunk.items():
        if name == "__interrupt__":
            print("  [থামা]", update[0].value)
            continue

        print("  [ধাপ]", name)

        if name == "search":
            print("       উৎস:", len(update.get("sources", [])))
        if name == "critique":
            print("       যথেষ্ট?", update.get("enough"))
        if name == "revise":
            print("       নতুন সার্চ:", update.get("queries"))
        if name == "write_report":
            print("       সেভ:", update.get("report_path"))


def research(question):
    config = {
        "configurable": {"thread_id": "run-" + uuid.uuid4().hex[:8]},
        "recursion_limit": 25,
    }
    state = {
        "question": question,
        "queries": [],
        "search_log": [],
        "sources": [],
        "summary": "",
        "enough": False,
        "gaps": "",
        "rounds": 0,
        "approved": False,
        "report_path": "",
    }

    for chunk in graph.stream(state, config=config, stream_mode="updates"):
        show(chunk)

    if graph.get_state(config).next:
        answer = input("\nরিপোর্ট লেখা হবে? (y/n): ").strip()

        for chunk in graph.stream(Command(resume=answer), config=config, stream_mode="updates"):
            show(chunk)

    final = graph.get_state(config).values

    if final.get("report_path"):
        print("\nরিপোর্ট সেভ হয়েছে:", final["report_path"])
    else:
        print("\nরিপোর্ট লেখা হয়নি।")


print("Research Buddy — প্রশ্ন লিখুন, উৎসসহ রিপোর্ট পাবেন। exit = বন্ধ")


def main():
    while True:
        question = input("\nপ্রশ্ন: ").strip()

        if question == "exit":
            break

        if not question:
            continue

        try:
            research(question)
        except Exception as error:
            print("সমস্যা:", error)


if __name__ == "__main__":
    main()
