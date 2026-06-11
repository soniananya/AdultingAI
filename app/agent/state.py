from typing import TypedDict, Annotated

from app.services.supabase import get_life_state 
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage
 
class LifeStateSnapshot(TypedDict):
    current_salary: float | None
    employer: str | None

    monthly_rent: float | None

    current_city: str | None
    housing_type: str | None

    employment_type: str | None
    joining_date: str | None

    recurring_bills: list

    
class AdultingBaseState(TypedDict):

    user_id: str

    workflow_id: int

    workflow_type: str

    life_state: LifeStateSnapshot

    messages: Annotated[list, add_messages]

    pending_life_state_updates: dict

    pending_reminders: list[dict]

    errors: list[str]

    hitl_approved: bool | None

    pending_action: dict | None



class SalarySlipState(
    AdultingBaseState
):

    document_id: int

    extracted_fields: dict

    parsed_salary: dict

    anomalies: list[str]

    artifact: dict | None



class OfferLetterState(
    AdultingBaseState
):

    document_id: int

    extracted_fields: dict

    ctc_breakdown: dict

    red_flags: list[str]

    negotiation_tips: list[str]

    artifact: dict | None



class RecurringBillState(
    AdultingBaseState
):

    bill_name: str

    amount: float

    due_day: int

    frequency: str

    reminder_id: int | None



def initial_state(
    user_id,
    workflow_id,
    workflow_type,
    event_text
):
    return{
    "user_id": user_id,

    "workflow_id": workflow_id,

    "workflow_type": workflow_type,

    "life_state": get_life_state(user_id),

    "messages": [
        HumanMessage(
            content=event_text
        )
    ],

    "pending_life_state_updates":{},
    
    "pending_reminders":[],

    "errors": [],

    "hitl_approved": None,

    "pending_action": None
}