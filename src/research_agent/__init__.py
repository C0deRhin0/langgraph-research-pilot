"""LangGraph Competitive Intelligence Agent package."""
from research_agent.domain.state import ResearchState

__all__ = ["ResearchState", "build_graph"]


def __getattr__(name: str):
    if name == "build_graph":
        from research_agent.application.graph import build_graph

        return build_graph
    raise AttributeError(f"module 'research_agent' has no attribute {name!r}")
