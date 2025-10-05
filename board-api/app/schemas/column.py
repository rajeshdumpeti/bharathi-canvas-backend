from pydantic import BaseModel
from uuid import UUID

class ColumnCreate(BaseModel):
    title: str

class ColumnOut(BaseModel):
    id: UUID
    key: str
    title: str
    pos: int
