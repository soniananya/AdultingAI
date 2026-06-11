from app.agent.state import OfferLetterState
from app.services.extractor import analyze_offer_letter


def analyze_offer_node(
    state: OfferLetterState
):

    analysis = analyze_offer_letter(
        state["extracted_fields"]
    )

    output = {
        "red_flags":
            analysis.red_flags,

        "negotiation_tips":
            analysis.negotiation_tips
    }

    if analysis.requires_hitl:

        output["pending_action"] = {
            "type": "approval",
            "question":
                analysis.approval_question
        }

    return output

#=================================================================


from app.agent.state import OfferLetterState


def prepare_life_state_updates_node(
    state: OfferLetterState
):

    fields = state["extracted_fields"]

    return {
        "pending_life_state_updates": {
            "employer":
                fields.employer,

            "current_salary":
                fields.ctc,

            "joining_date":
                fields.joining_date
        }
    }