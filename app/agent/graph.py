"""
Main Adulting AI Graph

Responsibilities:

1. Load user context
2. Classify incoming event
3. Route to the correct workflow sub-graph
4. Attach LangGraph checkpointer

Business logic belongs inside workflow graphs.
This file only handles top-level orchestration.
"""

from langgraph.graph import (
    StateGraph,
    END,
)

from app.models.workflow import (
    WorkflowType,
)

from app.agent.state import (
    AdultingBaseState,
)

from app.agent.nodes.common import (
    load_user_context_node,
    error_handler_node,
)

from app.agent.nodes.classifier import (
    classify_event,
)

from app.agent.graphs.jd_analysis import (
    build_jd_analysis_graph,
)

from app.agent.graphs.offer_letter import (
    build_offer_letter_graph,
)

from app.agent.checkpointer import (
    get_checkpointer,
)


# =====================================================
# ROUTING
# =====================================================

def route_after_classify(state):

    mapping = {

        WorkflowType.JD_ANALYSIS:
            "jd_analysis",

        WorkflowType.OFFER_LETTER:
            "offer_letter",
    }

    return mapping.get(
        state["workflow_type"],
        "error_handler"
    )


# =====================================================
# MAIN GRAPH
# =====================================================

def build_main_graph():

    builder = StateGraph(
        AdultingBaseState
    )

    builder.add_node(
        "load_user_context",
        load_user_context_node
    )

    builder.add_node(
        "classifier",
        classify_event
    )

    builder.add_node(
        "jd_analysis",
        build_jd_analysis_graph()
    )

    builder.add_node(
        "offer_letter",
        build_offer_letter_graph()
    )

    builder.add_node(
        "error_handler",
        error_handler_node
    )

    builder.set_entry_point(
        "load_user_context"
    )

    builder.add_edge(
        "load_user_context",
        "classifier"
    )

    builder.add_conditional_edges(
        "classifier",
        route_after_classify,
        {
            "jd_analysis":
                "jd_analysis",

            "offer_letter":
                "offer_letter",

            "error_handler":
                "error_handler",
        }
    )

    builder.add_edge(
        "jd_analysis",
        END
    )

    builder.add_edge(
        "offer_letter",
        END
    )

    builder.add_edge(
        "error_handler",
        END
    )

    return builder.compile(
        checkpointer=
        get_checkpointer()
    )