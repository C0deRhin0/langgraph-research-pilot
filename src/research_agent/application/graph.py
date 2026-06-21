import sqlite3
from pathlib import Path
from typing import Union

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, StateGraph

from research_agent.application.nodes.evaluator import evaluator_node
from research_agent.application.nodes.planner import planner_node
from research_agent.application.nodes.searcher import searcher_node
from research_agent.application.nodes.synthesizer import synthesizer_node
from research_agent.domain.state import ResearchState


def should_continue(state: ResearchState) -> str:
    if state.get("should_continue") and state.get("iteration_count", 0) < 4:
        return "searcher"
    return "synthesizer"


def build_graph(checkpoint_path: Union[str, Path] = "research_memory.db"):
    builder = StateGraph(ResearchState)

    builder.add_node("planner", planner_node)
    builder.add_node("searcher", searcher_node)
    builder.add_node("evaluator", evaluator_node)
    builder.add_node("synthesizer", synthesizer_node)

    builder.set_entry_point("planner")
    builder.add_edge("planner", "searcher")
    builder.add_edge("searcher", "evaluator")
    builder.add_conditional_edges("evaluator", should_continue)
    builder.add_edge("synthesizer", END)

    connection = sqlite3.connect(str(checkpoint_path), check_same_thread=False)
    checkpointer = SqliteSaver(connection)
    return builder.compile(checkpointer=checkpointer, interrupt_before=["synthesizer"])
