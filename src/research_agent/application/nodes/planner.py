import os
from typing import Any, Dict

from langchain_core.messages import HumanMessage, SystemMessage

from research_agent.domain.prompts import PLANNER_SYSTEM_PROMPT
from research_agent.domain.state import ResearchState
from research_agent.infrastructure.clients import get_chat_model


def planner_node(state: ResearchState) -> Dict[str, Any]:
    model_name = os.getenv("SEARCH_MODEL", "claude-haiku-4-5-20251001")
    model = get_chat_model(model_name)

    messages = [
        SystemMessage(content=PLANNER_SYSTEM_PROMPT),
        HumanMessage(content=state.get("original_query", "")),
    ]
    response = model.invoke(messages)

    lines = [line.strip() for line in response.content.splitlines() if line.strip()]
    sub_questions = [line.lstrip("0123456789.-) ") for line in lines]
    if not sub_questions:
        sub_questions = [state["original_query"]]

    return {
        "sub_questions": sub_questions,
        "iteration_count": 0,
        "search_results": [
            {
                "_reset": True,
                "results": [],
            }
        ],
    }
