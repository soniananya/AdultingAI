from app.models.workflow import WorkflowType


# =====================================================
# REQUIRED FIELDS PER WORKFLOW
# =====================================================

def get_required_fields_for_workflow(
    workflow_type
):


    
    if workflow_type == WorkflowType.JD_ANALYSIS:   # dont need for other workflows yet, because none req previous fields.

        return [
            "resume_url"
        ]

    return []


# ===========================INSPECT LIFE STATE=========================

def inspect_life_state(
    state
):

    required_fields = (
        get_required_fields_for_workflow(
            state["workflow_type"]
        )
    )

    life_state = state["life_state"]

    missing_fields = []

    for field in required_fields:

        value = getattr(
            life_state,
            field,
            None
        )

        if (
            value is None
            or value == ""
            or value == []
        ):

            missing_fields.append(
                field
            )

    return {
        "missing_fields":
            missing_fields
    }