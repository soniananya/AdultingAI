
from app.models.structured_output_models import WorkflowClassification
from app.services.llm import llm
from pydantic import BaseModel


def build_classifier_prompt(
    event_text: str
) -> str:

    return f"""
You are a workflow classifier.

Choose exactly one workflow type.

Workflow Types:

1. SALARY_SLIP
   Examples:
   - Uploaded salary slip
   - Payslip for May 2026
   - Monthly salary statement

2. OFFER_LETTER
   Examples:
   - New job offer
   - Employment offer letter
   - Joining package
   - Compensation letter

3. RECURRING_BILL
   Examples:
   - Electricity bill every month
   - Rent reminder
   - Internet bill reminder
   - Credit card due reminder

User Event:

{event_text}
"""


#==========================================================




def classify_event(state):

    structured_llm = (
        llm.with_structured_output(
            WorkflowClassification
        )
    )

    result = structured_llm.invoke(
        build_classifier_prompt(
            state["event_text"]
        )
    )

    return {
        "workflow_type":
            result.workflow_type
    }