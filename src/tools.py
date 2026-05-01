import os

from langchain_anthropic import ChatAnthropic
from tavily import TavilyClient


def get_search_client() -> TavilyClient:
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("TAVILY_API_KEY is not set")
    return TavilyClient(api_key=api_key)


def get_chat_model(model_name: str) -> ChatAnthropic:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY is not set")
    return ChatAnthropic(model=model_name, api_key=api_key, temperature=0.2)
