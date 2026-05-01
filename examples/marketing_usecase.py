import os

from dotenv import load_dotenv

from src.graph import build_graph


def main():
    load_dotenv()

    graph = build_graph()
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

    result = graph.invoke(initial_state, config={"configurable": {"thread_id": thread_id}})
    report = result.get("final_report", "")

    os.makedirs("output", exist_ok=True)
    with open("output/report.md", "w", encoding="utf-8") as f:
        f.write(report)

    print(report)


if __name__ == "__main__":
    main()
