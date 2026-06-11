from langgraph.types import interrupt
from app.config import get_supabase_client
from app.services.supabase import get_life_state,upsert_life_state,save_reminder, update_workflow_status
from app.config import get_supabase_client



def load_user_context_node(state):

    supabase = get_supabase_client()

    life_state = get_life_state(
        user_id=state["user_id"],
        supabase=supabase
    )

    return {
        "life_state": life_state
    }


#=========================================



def update_life_state_node(state):

    updates = state["pending_life_state_updates"]

    if not updates:
        return {
            "life_state_updated": False
        }

    supabase = get_supabase_client()

    upsert_life_state(
        user_id=state["user_id"],
        fields=updates,
        supabase=supabase
    )

    return {
        "life_state_updated": True
    }


#========================================================


def create_reminder_node(state):

    reminders = state.get(
        "pending_reminders",
        []
    )

    if not reminders:

        return {
            "reminder_ids": []
        }

    supabase = get_supabase_client()

    reminder_ids = []

    for reminder in reminders:

        result = save_reminder(
            user_id=state["user_id"],
            workflow_id=state["workflow_id"],
            title=reminder["title"],
            fire_at=reminder["remind_at"],
            supabase=supabase
        )

        reminder_ids.append(
            result["id"]
        )

    return {
        "reminder_ids": reminder_ids
    }



#==============================================================
def create_reminder_node(state):     #persistence node. saves data

    reminders = state["pending_reminders"]

    if not reminders:
        return {}

    supabase = get_supabase_client()

    for rem in reminders:

        save_reminder(
            user_id=state["user_id"],
            workflow_id=state["workflow_id"],
            title=rem["title"],
            fire_at=rem["remind_at"],
            supabase=supabase
        )

    return {}



#======================================================


def error_handler_node(state):              #logs errors in workflow table

    supabase = get_supabase_client()

    update_workflow_status(
        workflow_id=state["workflow_id"],
        status="FAILED",
        context={
            "errors": state["errors"]
        },
        supabase=supabase
    )

    return {}



#===================hitl=================================
def hitl_node(state):

    supabase = get_supabase_client()

    update_workflow_status(
        workflow_id=state["workflow_id"],
        status="PAUSED",
        context=state["pending_action"],
        supabase=supabase
    )

    response = interrupt(
        state["pending_action"]
    )

    return {
        "hitl_approved": response
    }


#=======================================================

def persist_state_node(state):

    supabase = get_supabase_client()

    update_workflow_status(
        workflow_id=state["workflow_id"],
        status="COMPLETED",
        context={},
        supabase=supabase
    )

    return {
        "workflow_completed": True
    }

