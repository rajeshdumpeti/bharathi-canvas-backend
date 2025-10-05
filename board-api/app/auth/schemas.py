from uuid import UUID
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    is_active: bool

    model_config = {
        "from_attributes": True,
    }

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
