from typing import Any, Dict

from src.state import ResearchState
from src.tools import get_search_client


def searcher_node(state: ResearchState) -> Dict[str, Any]:
    client = get_search_client()

    sub_questions = state.get("sub_questions", [])
    iteration = state.get("iteration_count", 0)

    if iteration >= len(sub_questions):
        return {
            "iteration_count": iteration + 1,
        }

    query = sub_questions[iteration]
    results = client.search(query=query, max_results=5)

    return {
        "search_results": [
            {
                "query": query,
                "results": results.get("results", []),
            }
        ],
        "iteration_count": iteration + 1,
    }
