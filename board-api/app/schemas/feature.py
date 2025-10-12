from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class FeatureBase(BaseModel):
    name: str
    details: Optional[str] = None
    user_story: Optional[str] = None
    core_requirements: Optional[str] = None
    acceptance_criteria: Optional[str] = None
    technical_notes: Optional[str] = None


class FeatureCreate(FeatureBase):
    project_id: UUID

class FeatureUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class FeatureOut(FeatureBase):
    id: UUID
    project_id: UUID
    user_id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}