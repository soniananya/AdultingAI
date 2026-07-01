from langgraph.graph import (
    StateGraph,
    END,
)

from app.agent.state import (
    OfferLetterState,
)

from app.agent.nodes.offer_letter import (
    analyze_offer_node,
    prepare_life_state_updates_node,
)

from app.agent.nodes.common import (
    hitl_node,
    update_life_state_node,
    persist_state_node,
)


def route_after_hitl(state):

    if state["hitl_approved"]:
        return "approved"

    return "rejected"


def build_graph():

    builder = StateGraph(
        OfferLetterState
    )

    builder.add_node(
        "analyze_offer",
        analyze_offer_node
    )

    builder.add_node(
        "prepare_life_state_updates",
        prepare_life_state_updates_node
    )

    builder.add_node(
        "hitl",
        hitl_node
    )

    builder.add_node(
        "update_life_state",
        update_life_state_node
    )

    builder.add_node(
        "persist_state",
        persist_state_node
    )

    builder.set_entry_point(
        "analyze_offer"
    )

    builder.add_edge(
        "analyze_offer",
        "prepare_life_state_updates"
    )

    builder.add_edge(
        "prepare_life_state_updates",
        "hitl"
    )

    builder.add_conditional_edges(
        "hitl",
        route_after_hitl,
        {
            "approved":
                "update_life_state",

            "rejected":
                END,
        }
    )

    builder.add_edge(
        "update_life_state",
        "persist_state"
    )

    builder.add_edge(
        "persist_state",
        END
    )

    return builder.compile()



"""
Offer Letter Workflow Graph

Purpose:
- Analyze a user's offer letter
- Extract compensation and employment details
- Generate proposed life state updates
- Present findings for human approval (HITL)
- Persist approved updates to LifeState

Workflow:

analyze_offer
    ↓
prepare_life_state_updates
    ↓
hitl
    ↓

approved?
    ├── YES
    │      ↓
    │ update_life_state
    │      ↓
    │ persist_state
    │      ↓
    │ END
    │
    └── NO
           ↓
          END

Key Design Decisions:

- No life_state updates are written before user approval.
- HITL acts as a safety gate for salary, employer,
  joining date, and other extracted employment facts.
- Rejected workflows exit without modifying user data.
- Nodes contain business logic; this file only defines
  execution order and routing.
"""