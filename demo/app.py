"""
Streamlit demo UI for the Competitive Intelligence Agent.

Shows:
- Original query at top
- Live-updating panel for each search iteration
- "Review Sources" button (triggers HITL interrupt)
- Final report rendered as formatted Markdown
"""

import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from research_agent import ResearchState, build_graph


def main():
    load_dotenv(PROJECT_ROOT / ".env")

    st.set_page_config(
        page_title="Competitive Intelligence Agent",
        page_icon="🎯",
        layout="wide",
    )

    st.title("🎯 Competitive Intelligence & Campaign Strategy Agent")

    # Sidebar for configuration
    st.sidebar.header("Configuration")
    thread_id = st.sidebar.text_input(
        "Thread ID",
        value="streamlit-demo",
        help="Unique ID to resume a session",
    )
    query = st.sidebar.text_input(
        "Research Query",
        value="Competitive landscape for SEA cybersecurity compliance SaaS",
    )

    # Initialize session state
    if "graph" not in st.session_state:
        st.session_state.graph = build_graph(PROJECT_ROOT / "research_memory.db")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    graph = st.session_state.graph
    config = {"configurable": {"thread_id": thread_id}}

    # Check for existing state
    try:
        current_state = graph.get_state(config)
        has_checkpoint = current_state is not None and bool(current_state.values)
    except Exception:
        has_checkpoint = False

    # Query input section
    st.header("Research Query")
    st.info(query)

    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        start_disabled = has_checkpoint
        if st.button("🚀 Start New Research", disabled=start_disabled):
            initial_state: ResearchState = {
                "original_query": query,
                "sub_questions": [],
                "search_results": [],
                "iteration_count": 0,
                "evaluation_score": 0.0,
                "should_continue": True,
                "final_report": "",
                "messages": [],
            }
            result = graph.invoke(initial_state, config=config)
            st.session_state.current_result = result
            st.rerun()

    with col2:
        resume_disabled = not has_checkpoint
        if st.button("▶️ Resume", disabled=resume_disabled):
            result = graph.invoke(None, config=config)
            st.session_state.current_result = result
            st.rerun()

    # Display current state
    if has_checkpoint:
        st.divider()
        st.subheader("📊 Current Research State")

        state_values = current_state.values

        # Iteration count
        iteration = state_values.get("iteration_count", 0)
        st.metric("Iterations Completed", iteration)

        # Sub-questions
        sub_questions = state_values.get("sub_questions", [])
        if sub_questions:
            with st.expander(f"📝 Sub-Questions ({len(sub_questions)})", expanded=True):
                for i, q in enumerate(sub_questions, 1):
                    st.markdown(f"**{i}.** {q}")

        # Search results
        search_results = state_values.get("search_results", [])
        if search_results:
            with st.expander(f"🔍 Search Results ({len(search_results)})", expanded=True):
                for i, sr in enumerate(search_results, 1):
                    st.markdown(f"**Iteration {i}:** {sr.get('query', 'N/A')}")
                    for r in sr.get("results", [])[:3]:
                        with st.container():
                            st.markdown(f"- [{r.get('title', 'No title')}]({r.get('url', '')})")
                    st.divider()

        # Evaluation score
        eval_score = state_values.get("evaluation_score", 0.0)
        if eval_score > 0:
            st.metric("Evaluation Score", f"{eval_score:.2f}")

        # Check if interrupted before synthesis
        if current_state.next and "synthesizer" in current_state.next:
            st.warning("⏸️ Paused - Ready for source review before synthesis")
            st.info("Please review the accumulated search results in the expanders above.")

            # Approve & Synthesize button (direct, not nested)
            if st.button("✅ Approve & Synthesize"):
                result = graph.invoke(None, config=config)
                st.session_state.current_result = result
                st.rerun()

    # Final report
    st.divider()
    if "current_result" in st.session_state:
        result = st.session_state.current_result
        report = result.get("final_report", "")
        if report:
            st.subheader("📋 Final Report")
            st.markdown(report)

            # Download button
            st.download_button(
                label="💾 Download Report",
                data=report,
                file_name="competitive_intel_report.md",
                mime="text/markdown",
            )
        else:
            st.info("Run or resume the research to generate a report.")
    else:
        st.info("Start a new research session or resume an existing one.")


if __name__ == "__main__":
    main()
