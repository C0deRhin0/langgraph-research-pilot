import os

from langchain_core.messages import HumanMessage, SystemMessage

from src.prompts import EVALUATOR_SYSTEM_PROMPT
from typing import Any, Dict

from src.state import ResearchState
from src.tools import get_chat_model


def evaluator_node(state: ResearchState) -> Dict[str, Any]:
    model_name = os.getenv("SEARCH_MODEL", "claude-haiku-4-5-20251001")
    model = get_chat_model(model_name)

    summary = {
        "query": state.get("original_query"),
        "iterations": state.get("iteration_count", 0),
        "results_count": len(state.get("search_results", [])),
    }

    messages = [
        SystemMessage(content=EVALUATOR_SYSTEM_PROMPT),
        HumanMessage(content=str(summary)),
    ]
    response = model.invoke(messages)

    try:
        score = float(str(response.content).strip())
    except ValueError:
        score = 0.5

    sub_questions = state.get("sub_questions", [])
    should_continue = score < 0.75 and state.get("iteration_count", 0) < len(sub_questions)

    return {
        "evaluation_score": score,
        "should_continue": should_continue,
    }
