from fastapi import UploadFile
from supabase import Client

from app.config import get_supabase_client


def upload_file(
    user_id: str,
    file: UploadFile,
    doc_type: str,
    supabase: Client
):

    path = f"documents/{user_id}/{doc_type}_{file.filename}"

    file_bytes = file.file.read()

    supabase.storage.from_("documents").upload(
        path,
        file_bytes
    )

    return path

#===============================================================
def get_file_bytes(
    storage_url: str,
    supabase: Client
):

    file_bytes = (
        supabase.storage
        .from_("documents")
        .download(storage_url)
    )

    return file_bytes

#=======================================================
def download_file(
    storage_url: str
):
    # Convenience wrapper for agent nodes, which don't have a
    # FastAPI-injected Supabase client.
    supabase = get_supabase_client()

    return get_file_bytes(storage_url, supabase)

#=======================================================

def delete_file(
    storage_url: str,
    supabase: Client
):

    supabase.storage.from_("documents").remove(
        [storage_url]
    )

    return True

#==================================================