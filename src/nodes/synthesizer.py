import os

from langchain_core.messages import HumanMessage, SystemMessage

from src.prompts import SYNTHESIZER_SYSTEM_PROMPT
from typing import Any, Dict

from src.state import ResearchState
from src.tools import get_chat_model


def synthesizer_node(state: ResearchState) -> Dict[str, Any]:
    model_name = os.getenv("SYNTHESIS_MODEL", "claude-sonnet-4-5")
    model = get_chat_model(model_name)

    payload = {
        "query": state.get("original_query"),
        "sub_questions": state.get("sub_questions", []),
        "search_results": state.get("search_results", []),
    }

    messages = [
        SystemMessage(content=SYNTHESIZER_SYSTEM_PROMPT),
        HumanMessage(content=str(payload)),
    ]
    response = model.invoke(messages)

    return {
        "final_report": response.content,
    }
