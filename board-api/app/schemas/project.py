from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    """Schema used for creating a new project"""
    pass

class ProjectOut(ProjectBase):
    id: UUID  # or UUID if you prefer
    columns: list[str] | None = None

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True,
    }
