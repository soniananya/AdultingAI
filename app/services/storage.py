from fastapi import UploadFile
from supabase import Client


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

def delete_file(
    storage_url: str,
    supabase: Client
):

    supabase.storage.from_("documents").remove(
        [storage_url]
    )

    return True

#==================================================