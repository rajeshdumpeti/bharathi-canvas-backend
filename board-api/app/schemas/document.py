from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel


class DocumentBase(BaseModel):
    project_id: UUID
    original_name: str
    file_type: Optional[str] = None
    file_size: Optional[int] = None


class DocumentCreate(DocumentBase):
    """Used when creating or uploading a document"""
    pass


class DocumentOut(DocumentBase):
    """Returned in API responses"""
    id: UUID
    filename: str
    uploaded_at: datetime

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True,
    }
