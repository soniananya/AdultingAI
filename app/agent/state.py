from typing import TypedDict, Annotated

from pydantic import BaseModel

from app.models.workflow import WorkflowType

from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage


# =====================================================
# LIFE STATE SNAPSHOT
# =====================================================

class LifeStateSnapshot(BaseModel):

    current_salary: float | None

    employer: str | None

    monthly_rent: float | None

    current_city: str | None

    housing_type: str | None

    employment_type: str | None

    joining_date: str | None

    recurring_bills: list

    resume_url: str | None

    skills: list[str]

# =====================================================
# BASE GRAPH STATE
# =====================================================

class AdultingBaseState(TypedDict):

    user_id: str

    workflow_id: int

    workflow_type: WorkflowType

    life_state: LifeStateSnapshot

    messages: Annotated[list, add_messages]

    pending_life_state_updates: dict

    pending_reminders: list[dict]

    pending_artifacts: list[dict]

    errors: list[str]

    hitl_approved: bool | None

    pending_action: dict | None


# =====================================================
# SALARY SLIP STATE
# =====================================================

class SalarySlipState(
    AdultingBaseState
):

    document_id: int

    extracted_fields: dict

    parsed_salary: dict

    anomalies: list[str]


# =====================================================
# OFFER LETTER STATE
# =====================================================

class OfferLetterState(
    AdultingBaseState
):

    document_id: int

    extracted_fields: dict

    ctc_breakdown: dict

    red_flags: list[str]

    negotiation_tips: list[str]


# =====================================================
# RECURRING BILL STATE
# =====================================================

class RecurringBillState(
    AdultingBaseState
):

    bill_name: str

    amount: float

    due_day: int

    frequency: str

    reminder_id: int | None


# =====================================================
# JD ANALYSIS MODELS
# =====================================================

class JDRequirements(BaseModel):

    must_have: list[str]

    nice_to_have: list[str]

    technologies: list[str]

    experience_level: str | None


class InterviewPrep(BaseModel):

    key_topics: list[str]

    likely_questions: list[str]

    learning_priority: list[str]


# =====================================================
# JD ANALYSIS STATE
# =====================================================

class JDAnalysisState(
    AdultingBaseState
):

    jd_text: str

    resume_text: str

    jd_requirements: JDRequirements

    skill_gaps: list[str]

    tailored_resume: str

    interview_prep: InterviewPrep


# =====================================================
# INITIAL STATE FACTORY
# =====================================================

def initial_state(
    user_id: str,
    workflow_id: int,
    event_text: str,
    extracted_fields=None
):

    # NOTE: life_state and workflow_type are populated by the graph itself
    # (load_user_context_node loads life_state, classify_event sets workflow_type).
    return {

        "user_id": user_id,

        "workflow_id": workflow_id,

        "life_state": None,

        "extracted_fields": extracted_fields,

        "messages": [
            HumanMessage(
                content=event_text
            )
        ],

        "pending_life_state_updates": {},

        "pending_reminders": [],

        "pending_artifacts": [],

        "errors": [],

        "hitl_approved": None,

        "pending_action": None
    }