from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    acceptanceCriteria: str | None = Field(None, alias="acceptanceCriteria")
    assignee: str | None = None
    priority: str = "Low"
    architecture: str = "FE"
    status: str = "to-do"
    storyId: str | None = Field(None, alias="storyId")
    dueDate: str | None = Field(None, alias="dueDate")

    model_config = {"populate_by_name": True}

class TaskOut(BaseModel):
    id: str
    project: str
    title: str
    description: str | None = None
    acceptanceCriteria: str | None = None
    assignee: str | None = None
    priority: str
    architecture: str
    status: str
    storyId: str
    createdAt: datetime
    dueDate: str | None = None
    completedAt: datetime | None = None
