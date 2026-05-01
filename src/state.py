from typing import Annotated, List, TypedDict

from langgraph.graph.message import add_messages


def merge_search_results(existing: List[dict] | None, incoming: List[dict]) -> List[dict]:
    existing = existing or []
    if not incoming:
        return existing
    if incoming and incoming[0].get("_reset"):
        return incoming[1:]
    return existing + incoming


class ResearchState(TypedDict):
    original_query: str
    sub_questions: List[str]
    search_results: Annotated[List[dict], merge_search_results]
    iteration_count: int
    evaluation_score: float
    should_continue: bool
    final_report: str
    messages: Annotated[list, add_messages]
