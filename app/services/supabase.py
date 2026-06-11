from supabase import Client 



def get_life_state(
    user_id: str,
    supabase: Client
):

    response = (
        supabase.table("life_state")
        .select("*")
        .eq("user_id", user_id)
        .single()
        .execute()
    )

    return response.data



#===========================================
def upsert_life_state(
    user_id: str,
    fields: dict,
    supabase: Client
):

    response = (
        supabase.table("life_state")
        .update(fields)
        .eq("user_id", user_id)
        .execute()
    )

    return response.data

#============================================
def create_workflow(
    user_id: str,
    event_text: str,
    supabase: Client
):

    response = (
        supabase.table("workflows")
        .insert(
            {
                "user_id": user_id,
                "event_text": event_text,
                "status": "CREATED"
            }
        )
        .execute()
    )

    return response.data[0]

#=====================================
def update_workflow_status(
    workflow_id: int,
    status: str,
    context: dict,
    supabase: Client
):

    response = (
        supabase.table("workflows")
        .update(
            {
                "status": status,
                "context": context
            }
        )
        .eq("id", workflow_id)
        .execute()
    )

    return response.data

#===============================================
def log_workflow_step(
    workflow_id: int,
    node: str,
    input_data: dict,
    output_data: dict,
    supabase: Client
):

    response = (
        supabase.table("workflow_steps")
        .insert(
            {
                "workflow_id": workflow_id,
                "tool_called": node,
                "output": {
                    "input": input_data,
                    "output": output_data
                },
                "status": "success"
            }
        )
        .execute()
    )

    return response.data

#=====================================================
def save_document(
    user_id: str,
    doc_type: str,
    url: str,
    fields: dict,
    version: int,
    supabase: Client
):

    response = (
        supabase.table("documents")
        .insert(
            {
                "user_id": user_id,
                "type": doc_type,
                "storage_url": url,
                "extracted_fields": fields,
                "version": version
            }
        )
        .execute()
    )

    return response.data[0]


#===================================================
def get_latest_document(
    user_id: str,
    doc_type: str,
    supabase: Client
):

    response = (
        supabase.table("documents")
        .select("*")
        .eq("user_id", user_id)
        .eq("type", doc_type)
        .order("version", desc=True)
        .limit(1)
        .execute()
    )

    if not response.data:
        return None

    return response.data[0]



#====================================================
def save_artifact(
    user_id: str,
    workflow_id: int,
    artifact_type: str,
    content: dict,
    supabase: Client
):

    response = (
        supabase.table("artifacts")
        .insert(
            {
                "user_id": user_id,
                "workflow_id": workflow_id,
                "type": artifact_type,
                "content": content
            }
        )
        .execute()
    )

    return response.data[0]



#=========================================================
def save_reminder(
    user_id: str,
    workflow_id: int,
    title: str,
    fire_at,
    supabase: Client
):

    response = (
        supabase.table("reminders")
        .insert(
            {
                "user_id": user_id,
                "workflow_id": workflow_id,
                "title": title,
                "remind_at": fire_at
            }
        )
        .execute()
    )

    return response.data[0]


#=============================================================
