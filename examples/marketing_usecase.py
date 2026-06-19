import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from dotenv import load_dotenv

from research_agent import build_graph


def main():
    load_dotenv(PROJECT_ROOT / ".env")

    graph = build_graph(PROJECT_ROOT / "research_memory.db")
    thread_id = "tedx-demo-thread"
    query = "Competitive landscape for SEA cybersecurity compliance SaaS"

    initial_state = {
        "original_query": query,
        "sub_questions": [],
        "search_results": [],
        "iteration_count": 0,
        "evaluation_score": 0.0,
        "should_continue": True,
        "final_report": "",
        "messages": [],
    }

    config = {"configurable": {"thread_id": thread_id}}

    # Check if we can resume from an existing checkpoint (HITL resume)
    try:
        # First, try to get current state - if it exists, we were interrupted
        current_state = graph.get_state(config)
        if current_state and current_state.next:
            print("Resuming interrupted session...")
            result = graph.invoke(None, config=config)
        else:
            # Start fresh
            print("Starting new research session...")
            result = graph.invoke(initial_state, config=config)
    except Exception:
        # Fallback: start fresh
        result = graph.invoke(initial_state, config=config)

    # Handle HITL interrupt before synthesis
    # If interrupted, we wait here - the user can resume manually
    while True:
        current_state = graph.get_state(config)
        if current_state.next and "synthesizer" in current_state.next:
            # Interrupted before synthesis - let user review and approve
            print("\n" + "=" * 60)
            print("REVIEW: Search Results Ready")
            print("=" * 60)

            # Show accumulated results
            search_results = current_state.values.get("search_results", [])
            for i, sr in enumerate(search_results, 1):
                print(f"\n### Iteration {i}: {sr.get('query', 'N/A')}")
                for r in sr.get("results", [])[:3]:
                    print(f"  - {r.get('title', 'No title')}")
                    print(f"    {r.get('url', '')}")

            print("\n" + "=" * 60)
            response = input("\nProceed to synthesis? [y/n]: ").strip().lower()
            if response == "y":
                result = graph.invoke(None, config=config)
                break
            else:
                print("Paused. Run again with same thread_id to resume.")
                sys.exit(0)
        else:
            break

    report = result.get("final_report", "")

    output_dir = PROJECT_ROOT / "output"
    output_dir.mkdir(exist_ok=True)
    with (output_dir / "report.md").open("w", encoding="utf-8") as f:
        f.write(report)

    print("\n" + "=" * 60)
    print("FINAL REPORT")
    print("=" * 60)
    print(report)


if __name__ == "__main__":
    main()
