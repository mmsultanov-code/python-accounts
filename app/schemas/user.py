from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from typing import Any, List, Optional

class CreateUserSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    passwordConfirm: str
    avatar: str
    role_id: int
    creator_id: Optional[int]

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class GetUserAfterLoginSchema(BaseModel):
    avatar: str
    name: str
    email: str

class ResponseLoginUser(BaseModel):
    status_code: int
    message: str
    data: GetUserAfterLoginSchema