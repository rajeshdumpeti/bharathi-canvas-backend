from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    """Schema used for creating a new project"""
    pass

class ProjectOut(ProjectBase):
    id: str  # or UUID if you prefer
    columns: list[str] | None = None

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True,
    }
