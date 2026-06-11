from fastapi import APIRouter, Depends,HTTPException
from supabase import Client
from app.config import get_supabase_client
from app.routers.users import get_current_user
from app.models.lifestate import LifeState,LifeStateUpdate

router=APIRouter(prefix="/lifestate")


#=========================================
@router.get("/", response_model=LifeState)
def get_life_state(
    user=Depends(get_current_user),
    supabase: Client = Depends(get_supabase_client)
):

    response = (
        supabase.table("life_state")
        .select("*")
        .eq("user_id", user.id)
        .single()
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Life state not found"
        )

    return LifeState(**response.data)





#=================================================
@router.patch("/update")
def update_life_state(
    update: LifeStateUpdate,
    user=Depends(get_current_user),
    supabase: Client = Depends(get_supabase_client)
):
    update_data = {
        field: getattr(update, field)
        for field in update.model_fields_set
    }

    response = (
        supabase.table("life_state")
        .update(update_data)
        .eq("user_id", user.id)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Life state not found"
        )

    return LifeState(**response.data[0])