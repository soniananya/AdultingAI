from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from supabase import Client
from app.routers.users import get_current_user
from app.config import get_supabase_client
from app.services.storage import upload_file, get_file_bytes
from app.services.extractor import (
    extract_text_from_pdf,
    extract_offer_letter_fields,
    extract_salary_slip_fields,
)

router = APIRouter(prefix="/documents", tags=["documents"])


# ========================================================
def extract_document(
    storage_url: str,
    doc_type: str,
    supabase: Client
) -> dict:
    """
    Download an uploaded document, pull out its text, and run the
    matching structured extractor. Returns a JSON-serializable dict
    suitable for the documents.extracted_fields column.
    """

    file_bytes = get_file_bytes(storage_url, supabase)
    text = extract_text_from_pdf(file_bytes)

    if doc_type == "OFFER_LETTER":
        return extract_offer_letter_fields(text).model_dump()

    if doc_type == "SALARY_SLIP":
        return extract_salary_slip_fields(text).model_dump()

    # Unknown document type: store the raw text only.
    return {"raw_text": text}


# ========================================================
@router.get("/")
def get_documents(
    user=Depends(get_current_user),
    supabase: Client = Depends(get_supabase_client)
):

    response = (
        supabase.table("documents")
        .select("*")
        .eq("user_id", user.id)
        .order("uploaded_at", desc=True)
        .execute()
    )

    return response.data


# ========================================================
@router.get("/{doc_id}")
def get_document(
    doc_id: int,
    user=Depends(get_current_user),
    supabase: Client = Depends(get_supabase_client)
):

    response = (
        supabase.table("documents")
        .select("*")
        .eq("id", doc_id)
        .eq("user_id", user.id)
        .single()
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return response.data


# ========================================================
@router.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    doc_type: str = Form(...),
    user=Depends(get_current_user),
    supabase: Client = Depends(get_supabase_client)
):

    # upload file to storage
    storage_url = upload_file(
        user_id=user.id,
        file=file,
        doc_type=doc_type,
        supabase=supabase
    )

    # extract fields from document
    extracted_fields = extract_document(
        storage_url,
        doc_type,
        supabase
    )

    response = (
        supabase.table("documents")
        .insert(
            {
                "user_id": user.id,
                "type": doc_type,
                "storage_url": storage_url,
                "extracted_fields": extracted_fields
            }
        )
        .execute()
    )

    document_id = response.data[0]["id"]

    # Analysis is triggered separately via POST /workflows/run
    # (pass this document_id to run the matching workflow).
    return {
        "document_id": document_id,
        "extracted_fields": extracted_fields
    }


# ========================================================
@router.get("/{doc_id}/diff")
def get_document_diff(
    doc_id: int,
    user=Depends(get_current_user),
    supabase: Client = Depends(get_supabase_client)
):

    # Get current document
    current_response = (
        supabase.table("documents")
        .select("*")
        .eq("id", doc_id)
        .eq("user_id", user.id)
        .single()
        .execute()
    )

    if not current_response.data:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    current_doc = current_response.data

    # Find previous version of same document type
    previous_response = (
        supabase.table("documents")
        .select("*")
        .eq("user_id", user.id)
        .eq("type", current_doc["type"])
        .lt("version", current_doc["version"])
        .order("version", desc=True)
        .limit(1)
        .execute()
    )

    if not previous_response.data:
        return {
            "document_id": doc_id,
            "changes": {},
            "message": "No previous version found"
        }

    previous_doc = previous_response.data[0]

    old_fields = previous_doc["extracted_fields"] or {}
    new_fields = current_doc["extracted_fields"] or {}

    changes = {}

    all_keys = set(old_fields.keys()) | set(new_fields.keys())

    for key in all_keys:

        old_value = old_fields.get(key)
        new_value = new_fields.get(key)

        if old_value != new_value:
            changes[key] = {
                "old": old_value,
                "new": new_value
            }

    return {
        "document_id": doc_id,
        "previous_document_id": previous_doc["id"],
        "changes": changes
    }
