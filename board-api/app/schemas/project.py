from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel
from app.schemas.column import BoardColumnOut
from app.schemas.task import TaskOut

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectOut(ProjectBase):
    id: UUID
    columns: Optional[List[BoardColumnOut]] = None  
    tasks: Optional[List[TaskOut]] = None   


    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True,
    }
