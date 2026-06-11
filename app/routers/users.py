from fastapi import APIRouter, Depends, HTTPException, Header
from supabase import Client

from app.config import get_supabase_client
from app.models.user import UserCreate, UserResponse

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

#=====================================================
@router.post("/register", response_model=UserResponse)
def register_user(
    user: UserCreate,
    supabase: Client = Depends(get_supabase_client)
):

    auth_response = supabase.auth.sign_up(
        {
            "email": user.email,
            "password": user.password
        }
    )

    if not auth_response.user:
        raise HTTPException(
            status_code=400,
            detail="Failed to create user"
        )

    user_id = auth_response.user.id

    (
        supabase.table("users")
        .insert(
            {
                "id": user_id,
                "name": user.name,
                "email": user.email
            }
        )
        .execute()
    )

    (
        supabase.table("life_state")
        .insert(
            {
                "user_id": user_id
            }
        )
        .execute()
    )

    return UserResponse(
        id=user_id,
        name=user.name,
        email=user.email,
        created_at=auth_response.user.created_at
    )


#=====================================================
def get_current_user(
    Authorization: str = Header(...),
    supabase: Client = Depends(get_supabase_client)
):

    if not Authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header"
        )

    token = Authorization.split(" ")[1]

    try:
        response = supabase.auth.get_user(token)

        if not response.user:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return response.user

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Authentication failed"
        )
    


#==================================================
@router.get("/me", response_model=UserResponse)
def get_user_profile(
    user=Depends(get_current_user),
    supabase: Client = Depends(get_supabase_client)
):

    response = (
        supabase.table("users")
        .select("*")
        .eq("id", user.id)
        .single()
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return UserResponse(
        id=response.data["id"],
        name=response.data["name"],
        email=response.data["email"],
        created_at=response.data["created_at"]
    )
