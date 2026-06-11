from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class UserCreate(BaseModel):
    email:str
    name:str
    password:str

class UserResponse(BaseModel):
    id:UUID
    email:str
    name:str
    created_at:datetime

class UserInDB(BaseModel):
    id:UUID
    email:str
    hashed_password:str
    created_at:datetime