from uuid import UUID
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str | None = None
    last_name: str | None = None

class UserOut(BaseModel):
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True,
    }
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
