from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, StateGraph

from src.nodes.evaluator import evaluator_node
from src.nodes.planner import planner_node
from src.nodes.searcher import searcher_node
from src.nodes.synthesizer import synthesizer_node
from src.state import ResearchState


def should_continue(state: ResearchState) -> str:
    if state.get("should_continue") and state.get("iteration_count", 0) < 4:
        return "searcher"
    return "synthesizer"


def build_graph():
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

    checkpointer = SqliteSaver.from_conn_string("research_memory.db")
    return builder.compile(checkpointer=checkpointer, interrupt_before=["synthesizer"])
