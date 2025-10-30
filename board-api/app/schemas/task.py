from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional
from app.models.task import TaskStatus


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.to_do
    assignee: Optional[str] = None
    acceptance_criteria: Optional[str] = None  
    priority: Optional[str] = None    

class TaskCreate(TaskBase):
    project_id: UUID
    feature_id: Optional[UUID] = None  

class TaskOut(TaskBase):
    id: UUID
    project_id: UUID
    feature_id: Optional[UUID] = None  
    user_id: str | UUID  # ✅ allow both UUID and string
    created_at: datetime
    completed_at: Optional[datetime] = None
    story_code: Optional[str] = None

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True,  # ✅ important for UUID serialization
    }
