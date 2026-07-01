from langgraph.graph import (
    StateGraph,
    END,
)

from app.agent.state import (
    JDAnalysisState,
)

from app.agent.nodes.inspector import (
    inspect_life_state,
)

from app.agent.nodes.resolve_gap import (
    resolve_gap,
)

from app.agent.nodes.jd_analysis import (
    extract_jd_node,
    analyse_resume_node,
    tailor_resume_node,
    build_prep_list_node,
)

from app.agent.nodes.common import (
    hitl_node,
    persist_state_node,
)


def route_after_inspect(state):

    if state["missing_fields"]:
        return "resolve_gap"

    return "continue"


def route_after_hitl(state):

    if state["hitl_approved"]:
        return "approved"

    return "rejected"


def build_graph():

    builder = StateGraph(
        JDAnalysisState
    )

    builder.add_node(
        "inspect_life_state",
        inspect_life_state
    )

    builder.add_node(
        "resolve_gap",
        resolve_gap
    )

    builder.add_node(
        "extract_jd",
        extract_jd_node
    )

    builder.add_node(
        "analyse_resume",
        analyse_resume_node
    )

    builder.add_node(
        "tailor_resume",
        tailor_resume_node
    )

    builder.add_node(
        "build_prep_list",
        build_prep_list_node
    )

    builder.add_node(
        "hitl",
        hitl_node
    )

    builder.add_node(
        "persist_state",
        persist_state_node
    )

    builder.set_entry_point(
        "inspect_life_state"
    )

    builder.add_conditional_edges(
        "inspect_life_state",
        route_after_inspect,
        {
            "resolve_gap":
                "resolve_gap",

            "continue":
                "extract_jd",
        }
    )

    builder.add_edge(
        "resolve_gap",
        "inspect_life_state"
    )

    builder.add_edge(
        "extract_jd",
        "analyse_resume"
    )

    builder.add_edge(
        "analyse_resume",
        "tailor_resume"
    )

    builder.add_edge(
        "tailor_resume",
        "build_prep_list"
    )

    builder.add_edge(
        "build_prep_list",
        "hitl"
    )

    builder.add_conditional_edges(
        "hitl",
        route_after_hitl,
        {
            "approved":
                "persist_state",

            "rejected":
                END,
        }
    )

    builder.add_edge(
        "persist_state",
        END
    )

    return builder.compile()