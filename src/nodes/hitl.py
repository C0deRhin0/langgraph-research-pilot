from src.state import ResearchState


def hitl_node(state: ResearchState) -> ResearchState:
    """Human-in-the-loop placeholder.

    This node is not invoked directly, but the graph is compiled with
    interrupt_before=["synthesizer"] to allow manual approval.
    """

    return state
