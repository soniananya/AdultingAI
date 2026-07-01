from langgraph.types import interrupt


# =====================================================
# QUESTION BUILDER
# =====================================================

def build_question_for_field(
    field_name,
    workflow_type
):

    questions = {

        "resume_url":
            "Please upload your current resume (PDF).",

        "skills":
            "List your key skills (for example: Python, FastAPI, SQL).",

        "current_city":
            "Which city are you currently living in?",
    }

    return questions.get(
        field_name,
        f"Please provide {field_name}"
    )


# =====================================================
# RESOLVE GAP
# =====================================================

def resolve_gap(
    state
):

    missing_fields = (
        state["missing_fields"]
    )

    if not missing_fields:

        return {}

    field_name = (
        missing_fields[0]
    )

    question = (
        build_question_for_field(
            field_name,
            state["workflow_type"]
        )
    )

    return interrupt(
        {
            "field_name":
                field_name,

            "question":
                question
        }
    )


# =====================================================
# INJECT ANSWER
# =====================================================

def inject_answer(
    state,
    field_name,
    answer
):

    setattr(
        state["life_state"],
        field_name,
        answer
    )

    missing_fields = [

        field

        for field in state["missing_fields"]

        if field != field_name
    ]

    return {

        "life_state":
            state["life_state"],

        "missing_fields":
            missing_fields
    }