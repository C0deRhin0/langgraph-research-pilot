__all__ = ["get_chat_model", "get_search_client"]


def __getattr__(name: str):
    if name in __all__:
        from research_agent.infrastructure.clients import get_chat_model, get_search_client

        return {
            "get_chat_model": get_chat_model,
            "get_search_client": get_search_client,
        }[name]
    raise AttributeError(f"module 'research_agent.infrastructure' has no attribute {name!r}")
