
from app.models.structured_output_models import WorkflowClassification
from app.services.llm import llm
from pydantic import BaseModel


def build_classifier_prompt(
    event_text: str
) -> str:

    return f"""
You are a workflow classifier.

Choose exactly one workflow type: either OFFER_LETTER or JD_ANALYSIS.

Workflow Types:

1. OFFER_LETTER

Examples:
- New job offer
- Employment offer letter
- Joining package
- Compensation letter


2. JD_ANALYSIS

Examples:
- I have an interview at Zepto
- Can you tailor my resume for this role?
- Analyze this job description
- What should I prepare for this interview?
- Backend Engineer JD
- SDE role at Flipkart
- Startup backend position
- FAANG referral opportunity
- Compare my resume against this job description
- Help me prepare for this role


User Event:

{event_text}
"""

#==========================================================




def classify_event(state):

    event_text = state["messages"][-1].content
    structured_llm = (
        llm.with_structured_output(
            WorkflowClassification
        )
    )

    result = structured_llm.invoke(
        build_classifier_prompt(
            event_text
        )
    )

    return {
        "workflow_type":
            result.workflow_type
    }