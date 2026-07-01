from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from supabase import Client

from app.config import get_supabase_client
from app.routers.users import get_current_user
from app.services.supabase import create_workflow
from app.models.structured_output_models import OfferLetterFields

router = APIRouter(prefix="/workflows", tags=["workflows"])


# The compiled graph is built lazily and reused across requests.
_graph = None


def _get_graph():
    global _graph
    if _graph is None:
        from app.agent.graph import build_main_graph
        _graph = build_main_graph()
    return _graph


def _summarize(result: dict) -> dict:
    """Pull the user-facing fields out of the final graph state."""
    keys = [
        "workflow_type",
        "red_flags",
        "negotiation_tips",
        "tailored_resume",
        "prep_list",
        "skill_gaps",
        "keyword_mismatches",
        "jd_requirements",
        "pending_action",
        "errors",
    ]

    summary = {k: result[k] for k in keys if k in result}

    # A workflow paused at a human-in-the-loop / gap step surfaces __interrupt__.
    summary["interrupted"] = "__interrupt__" in result

    return summary


class RunWorkflowRequest(BaseModel):
    event_text: str
    document_id: int | None = None


# ========================================================
@router.post("/run")
def run_workflow(
    body: RunWorkflowRequest,
    user=Depends(get_current_user),
    supabase: Client = Depends(get_supabase_client)
):

    workflow = create_workflow(
        user_id=user.id,
        event_text=body.event_text,
        supabase=supabase
    )
    workflow_id = workflow["id"]

    # For document-driven workflows (e.g. offer letters) load the fields
    # extracted at upload time so the graph doesn't re-parse the file.
    extracted_fields = None

    if body.document_id is not None:

        doc = (
            supabase.table("documents")
            .select("*")
            .eq("id", body.document_id)
            .eq("user_id", user.id)
            .single()
            .execute()
        )

        if not doc.data:
            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )

        raw_fields = doc.data.get("extracted_fields") or {}

        if doc.data.get("type") == "OFFER_LETTER":
            extracted_fields = OfferLetterFields(**raw_fields)
        else:
            extracted_fields = raw_fields

    from app.agent.state import initial_state

    state = initial_state(
        user_id=user.id,
        workflow_id=workflow_id,
        event_text=body.event_text,
        extracted_fields=extracted_fields
    )

    graph = _get_graph()

    config = {
        "configurable": {
            "thread_id": str(workflow_id)
        }
    }

    result = graph.invoke(state, config=config)

    return {
        "workflow_id": workflow_id,
        "result": _summarize(result)
    }


# ========================================================
@router.get("/")
def list_workflows(
    user=Depends(get_current_user),
    supabase: Client = Depends(get_supabase_client)
):

    response = (
        supabase.table("workflows")
        .select("*")
        .eq("user_id", user.id)
        .order("created_at", desc=True)
        .execute()
    )

    return response.data


# ========================================================
@router.get("/{workflow_id}")
def get_workflow(
    workflow_id: int,
    user=Depends(get_current_user),
    supabase: Client = Depends(get_supabase_client)
):

    response = (
        supabase.table("workflows")
        .select("*")
        .eq("id", workflow_id)
        .eq("user_id", user.id)
        .single()
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found"
        )

    return response.data
