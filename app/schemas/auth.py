from datetime import datetime
from typing import Any, List
from pydantic import BaseModel, EmailStr, constr

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    avatar: str | None
    role_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class GetUserAfterRegistrationSchema(BaseModel):
    status_code: int
    message: str
    data: UserResponse | None

class GetUserAfterLoginSchema(BaseModel):
    status: int
    access_token: str | None
    permissions: List[str] | None