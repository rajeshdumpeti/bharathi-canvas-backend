from typing import Any, Optional
from uuid import UUID
from pydantic import BaseModel, Field

class ProjectHubSectionBase(BaseModel):
    section_type: str = Field(..., example="setup")
    content: dict[str, Any] = Field(..., description="Flexible JSON content for the section")

class ProjectHubSectionCreate(ProjectHubSectionBase):
    project_id: Optional[UUID] = None
    created_by: Optional[str] = None


class ProjectHubSectionOut(ProjectHubSectionBase):
    id: UUID
    project_id: UUID
    created_by: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True,
    }
