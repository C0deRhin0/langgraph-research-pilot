# Architecture

## Pattern

This repository is a Python LangGraph research-agent package with example and Streamlit entrypoints. It uses a package-oriented `src/` layout rather than a web-framework route layout.

## Boundaries

- `src/research_agent/application/` contains graph assembly and executable nodes.
- `src/research_agent/domain/` contains the research state contract and prompt definitions.
- `src/research_agent/infrastructure/` contains adapters for external services such as Anthropic and Tavily.
- `examples/` contains command-line usage examples.
- `demo/` contains the Streamlit UI.
- `tests/` contains repository-level automated tests.

## Runtime Paths

- LangGraph checkpoint data defaults to `research_memory.db`; bundled examples and the Streamlit demo resolve it under the repository root.
- Example reports are written to `output/report.md` under the repository root.
- Secrets are loaded from environment variables; `.env` is intentionally ignored and `.env.example` is the only checked-in template.
