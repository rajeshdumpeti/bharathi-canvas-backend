from pydantic import BaseModel
from uuid import UUID


class BoardColumnBase(BaseModel):
    title: str


class BoardColumnCreate(BoardColumnBase):
    pass


class BoardColumnOut(BoardColumnBase):
    id: UUID
    key: str
    pos: int

    model_config = {"from_attributes": True}
