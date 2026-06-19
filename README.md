# LangGraph Competitive Intelligence & Campaign Strategy Agent

This project implements a **Competitive Intelligence & Campaign Strategy Agent** for marketing use cases using **LangGraph** and **LangChain**. It goes beyond a generic chatbot by using **iterative research loops**, **persistent state**, and **conditional routing** to build higher‑quality strategic outputs.

## What Makes This Different

- **Persistent State**: Accumulates results across search iterations for richer synthesis.
- **Iterative Refinement**: Loops until coverage is strong (or a guardrail is reached).
- **Conditional Routing**: Evaluation node decides whether to continue searching.
- **Human‑in‑the‑Loop (HITL)**: Optional approval before final synthesis.

## Architecture Overview

```
Query
  │
  ▼
Planner → Searcher → Evaluator ─┐
  ▲                            │
  └──────────── loop ──────────┘
              │
              ▼
         Synthesizer → Final Report
```

## Quick Start

1. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    # or install the package in editable mode
    pip install -e .
    ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   ```
   Fill in required keys.

3. **Run example**
   ```bash
   python examples/marketing_usecase.py
   ```

> Note: the example uses an interrupt before synthesis (HITL). To resume after reviewing results, invoke the graph with the same thread_id and a flag to proceed.

## Repo Layout

```
codebase/
├── README.md
├── pyproject.toml
├── requirements.txt
├── .env.example
├── src/
│   └── research_agent/
│       ├── __init__.py
│       ├── application/
│       │   ├── graph.py
│       │   └── nodes/
│       │       ├── planner.py
│       │       ├── searcher.py
│       │       ├── evaluator.py
│       │       ├── synthesizer.py
│       │       └── hitl.py
│       ├── domain/
│       │   ├── prompts.py
│       │   └── state.py
│       └── infrastructure/
│           └── clients.py
├── examples/
│   └── marketing_usecase.py
├── demo/
│   └── app.py
├── docs/
│   └── ARCHITECTURE.md
└── tests/
    └── test_graph.py
```

The `src/research_agent` package separates orchestration (`application`), business state and prompts (`domain`), and external adapters (`infrastructure`) while preserving the existing LangGraph workflow and CLI/demo entrypoints.

## Roadmap Alignment

This repository implements **Phase 0–3** of the technical roadmap:

- **Phase 0**: Repo scaffolding
- **Phase 1**: State definition
- **Phase 2**: Node implementations
- **Phase 3**: Graph assembly

Phase 4 (demo assets) and Phase 5 (Streamlit UI) can be added later.
